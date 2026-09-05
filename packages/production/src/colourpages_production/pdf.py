"""PDF assembly for KDP interior and cover."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from .catalog import load_book
from .config import DPI, book_data_dir, page_spec
from .qr import generate_qr


def _blank_page(spec_width: int, spec_height: int) -> Image.Image:
    return Image.new("RGB", (spec_width, spec_height), "white")


def build_interior_pdf(book_id: str) -> Path:
    book = load_book(book_id)
    spec = page_spec(book["trim"], book.get("kdp", {}).get("bleed", False))
    laid_out = book_data_dir(book_id) / "art" / "laid-out"
    out = book_data_dir(book_id) / "production" / "interior.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    art_count = book.get("art_page_count", len(book.get("pages", [])))
    page_w = spec.width_in * inch
    page_h = spec.height_in * inch

    c = canvas.Canvas(str(out), pagesize=(page_w, page_h))

    for i in range(1, art_count + 1):
        art_path = laid_out / f"{i:03d}.png"
        if art_path.exists():
            c.drawImage(ImageReader(str(art_path)), 0, 0, width=page_w, height=page_h)
        c.showPage()
        # Blank back for single-sided coloring
        c.showPage()

    # Pad to target page count with blank pages if needed
    current = art_count * 2
    target = book.get("page_count", current)
    while current < target:
        c.showPage()
        current += 1

    c.save()
    return out


def build_cover_pdf(book_id: str) -> Path:
    book = load_book(book_id)
    spec = page_spec(book["trim"], bleed=True)  # covers require bleed
    out = book_data_dir(book_id) / "production" / "cover.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    art_count = book.get("art_page_count", 25)
    page_count = book.get("page_count", art_count * 2)
    spine_in = page_count * 0.002252  # KDP formula for white paper

    back_w = spec.width_in
    front_w = spec.width_in
    bleed = 0.125
    total_w = bleed + back_w + spine_in + front_w + bleed
    total_h = spec.height_in + 2 * bleed

    c = canvas.Canvas(str(out), pagesize=(total_w * inch, total_h * inch))

    # Back cover (left)
    back_x = bleed * inch
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(back_x, bleed * inch, back_w * inch, spec.height_in * inch, fill=1, stroke=0)

    qr_url = book.get("app", {}).get("qr_url", f"https://colourpages.app/b/{book_id}")
    qr_img = generate_qr(qr_url, size_px=300)
    qr_path = book_data_dir(book_id) / "production" / "_qr_temp.png"
    qr_img.save(qr_path)
    qr_size = 1.2 * inch
    c.drawImage(
        ImageReader(str(qr_path)),
        back_x + back_w * inch - qr_size - 0.3 * inch,
        bleed * inch + 0.3 * inch,
        width=qr_size,
        height=qr_size,
    )
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 8)
    c.drawString(back_x + 0.3 * inch, bleed * inch + 0.3 * inch, "Scan to unlock digital pages")

    # Spine
    spine_x = (bleed + back_w) * inch
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.rect(spine_x, bleed * inch, spine_in * inch, spec.height_in * inch, fill=1, stroke=0)
    if page_count >= 79 and spine_in > 0.1:
        c.saveState()
        c.translate(spine_x + spine_in * inch / 2, bleed * inch + spec.height_in * inch / 2)
        c.rotate(90)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", min(10, int(spine_in * 72)))
        title = book.get("title", book_id)[:40]
        c.drawCentredString(0, 0, title)
        c.restoreState()

    # Front cover (right)
    front_x = (bleed + back_w + spine_in) * inch
    c.setFillColorRGB(1, 1, 1)
    c.rect(front_x, bleed * inch, front_w * inch, spec.height_in * inch, fill=1, stroke=0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 24)
    title = book.get("title", "Colouring Book")
    c.drawCentredString(front_x + front_w * inch / 2, bleed * inch + spec.height_in * inch * 0.55, title)
    c.setFont("Helvetica", 14)
    subtitle = book.get("subtitle", "")
    if subtitle:
        c.drawCentredString(front_x + front_w * inch / 2, bleed * inch + spec.height_in * inch * 0.45, subtitle)
    c.setFont("Helvetica", 10)
    c.drawCentredString(front_x + front_w * inch / 2, bleed * inch + 0.5 * inch, "ColourPages Press")

    c.save()
    if qr_path.exists():
        qr_path.unlink()
    return out
