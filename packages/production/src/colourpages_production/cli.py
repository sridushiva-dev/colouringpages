"""CLI entry points."""

from __future__ import annotations

import json
import sys

import click

from .build import build_book, sync_catalog_to_api_store
from .layout import run_layout
from .placeholders import generate_placeholders
from .preflight import run_preflight, save_report


@click.command("preflight")
@click.option("--book-id", required=True)
@click.option("--no-pdf", is_flag=True, help="Skip PDF existence checks")
def preflight_cmd(book_id: str, no_pdf: bool) -> None:
    """Run KDP preflight checks on a book."""
    report = run_preflight(book_id, require_pdfs=not no_pdf)
    path = save_report(report, book_id)
    click.echo(json.dumps(report.to_dict(), indent=2))
    click.echo(f"\nReport saved: {path}")
    sys.exit(0 if report.passed else 1)


@click.command("build")
@click.option("--book-id", required=True)
@click.option("--placeholders", is_flag=True, help="Generate placeholder art for testing")
def build_cmd(book_id: str, placeholders: bool) -> None:
    """Build full publish package for a book."""
    result = build_book(book_id, use_placeholders=placeholders)
    sync_catalog_to_api_store(book_id)
    click.echo(json.dumps(result, indent=2))
    sys.exit(0 if result["preflight_passed"] else 1)


@click.command("layout")
@click.option("--book-id", required=True)
def layout_cmd(book_id: str) -> None:
    """Apply prompt layout to raw art pages."""
    paths = run_layout(book_id)
    click.echo(f"Laid out {len(paths)} pages")


@click.command("placeholders")
@click.option("--book-id", required=True)
def placeholders_cmd(book_id: str) -> None:
    """Generate placeholder art for pipeline testing."""
    paths = generate_placeholders(book_id)
    click.echo(f"Generated {len(paths)} placeholder pages")
