"""Standardized error response schemas for the Adaptix API."""
from __future__ import annotations

import enum
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class ErrorCode(str, enum.Enum):
    """Canonical error codes returned in API error responses."""

    # Authentication / Authorization
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_FORBIDDEN = "AUTH_FORBIDDEN"

    # Tenant
    TENANT_NOT_FOUND = "TENANT_NOT_FOUND"

    # Validation
    VALIDATION_FAILED = "VALIDATION_FAILED"

    # Integration / Circuit breaker
    INTEGRATION_UNAVAILABLE = "INTEGRATION_UNAVAILABLE"
    CIRCUIT_OPEN = "CIRCUIT_OPEN"

    # Rate limiting
    RATE_LIMITED = "RATE_LIMITED"

    # PHI access
    PHI_LOCKED = "PHI_LOCKED"

    # Generic CRUD
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"

    # Catch-all
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorDetail(BaseModel):
    """Field-level validation error detail."""

    field: str = Field(..., description="JSONPath-style field reference (e.g. 'body.email')")
    message: str = Field(..., description="Human-readable description of the error")
    code: str | None = Field(None, description="Machine-readable sub-code (e.g. 'min_length')")


class ErrorResponse(BaseModel):
    """Standardized top-level error envelope returned by all API error paths."""

    error: ErrorCode = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable summary")
    request_id: str | None = Field(None, description="Correlation / trace ID for support")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    details: dict[str, Any] | None = Field(None, description="Additional context (non-PHI)")

    model_config = {"json_schema_extra": {"examples": [
        {
            "error": "NOT_FOUND",
            "message": "Incident 00000000-0000-0000-0000-000000000000 not found.",
            "request_id": "req_abc123",
            "timestamp": "2026-04-04T00:00:00Z",
            "details": None,
        },
    ]}}


class ValidationErrorResponse(BaseModel):
    """Returned on request validation failures (422)."""

    error: ErrorCode = Field(default=ErrorCode.VALIDATION_FAILED)
    message: str = Field(default="Request validation failed")
    request_id: str | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    errors: list[ErrorDetail] = Field(default_factory=list, description="Per-field error list")
