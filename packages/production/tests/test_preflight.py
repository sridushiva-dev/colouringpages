"""Basic preflight tests."""

from colourpages_production.config import page_spec
from colourpages_production.preflight import check_page_count


def test_page_spec_dimensions():
    spec = page_spec("8.5x11", bleed=False)
    assert spec.width_px == 2550
    assert spec.height_px == 3300


def test_page_count_valid():
    book = {"page_count": 50}
    assert check_page_count(book).passed is True


def test_page_count_odd_fails():
    book = {"page_count": 25}
    assert check_page_count(book).passed is False
