"""Workforce contracts for Adaptix platform."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class FatigueRiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class StaffStatus(str, Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    RESTRICTED = "restricted"
    RETURN_TO_DUTY = "return_to_duty"
    INACTIVE = "inactive"


class StaffProfile(BaseModel):
    """Staff profile contract."""
    staff_id: str
    tenant_id: str
    name: str
    role: str
    certifications: list[str] = []
    status: StaffStatus = StaffStatus.ACTIVE
    unit_assignment: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FatigueAssessment(BaseModel):
    """Fatigue risk assessment for a staff member."""
    assessment_id: str
    staff_id: str
    tenant_id: str
    risk_level: FatigueRiskLevel
    hours_worked_last_24h: float
    hours_worked_last_7d: float
    consecutive_shifts: int
    risk_factors: list[str] = []
    recommendation: Optional[str] = None
    human_review_required: bool = True
    supervisor_review_flag: bool = False
    assessed_at: datetime
    ai_generated: bool = False


class StaffRestriction(BaseModel):
    """Staff restriction record."""
    restriction_id: str
    staff_id: str
    tenant_id: str
    actor_id: str
    reason: str
    restriction_type: str
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    supervisor_id: Optional[str] = None
    audit_event_emitted: bool = True
    created_at: datetime


class ReturnToDutyRecord(BaseModel):
    """Return to duty record."""
    record_id: str
    staff_id: str
    tenant_id: str
    actor_id: str
    cleared_by: str
    clearance_notes: Optional[str] = None
    return_datetime: datetime
    audit_event_emitted: bool = True
    created_at: datetime


class WorkforceAvailability(BaseModel):
    """Workforce availability for CAD/CrewLink linkage."""
    tenant_id: str
    date: str
    shift_type: str
    available_staff: list[str] = []
    unavailable_staff: list[str] = []
    restricted_staff: list[str] = []
    coverage_adequate: bool = True
    fatigue_risk_flags: list[str] = []
    cad_linkage_active: bool = True
    crewlink_linkage_active: bool = True
