"""Error envelope contracts for Adaptix services."""
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class ErrorCode(str, Enum):
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    CONFLICT = "conflict"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    CREDENTIAL_GATED = "credential_gated"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    VALIDATION_FAILED = "validation_failed"
    EXPORT_FAILED = "export_failed"
    ARTIFACT_UNAVAILABLE = "artifact_unavailable"
    NOT_CONFIGURED = "not_configured"
    INTERNAL_ERROR = "internal_error"


class ErrorEnvelope(BaseModel):
    error: str
    code: ErrorCode
    detail: Optional[str] = None
    field: Optional[str] = None
    correlation_id: Optional[str] = None
    tenant_id: Optional[str] = None


class CredentialGatedResponse(BaseModel):
    status: str = "credential_gated"
    provider: str
    reason: str
    configuration_required: str
    affected_features: list[str] = []
