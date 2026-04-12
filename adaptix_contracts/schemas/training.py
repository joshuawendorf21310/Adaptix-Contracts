"""Training domain response schemas.

Pydantic v2 request/response models for training course and
completion-record endpoints.
"""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from adaptix_contracts.types.enums import TrainingType


# ── Course Catalog ────────────────────────────────────────────────────────────


class TrainingCourseCreateRequest(BaseModel):
    """Request to create a training course definition."""

    course_name: str = Field(min_length=1, max_length=255)
    training_type: TrainingType
    description: str | None = Field(default=None, max_length=2000)
    duration_hours: float | None = Field(default=None, ge=0)
    required: bool = False
    renewal_months: int | None = Field(default=None, ge=1, le=120)


class TrainingCourseResponse(BaseModel):
    """Training course response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    course_name: str
    training_type: TrainingType
    description: str | None
    duration_hours: float | None
    required: bool
    renewal_months: int | None
    active: bool
    created_at: datetime
    updated_at: datetime


class TrainingCourseListResponse(BaseModel):
    """Paginated training course list."""

    items: list[TrainingCourseResponse]
    total: int


# ── Completion Records ────────────────────────────────────────────────────────


class TrainingCompletionCreateRequest(BaseModel):
    """Request to record a training completion."""

    user_id: UUID
    course_id: UUID
    completed_at: datetime
    score: float | None = Field(default=None, ge=0, le=100)
    certificate_url: str | None = Field(default=None, max_length=2048)
    expires_at: date | None = None


class TrainingCompletionResponse(BaseModel):
    """Training completion record response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    user_id: UUID
    course_id: UUID
    course_name: str
    completed_at: datetime
    score: float | None
    certificate_url: str | None
    expires_at: date | None
    created_at: datetime


class TrainingCompletionListResponse(BaseModel):
    """Paginated training completion list."""

    items: list[TrainingCompletionResponse]
    total: int


# ── Compliance Summary ────────────────────────────────────────────────────────


class TrainingComplianceSummary(BaseModel):
    """Training compliance overview for a personnel member."""

    user_id: UUID
    total_required: int
    total_completed: int
    compliance_pct: float
    overdue_courses: list[str] = Field(default_factory=list)
    expiring_soon: list[str] = Field(default_factory=list)
