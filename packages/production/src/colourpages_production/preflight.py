"""KDP preflight validation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import imagehash
from PIL import Image

from .catalog import load_book
from .config import DPI, PROMPT_BANNER_RATIO, PROMPT_FOOTER_RATIO, book_data_dir, page_spec


@dataclass
class CheckResult:
    name: str
    passed: bool
    message: str
    severity: str = "error"  # error | warning


@dataclass
class PreflightReport:
    book_id: str
    passed: bool
    checks: list[CheckResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "book_id": self.book_id,
            "passed": self.passed,
            "checks": [
                {"name": c.name, "passed": c.passed, "message": c.message, "severity": c.severity}
                for c in self.checks
            ],
        }


def _is_bw_pixel(r: int, g: int, b: int, tolerance: int = 15) -> bool:
    if r > 240 and g > 240 and b > 240:
        return True
    if r < tolerance and g < tolerance and b < tolerance:
        return True
    return False


def check_page_count(book: dict[str, Any]) -> CheckResult:
    count = book.get("page_count", 0)
    if count < 24:
        return CheckResult("page_count", False, f"Page count {count} is below KDP minimum of 24")
    if count % 2 != 0:
        return CheckResult("page_count", False, f"Page count {count} must be even")
    return CheckResult("page_count", True, f"Page count {count} is valid")


def check_art_files(book_id: str, book: dict[str, Any]) -> list[CheckResult]:
    results: list[CheckResult] = []
    spec = page_spec(book["trim"], book.get("kdp", {}).get("bleed", False))
    laid_out = book_data_dir(book_id) / "art" / "laid-out"
    pages = book.get("pages", [])
    art_count = book.get("art_page_count", len(pages))

    if not laid_out.exists():
        return [CheckResult("art_files", False, f"Missing laid-out directory: {laid_out}")]

    hashes: list[tuple[str, int]] = []
    for i in range(1, art_count + 1):
        path = laid_out / f"{i:03d}.png"
        if not path.exists():
            results.append(CheckResult(f"page_{i:03d}_exists", False, f"Missing page: {path}"))
            continue

        img = Image.open(path).convert("RGB")
        w, h = img.size
        # Hash art region only (excludes prompt banners that may look similar)
        art_top = int(h * PROMPT_BANNER_RATIO)
        art_bottom = h - int(h * PROMPT_FOOTER_RATIO)
        art_crop = img.crop((0, art_top, w, art_bottom))
        if w != spec.width_px or h != spec.height_px:
            results.append(
                CheckResult(
                    f"page_{i:03d}_dimensions",
                    False,
                    f"Page {i}: {w}x{h}px, expected {spec.width_px}x{spec.height_px}px at {DPI} DPI",
                )
            )
        else:
            results.append(CheckResult(f"page_{i:03d}_dimensions", True, f"Page {i} dimensions OK"))

        gray_pixels = 0
        total = w * h
        for y in range(0, h, 4):  # sample every 4px for speed
            for x in range(0, w, 4):
                if not _is_bw_pixel(*img.getpixel((x, y))):
                    gray_pixels += 1
        gray_ratio = gray_pixels / max(1, (total // 16))
        if gray_ratio > 0.02:
            results.append(
                CheckResult(
                    f"page_{i:03d}_bw",
                    False,
                    f"Page {i}: {gray_ratio:.1%} non-B&W pixels (max 2%)",
                )
            )
        else:
            results.append(CheckResult(f"page_{i:03d}_bw", True, f"Page {i} B&W check OK"))

        phash = imagehash.phash(art_crop)
        duplicate_of = None
        for existing_hash, existing_page in hashes:
            if phash - existing_hash < 2:
                duplicate_of = existing_page
                break
        if duplicate_of is not None:
            results.append(
                CheckResult(
                    f"page_{i:03d}_duplicate",
                    False,
                    f"Page {i} appears duplicate of page {duplicate_of}",
                )
            )
        else:
            hashes.append((phash, i))
            results.append(CheckResult(f"page_{i:03d}_duplicate", True, f"Page {i} uniqueness OK"))

    return results


def check_pdfs(book_id: str) -> list[CheckResult]:
    results: list[CheckResult] = []
    prod = book_data_dir(book_id) / "production"
    interior = prod / "interior.pdf"
    cover = prod / "cover.pdf"

    for label, path in [("interior_pdf", interior), ("cover_pdf", cover)]:
        if not path.exists():
            results.append(CheckResult(label, False, f"Missing {path}"))
        elif path.stat().st_size > 650 * 1024 * 1024:
            results.append(CheckResult(label, False, "PDF exceeds KDP 650MB limit"))
        else:
            results.append(CheckResult(label, True, f"{label} exists ({path.stat().st_size // 1024} KB)"))

    return results


def check_manifest(book_id: str, book: dict[str, Any]) -> list[CheckResult]:
    results: list[CheckResult] = []
    manifest = book_data_dir(book_id) / "app-bundle" / "manifest.yaml"
    if not manifest.exists():
        return [CheckResult("manifest", False, f"Missing manifest: {manifest}")]

    templates = book_data_dir(book_id) / "app-bundle" / "templates"
    art_count = book.get("art_page_count", 0)
    missing = [i for i in range(1, art_count + 1) if not (templates / f"{i:03d}.png").exists()]
    if missing:
        results.append(CheckResult("manifest_templates", False, f"Missing templates: {missing[:5]}..."))
    else:
        results.append(CheckResult("manifest_templates", True, f"All {art_count} templates present"))

    results.append(CheckResult("manifest", True, "App manifest exists"))
    return results


def run_preflight(book_id: str, require_pdfs: bool = True) -> PreflightReport:
    book = load_book(book_id)
    report = PreflightReport(book_id=book_id, passed=True)

    all_checks = [check_page_count(book)]
    all_checks.extend(check_art_files(book_id, book))
    if require_pdfs:
        all_checks.extend(check_pdfs(book_id))
    all_checks.extend(check_manifest(book_id, book))

    report.checks = all_checks
    report.passed = all(c.passed for c in all_checks if c.severity == "error")
    return report


def save_report(report: PreflightReport, book_id: str) -> Path:
    out = book_data_dir(book_id) / "production" / "qa-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return out
