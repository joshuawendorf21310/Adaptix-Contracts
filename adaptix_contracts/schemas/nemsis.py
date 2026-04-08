"""NEMSIS submission response schemas (Phase 2, T217).

Pydantic v2 response models for NEMSIS state submission endpoints.
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
