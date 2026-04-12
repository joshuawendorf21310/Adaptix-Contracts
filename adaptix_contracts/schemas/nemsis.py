"""NEMSIS response schemas (Phase 2 submission, Phase 3.6 validation/export).

Pydantic v2 response models for NEMSIS submission, validation, readiness,
and export endpoints. These are shared contracts between backend (epcr/) and
frontend (ePCR UI), ensuring type-safe integration.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NemsisStatusHistoryEntry(BaseModel):
    status: str
    timestamp: str
    actor: str | None = None
    notes: str | None = None


class NemsisSubmissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    chart_id: str
    tenant_id: str
    status: str
    attempt_number: int = 1
    xml_s3_key: str | None = None
    xml_sha256: str | None = None
    ack_s3_key: str | None = None
    response_s3_key: str | None = None
    status_history: list[NemsisStatusHistoryEntry] = []
    rejection_reasons: list[str] = []
    created_at: str | None = None
    updated_at: str | None = None


class NemsisSubmissionListResponse(BaseModel):
    submissions: list[NemsisSubmissionResponse]
    chart_id: str
    total: int


class BlockerDetail(BaseModel):
    """A single validation blocker, warning, or info message.
    
    Used in validation responses to communicate issues that must be
    resolved before export can be generated.
    """
    model_config = ConfigDict(from_attributes=True)

    type: str
    field: str
    message: str
    jump_target: str | None = None


class ValidationResponse(BaseModel):
    """Response from POST /api/v1/epcr/nemsis/validate.
    
    Validates a chart for NEMSIS compliance, returning:
    - valid: whether chart meets all compliance requirements
    - blockers: list of issues preventing export
    - warnings: list of non-blocking issues
    - timestamp: when validation was performed
    """
    model_config = ConfigDict(from_attributes=True)

    valid: bool
    chart_id: str
    state_code: str
    mapped_elements: int
    blockers: list[BlockerDetail] = []
    warnings: list[BlockerDetail] = []
    timestamp: str


class ReadinessResponse(BaseModel):
    """Response from GET /api/v1/epcr/nemsis/readiness.
    
    Indicates whether a chart is ready for export generation.
    A chart is ready if validation passes with no blockers.
    """
    model_config = ConfigDict(from_attributes=True)

    chart_id: str
    ready_for_export: bool
    blockers: list[BlockerDetail] = []
    warnings: list[BlockerDetail] = []
    mapped_elements: int


class ExportStatusResponse(BaseModel):
    """Response from GET /api/v1/epcr/nemsis/export/{export_id}.
    
    Provides status and metadata for a single export attempt.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    chart_id: str
    status: str
    created_at: str
    submitted_at: str | None = None
    blocker_count: int
    warning_count: int
    failure_reason: str | None = None


class ExportPreviewResponse(BaseModel):
    """Response from GET /api/v1/epcr/nemsis/export-preview.
    
    Previews export feasibility before generation, showing estimated
    payload size and whether blockers would prevent export.
    """
    model_config = ConfigDict(from_attributes=True)

    chart_id: str
    nemsis_version: str
    state_dataset: str | None = None
    mapped_elements: int
    blockers: list[BlockerDetail] = []
    warnings: list[BlockerDetail] = []
    can_export: bool
    estimated_xml_size_bytes: int


class MappingSummaryResponse(BaseModel):
    """Response from GET /api/v1/epcr/nemsis/mapping-summary.
    
    Summarizes mapping coverage by NEMSIS section and mapping status.
    """
    model_config = ConfigDict(from_attributes=True)

    chart_id: str
    total_mappings: int
    by_section: dict[str, int] = {}
    by_status: dict[str, int] = {}


class ExportHistoryResponse(BaseModel):
    """Response from GET /api/v1/epcr/nemsis/export-history.
    
    Provides list of all export attempts for a chart, newest first.
    """
    model_config = ConfigDict(from_attributes=True)

    chart_id: str
    exports: list[ExportStatusResponse] = []
    total: int


class ExportGenerationResponse(BaseModel):
    """Response from POST /api/v1/epcr/nemsis/export-generate.
    
    Authoritative outcome of an export generation attempt.
    Provides explicit status, blocker info, and success/failure details.
    Frontend must not infer success from XML presence; must use 'success' flag.
    """
    model_config = ConfigDict(from_attributes=True)

    chart_id: str
    success: bool
    blocked: bool
    export_id: int | None = None
    status: str
    blocker_count: int
    warning_count: int
    message: str
    failure_reason: str | None = None

