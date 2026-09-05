"""KDP print configuration and dimension helpers."""

from __future__ import annotations

from dataclasses import dataclass

DPI = 300
BLEED_INCHES = 0.125
OUTSIDE_MARGIN_INCHES = 0.25
GUTTER_MARGIN_INCHES = 0.375  # 24-150 pages
PROMPT_BANNER_RATIO = 0.12
PROMPT_FOOTER_RATIO = 0.05

TRIM_SIZES_INCHES: dict[str, tuple[float, float]] = {
    "8.5x11": (8.5, 11.0),
    "8.5x8.5": (8.5, 8.5),
}


@dataclass(frozen=True)
class PageSpec:
    trim_key: str
    width_in: float
    height_in: float
    bleed: bool

    @property
    def width_px(self) -> int:
        w = self.width_in + (BLEED_INCHES * 2 if self.bleed else 0)
        return int(round(w * DPI))

    @property
    def height_px(self) -> int:
        h = self.height_in + (BLEED_INCHES * 2 if self.bleed else 0)
        return int(round(h * DPI))

    @property
    def margin_px(self) -> int:
        margin = OUTSIDE_MARGIN_INCHES + (BLEED_INCHES if self.bleed else 0)
        return int(round(margin * DPI))

    @property
    def gutter_px(self) -> int:
        return int(round(GUTTER_MARGIN_INCHES * DPI))


def page_spec(trim: str, bleed: bool = False) -> PageSpec:
    if trim not in TRIM_SIZES_INCHES:
        raise ValueError(f"Unknown trim size: {trim}")
    w, h = TRIM_SIZES_INCHES[trim]
    return PageSpec(trim_key=trim, width_in=w, height_in=h, bleed=bleed)


def workspace_root() -> "Path":
    from pathlib import Path

    # packages/production/src/colourpages_production/config.py -> repo root
    return Path(__file__).resolve().parents[4]


def book_data_dir(book_id: str) -> "Path":
    return workspace_root() / "data" / "books" / book_id


def catalog_path(book_id: str) -> "Path":
    return workspace_root() / "catalog" / "books" / f"{book_id}.yaml"
