"""NEMSIS 3.5.1 export lifecycle contracts.

Defines the complete, typed export attempt lifecycle with state, failure classification,
and readiness snapshots.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ExportLifecycleStatus(str, Enum):
    BLOCKED = "blocked"
    GENERATION_REQUESTED = "generation_requested"
    GENERATION_IN_PROGRESS = "generation_in_progress"
    GENERATION_SUCCEEDED = "generation_succeeded"
    GENERATION_FAILED = "generation_failed"


class ExportFailureType(str, Enum):
    NONE = "none"
    READINESS_BLOCKED = "readiness_blocked"
    VALIDATION_ERROR = "validation_error"
    GENERATION_ERROR = "generation_error"
    STORAGE_ERROR = "storage_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class ExportTriggerSource(str, Enum):
    CHART = "chart"
    READINESS_PAGE = "readiness_page"
    OPERATOR_PANEL = "operator_panel"
    MANUAL_RETRY = "manual_retry"
    SYSTEM_RETRY = "system_retry"
    API = "api"


class ExportReadinessSnapshot(BaseModel):
    ready_for_export: bool
    blocker_count: int
    warning_count: int

    compliance_percentage: float | None = None
    missing_mandatory_fields: list[str] = Field(default_factory=list)


class ExportArtifactMetadata(BaseModel):
    file_name: str | None = None
    mime_type: str | None = None
    size_bytes: int | None = None
    storage_key: str | None = None
    checksum_sha256: str | None = None


class ExportAttemptSummary(BaseModel):
    export_id: int
    chart_id: str

    status: ExportLifecycleStatus
    failure_type: ExportFailureType = ExportFailureType.NONE

    message: str
    trigger_source: ExportTriggerSource

    retry_count: int = 0

    created_at: datetime
    updated_at: datetime


class ExportAttemptDetail(BaseModel):
    export_id: int
    chart_id: str
    tenant_id: str

    status: ExportLifecycleStatus
    failure_type: ExportFailureType = ExportFailureType.NONE

    message: str
    failure_reason: str | None = None

    trigger_source: ExportTriggerSource
    retry_count: int = 0

    supersedes_export_id: int | None = None
    superseded_by_export_id: int | None = None

    readiness_snapshot: ExportReadinessSnapshot
    artifact: ExportArtifactMetadata | None = None

    created_at: datetime
    updated_at: datetime

    requested_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class GenerateExportRequest(BaseModel):
    chart_id: str
    state_dataset: str | None = None
    trigger_source: ExportTriggerSource = ExportTriggerSource.CHART
    allow_retry_of_failed_attempt: bool = True


class GenerateExportResponse(BaseModel):
    export_id: int
    chart_id: str

    success: bool
    blocked: bool

    status: ExportLifecycleStatus
    failure_type: ExportFailureType = ExportFailureType.NONE

    message: str
    failure_reason: str | None = None

    retry_count: int = 0

    readiness_snapshot: ExportReadinessSnapshot
    artifact: ExportArtifactMetadata | None = None

    created_at: datetime
    updated_at: datetime


class ExportHistoryResponse(BaseModel):
    chart_id: str
    total_count: int
    limit: int
    offset: int

    exports: list[ExportAttemptSummary]


class ExportDetailResponse(BaseModel):
    export: ExportAttemptDetail


class RetryExportRequest(BaseModel):
    trigger_source: ExportTriggerSource = ExportTriggerSource.MANUAL_RETRY


class RetryExportResponse(BaseModel):
    original_export_id: int
    new_export_id: int

    success: bool
    blocked: bool

    status: ExportLifecycleStatus
    failure_type: ExportFailureType = ExportFailureType.NONE

    message: str
    failure_reason: str | None = None

    retry_count: int

    readiness_snapshot: ExportReadinessSnapshot

    created_at: datetime
    updated_at: datetime
