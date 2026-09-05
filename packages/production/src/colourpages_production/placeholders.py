"""Generate placeholder line art for pipeline testing."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from .catalog import load_book
from .config import book_data_dir, page_spec


def _placeholder_art(width: int, height: int, label: str, seed: int = 0) -> Image.Image:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    margin = int(min(width, height) * (0.08 + (seed % 5) * 0.01))
    draw.rectangle(
        [margin, margin, width - margin, height - margin],
        outline="black",
        width=2 + (seed % 3),
    )
    # Vary inner shapes per page so perceptual hash differs
    cx = width // 2 + (seed % 7 - 3) * (width // 20)
    cy = height // 2 + (seed % 5 - 2) * (height // 20)
    rx = width // 4 + (seed % 4) * (width // 40)
    ry = height // 4 + (seed % 3) * (height // 40)
    if seed % 3 == 0:
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline="black", width=2)
    elif seed % 3 == 1:
        draw.polygon(
            [(cx, cy - ry), (cx + rx, cy + ry), (cx - rx, cy + ry)],
            outline="black",
        )
    else:
        draw.arc([cx - rx, cy - ry, cx + rx, cy + ry], 0, 270, fill="black", width=2)
    for i in range(seed % 4):
        x = margin + (i + 1) * (width - 2 * margin) // 5
        draw.line([x, margin, x, height - margin], fill="black", width=1)
    draw.text((width // 2 - 20, height // 2 - 10), str(seed), fill="black")
    draw.text((width // 2 - 60, height - margin - 20), label[:24], fill="black")
    return img


def _page_definitions(book: dict) -> list[dict]:
    """Return page defs for 1..art_page_count, merging catalog entries."""
    art_count = book.get("art_page_count", len(book.get("pages", [])))
    by_num = {p["number"]: p for p in book.get("pages", [])}
    pages: list[dict] = []
    for i in range(1, art_count + 1):
        if i in by_num:
            pages.append(by_num[i])
        else:
            pages.append(
                {
                    "number": i,
                    "subject": f"Monument scene {i}",
                    "prompt": f"Reimagine this monument in a surprising new way (page {i}).",
                    "challenge": "Add one hidden detail only you would think of.",
                }
            )
    return pages


def generate_placeholders(book_id: str) -> list[Path]:
    book = load_book(book_id)
    spec = page_spec(book["trim"], book.get("kdp", {}).get("bleed", False))
    raw_dir = book_data_dir(book_id) / "art" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    art_w = int(spec.width_px * 0.85)
    art_h = int(spec.height_px * 0.75)

    outputs: list[Path] = []
    for page in _page_definitions(book):
        num = page["number"]
        subject = page.get("subject", f"Page {num}")
        img = _placeholder_art(art_w, art_h, subject, seed=num)
        out = raw_dir / f"{num:03d}.png"
        img.save(out, dpi=(300, 300))
        outputs.append(out)

    return outputs
