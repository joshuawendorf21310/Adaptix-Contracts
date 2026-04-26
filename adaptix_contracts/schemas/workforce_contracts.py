"""Workforce/scheduling contracts shared across Adaptix services."""

from __future__ import annotations

import enum
from datetime import datetime, date, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ShiftStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AvailabilityType(str, enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    PREFERRED = "preferred"
    ON_CALL = "on_call"


class TimeOffStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"


class FatigueLevel(str, enum.Enum):
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class WorkforceShiftContract(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    minimum_staff: int = 1
    status: ShiftStatus = ShiftStatus.DRAFT
    created_at: datetime
    updated_at: Optional[datetime] = None


class WorkforceShiftAssignmentContract(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    user_id: UUID
    role: Optional[str] = None
    status: str = "assigned"
    assigned_at: datetime


class WorkforceAvailabilityContract(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    day_of_week: Optional[int] = None
    specific_date: Optional[date] = None
    start_time: time
    end_time: time
    availability_type: AvailabilityType
    created_at: datetime


class WorkforceTimeOffContract(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: TimeOffStatus = TimeOffStatus.PENDING
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime


class WorkforceFatigueEventContract(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    hours_worked_last_24: float
    hours_worked_last_48: float
    fatigue_level: FatigueLevel
    restriction_applied: bool = False
    restriction_reason: Optional[str] = None
    created_at: datetime


class WorkforceReadinessContract(BaseModel):
    tenant_id: UUID
    shift_id: Optional[UUID] = None
    total_required: int
    total_assigned: int
    total_available: int
    coverage_percentage: float
    fatigue_flagged_count: int = 0
    snapshot_at: datetime


class WorkforceShiftCreatedEvent(BaseModel):
    shift_id: UUID
    tenant_id: UUID
    start_time: datetime
    end_time: datetime
    status: ShiftStatus
    created_at: datetime


class WorkforceShiftAssignedEvent(BaseModel):
    shift_id: UUID
    user_id: UUID
    tenant_id: UUID
    assigned_at: datetime


class WorkforceFatigueAlertEvent(BaseModel):
    user_id: UUID
    tenant_id: UUID
    fatigue_level: FatigueLevel
    hours_worked_last_24: float
    created_at: datetime
