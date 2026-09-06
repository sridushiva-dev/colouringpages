"""Full production build orchestration."""

from __future__ import annotations

import zipfile

import yaml

from .catalog import load_book, log_agent_action, save_book
from .config import book_data_dir, workspace_root
from .layout import run_layout
from .manifest import export_manifest
from .pdf import build_cover_pdf, build_interior_pdf
from .placeholders import generate_placeholders
from .preflight import run_preflight, save_report


def build_book(book_id: str, use_placeholders: bool = False) -> dict:
    book = load_book(book_id)
    data_dir = book_data_dir(book_id)
    data_dir.mkdir(parents=True, exist_ok=True)

    if use_placeholders:
        generate_placeholders(book_id)

    run_layout(book_id)
    build_interior_pdf(book_id)
    build_cover_pdf(book_id)
    export_manifest(book_id)

    report = run_preflight(book_id, require_pdfs=True)
    save_report(report, book_id)

    listing_dir = data_dir / "listing"
    listing_dir.mkdir(parents=True, exist_ok=True)
    listing_path = listing_dir / "kdp-metadata.yaml"
    listing_data = {
        "title": book.get("title"),
        "subtitle": book.get("subtitle"),
        "keywords": book.get("listing", {}).get("keywords", []),
        "description_html": book.get("listing", {}).get("description_html", ""),
        "ai_disclosure": book.get("ai_disclosure", {}),
        "kdp": book.get("kdp", {}),
        "trim": book.get("trim"),
        "page_count": book.get("page_count"),
    }
    listing_path.write_text(yaml.dump(listing_data, default_flow_style=False), encoding="utf-8")

    zip_path = _create_publish_zip(book_id)
    log_agent_action(book, "production", f"Build complete. Preflight passed={report.passed}")

    if report.passed:
        book["status"] = "AWAITING_PUBLISH_APPROVAL"
        book.setdefault("approvals", {})["publish"] = "pending"
        book.setdefault("pending_actions", []).append(
            {
                "type": "publish_approval",
                "created_at": book.get("updated_at"),
                "notes": "Publish package ready for Control Center review",
            }
        )
    else:
        book["status"] = "PRODUCTION"
        log_agent_action(
            book, "qa", f"Preflight failed with {sum(1 for c in report.checks if not c.passed)} issues"
        )

    save_book(book)

    return {
        "book_id": book_id,
        "preflight_passed": report.passed,
        "zip_path": str(zip_path),
        "qa_report": str(data_dir / "production" / "qa-report.json"),
    }


def _create_publish_zip(book_id: str):
    data_dir = book_data_dir(book_id)
    zip_path = data_dir / "publish-ready.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in [
            "production/interior.pdf",
            "production/cover.pdf",
            "production/qa-report.json",
            "listing/kdp-metadata.yaml",
            "app-bundle/manifest.yaml",
        ]:
            full = data_dir / rel
            if full.exists():
                zf.write(full, arcname=f"{book_id}/{rel}")
        templates = data_dir / "app-bundle" / "templates"
        if templates.exists():
            for t in sorted(templates.glob("*.png")):
                zf.write(t, arcname=f"{book_id}/app-bundle/templates/{t.name}")
    return zip_path


def sync_catalog_to_api_store(book_id: str) -> None:
    """Copy catalog state to admin data store."""
    import shutil

    store = workspace_root() / "apps" / "admin" / "data" / "books"
    store.mkdir(parents=True, exist_ok=True)
    src = workspace_root() / "catalog" / "books" / f"{book_id}.yaml"
    shutil.copy2(src, store / f"{book_id}.yaml")

    qa = book_data_dir(book_id) / "production" / "qa-report.json"
    if qa.exists():
        shutil.copy2(qa, store / f"{book_id}.qa.json")
