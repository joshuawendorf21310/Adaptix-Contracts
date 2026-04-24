"""Shared structured error response contracts for Adaptix services."""

from __future__ import annotations

from enum import Enum
from typing import Any


class ErrorCode(str, Enum):
    """Stable machine-readable error codes used across Adaptix APIs."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTH_INVALID = "AUTH_INVALID"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def make_error_response(
    *,
    code: ErrorCode | str,
    message: str,
    details: dict[str, Any] | None,
    trace_id: str,
) -> dict[str, Any]:
    """Build the canonical Adaptix error response envelope."""

    resolved_code = code.value if isinstance(code, ErrorCode) else str(code)
    return {
        "error": {
            "code": resolved_code,
            "message": message,
            "details": details or {},
            "trace_id": trace_id,
        }
    }