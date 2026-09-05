"""Page layout: prompt banners + art placement."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .catalog import load_book
from .config import (
    PROMPT_BANNER_RATIO,
    PROMPT_FOOTER_RATIO,
    book_data_dir,
    page_spec,
)
from .placeholders import _page_definitions


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def layout_page(
    art: Image.Image,
    prompt: str,
    challenge: str | None,
    spec_width: int,
    spec_height: int,
) -> Image.Image:
    canvas = Image.new("RGB", (spec_width, spec_height), "white")
    draw = ImageDraw.Draw(canvas)

    banner_h = int(spec_height * PROMPT_BANNER_RATIO)
    footer_h = int(spec_height * PROMPT_FOOTER_RATIO) if challenge else 0
    art_top = banner_h
    art_bottom = spec_height - footer_h

    # Banner background
    draw.rectangle([0, 0, spec_width, banner_h], fill="#F5F5F5")
    draw.line([0, banner_h, spec_width, banner_h], fill="#000000", width=2)

    font_prompt = _get_font(max(14, spec_width // 55))
    font_label = _get_font(max(12, spec_width // 65))

    draw.text((20, 8), "PROMPT:", fill="#000000", font=font_label)
    draw.text((20, 8 + font_label.size + 4), prompt, fill="#000000", font=font_prompt)

    # Fit art in remaining area with margin
    margin = int(spec_width * 0.05)
    art_w = spec_width - 2 * margin
    art_h = art_bottom - art_top - 2 * margin
    art_resized = art.copy().convert("RGB")
    art_resized.thumbnail((art_w, art_h), Image.Resampling.LANCZOS)
    ax = margin + (art_w - art_resized.width) // 2
    ay = art_top + margin + (art_h - art_resized.height) // 2
    canvas.paste(art_resized, (ax, ay))

    if challenge and footer_h > 0:
        draw.line([0, art_bottom, spec_width, art_bottom], fill="#000000", width=1)
        draw.text((20, art_bottom + 6), f"CHALLENGE: {challenge}", fill="#000000", font=font_label)

    return canvas


def run_layout(book_id: str) -> list[Path]:
    book = load_book(book_id)
    spec = page_spec(book["trim"], book.get("kdp", {}).get("bleed", False))
    raw_dir = book_data_dir(book_id) / "art" / "raw"
    out_dir = book_data_dir(book_id) / "art" / "laid-out"
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[Path] = []
    for page in _page_definitions(book):
        num = page["number"]
        raw_path = raw_dir / f"{num:03d}.png"
        if not raw_path.exists():
            continue
        art = Image.open(raw_path)
        laid = layout_page(
            art,
            page.get("prompt", ""),
            page.get("challenge"),
            spec.width_px,
            spec.height_px,
        )
        out = out_dir / f"{num:03d}.png"
        laid.save(out, dpi=(300, 300))
        outputs.append(out)

    return outputs
