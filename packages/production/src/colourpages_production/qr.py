"""QR code generation for book covers."""

from __future__ import annotations

from pathlib import Path

import qrcode
from PIL import Image


def generate_qr(url: str, size_px: int = 400) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((size_px, size_px), Image.Resampling.NEAREST)


def save_qr(url: str, path: Path, size_px: int = 400) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    generate_qr(url, size_px).save(path)
    return path
