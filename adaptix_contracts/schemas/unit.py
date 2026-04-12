"""Unit domain response schemas.

Pydantic v2 request/response models for unit (apparatus) lifecycle and
status endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from adaptix_contracts.types.enums import CadUnitStatus


# ── Unit CRUD ─────────────────────────────────────────────────────────────────


class UnitCreateRequest(BaseModel):
    """Request to register a new unit/apparatus."""

    unit_identifier: str = Field(min_length=1, max_length=64)
    unit_type: str | None = Field(default=None, max_length=64)
    station_id: UUID | None = None
    capabilities: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class UnitUpdateRequest(BaseModel):
    """Request to update a unit record."""

    unit_identifier: str | None = Field(default=None, min_length=1, max_length=64)
    unit_type: str | None = Field(default=None, max_length=64)
    station_id: UUID | None = None
    capabilities: list[str] | None = None
    active: bool | None = None
    metadata: dict[str, Any] | None = None


class UnitResponse(BaseModel):
    """Full unit/apparatus response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    unit_identifier: str
    unit_type: str | None
    station_id: UUID | None
    capabilities: list[str]
    status: CadUnitStatus
    active: bool
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class UnitListResponse(BaseModel):
    """Paginated unit list."""

    items: list[UnitResponse]
    total: int


# ── Unit Status ───────────────────────────────────────────────────────────────


class UnitStatusChangeRequest(BaseModel):
    """Request to change a unit's operational status."""

    new_status: CadUnitStatus
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    reason: str | None = Field(default=None, max_length=255)


class UnitStatusHistoryEntry(BaseModel):
    """A single status-change record for audit trail."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    unit_id: UUID
    previous_status: CadUnitStatus
    new_status: CadUnitStatus
    changed_by: UUID | None
    reason: str | None
    changed_at: datetime


class UnitStatusHistoryResponse(BaseModel):
    """Paginated status history."""

    items: list[UnitStatusHistoryEntry]
    total: int
