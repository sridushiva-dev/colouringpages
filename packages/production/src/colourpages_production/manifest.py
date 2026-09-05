"""App bundle manifest export."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from .catalog import load_book
from .config import book_data_dir


from .placeholders import _page_definitions


def export_manifest(book_id: str) -> Path:
    book = load_book(book_id)
    bundle_dir = book_data_dir(book_id) / "app-bundle"
    templates_dir = bundle_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    laid_out = book_data_dir(book_id) / "art" / "laid-out"
    pages_out = []
    for page in _page_definitions(book):
        num = page["number"]
        src = laid_out / f"{num:03d}.png"
        dst = templates_dir / f"{num:03d}.png"
        if src.exists():
            shutil.copy2(src, dst)
        pages_out.append(
            {
                "number": num,
                "template": f"templates/{num:03d}.png",
                "prompt": page.get("prompt", ""),
                "challenge": page.get("challenge"),
                "subject": page.get("subject"),
            }
        )

    manifest = {
        "book_id": book_id,
        "title": book.get("title"),
        "subtitle": book.get("subtitle"),
        "line": book.get("line"),
        "edition": book.get("app", {}).get("edition", "2026-01"),
        "qr_url": book.get("app", {}).get("qr_url", f"https://colourpages.app/b/{book_id}"),
        "target_audience": book.get("target_audience"),
        "pages": pages_out,
    }

    out = bundle_dir / "manifest.yaml"
    with out.open("w", encoding="utf-8") as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return out
