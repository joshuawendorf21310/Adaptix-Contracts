from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class NerisValidationStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    DRAFT_INCOMPLETE = "DRAFT_INCOMPLETE"
    READY_FOR_VALIDATION = "READY_FOR_VALIDATION"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATION_WARNING = "VALIDATION_WARNING"
    VALIDATION_PASSED = "VALIDATION_PASSED"
    READY_FOR_EXPORT = "READY_FOR_EXPORT"
    EXPORTED = "EXPORTED"


class NerisRequiredFieldStatus(BaseModel):
    field_name: str
    present: bool
    source: str | None = None


class NerisValidationFinding(BaseModel):
    field_name: str
    severity: str
    code: str
    message: str


class NerisValidationResult(BaseModel):
    validation_id: str
    incident_id: str
    status: NerisValidationStatus
    findings: list[NerisValidationFinding] = Field(default_factory=list)
    normalized_findings: list[dict[str, str]] = Field(default_factory=list)
    validated_at: datetime | None = None


class NerisSubmissionReadiness(BaseModel):
    incident_id: str
    status: NerisValidationStatus
    missing_required_fields: list[str] = Field(default_factory=list)
    warning_fields: list[str] = Field(default_factory=list)


class NerisExportPackage(BaseModel):
    export_id: str
    incident_id: str
    status: NerisValidationStatus
    field_count: int
    payload: dict[str, object] = Field(default_factory=dict)
    created_at: datetime | None = None


class NerisIncidentMappingResult(BaseModel):
    incident_id: str
    mapped_fields: dict[str, object] = Field(default_factory=dict)
    missing_fields: list[str] = Field(default_factory=list)
    mapping_version: str = "fire-v1"


class NerisMappingAudit(BaseModel):
    incident_id: str
    source_service: str = "adaptix-fire"
    mapped_at: datetime
    source_attribution: list[str] = Field(default_factory=list)


__all__ = [
    "NerisExportPackage",
    "NerisIncidentMappingResult",
    "NerisMappingAudit",
    "NerisRequiredFieldStatus",
    "NerisSubmissionReadiness",
    "NerisValidationFinding",
    "NerisValidationResult",
    "NerisValidationStatus",
]