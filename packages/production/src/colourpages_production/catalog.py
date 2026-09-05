"""Catalog loading and persistence."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from .config import catalog_path


def load_book(book_id: str) -> dict[str, Any]:
    path = catalog_path(book_id)
    if not path.exists():
        raise FileNotFoundError(f"Book catalog not found: {path}")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data.get("id") != book_id:
        raise ValueError(f"Catalog id mismatch: expected {book_id}, got {data.get('id')}")
    return data


def save_book(book: dict[str, Any]) -> Path:
    book_id = book["id"]
    path = catalog_path(book_id)
    book["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(book, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return path


def log_agent_action(book: dict[str, Any], agent: str, message: str) -> None:
    book.setdefault("agent_log", []).append(
        {
            "agent": agent,
            "at": datetime.now(timezone.utc).isoformat(),
            "message": message,
        }
    )
