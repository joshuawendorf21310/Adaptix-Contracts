"""Personnel domain response schemas.

Pydantic v2 request/response models for personnel lifecycle endpoints
(create, deactivate, certifications, roster).
"""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ── Personnel CRUD ────────────────────────────────────────────────────────────


class PersonnelCreateRequest(BaseModel):
    """Request to create a new personnel record."""

    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    role: str = Field(min_length=1, max_length=64)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    hire_date: date | None = None
    certifications: list[str] = Field(default_factory=list)


class PersonnelUpdateRequest(BaseModel):
    """Request to update an existing personnel record."""

    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, min_length=1, max_length=120)
    role: str | None = Field(default=None, min_length=1, max_length=64)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    certifications: list[str] | None = None


class PersonnelDeactivateRequest(BaseModel):
    """Request to deactivate a personnel member."""

    reason: str = Field(min_length=1, max_length=500)
    effective_date: date | None = None


class PersonnelResponse(BaseModel):
    """Full personnel record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    user_id: UUID
    first_name: str
    last_name: str
    role: str
    email: str | None
    phone: str | None
    hire_date: date | None
    certifications: list[str]
    active: bool
    deactivated_at: datetime | None = None
    deactivation_reason: str | None = None
    created_at: datetime
    updated_at: datetime


class PersonnelListResponse(BaseModel):
    """Paginated personnel list."""

    items: list[PersonnelResponse]
    total: int


# ── Roster ────────────────────────────────────────────────────────────────────


class RosterEntryResponse(BaseModel):
    """A single roster entry linking personnel to a unit/shift."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    personnel_id: UUID
    unit_id: UUID | None
    shift_id: UUID | None
    role: str
    active: bool
    created_at: datetime
    updated_at: datetime


class RosterListResponse(BaseModel):
    """Paginated roster list."""

    items: list[RosterEntryResponse]
    total: int
