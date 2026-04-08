"""
Adaptix Contracts — Role claim utilities v0.1.0

Extracted from core_app.security. No external dependencies.
"""
from __future__ import annotations

from typing import Any


def _stringify_claim(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    return str(value)


def normalize_role_claims(
    primary_role: Any = None,
    role: Any = None,
    roles: Any = None,
) -> list[str]:
    """Normalize heterogeneous role claim inputs into a deduplicated ordered list."""
    normalized: list[str] = []

    if isinstance(roles, (list, tuple, set)):
        for candidate in roles:
            text = _stringify_claim(candidate)
            if text and text not in normalized:
                normalized.append(text)

    for candidate in (primary_role, role):
        text = _stringify_claim(candidate)
        if text and text not in normalized:
            normalized.insert(0, text)

    return normalized
