"""Adaptix Scheduling — Core Shared Models (Pydantic contracts)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class ScheduleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ShiftStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class AssignmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class TimeOffStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"


class OvertimeStatus(str, Enum):
    OFFERED = "offered"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


class SwapStatus(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"


class HoldoverStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Core Scheduling Models
# ---------------------------------------------------------------------------

class Schedule(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    description: Optional[str] = None
    agency_type: str  # ems, fire, law_enforcement, dispatch, corrections
    status: ScheduleStatus = ScheduleStatus.DRAFT
    start_date: datetime
    end_date: datetime
    created_by: UUID
    updated_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    correlation_id: Optional[str] = None


class ShiftTemplate(BaseModel):
    id: UUID
    tenant_id: UUID
    schedule_id: UUID
    name: str
    agency_type: str
    start_time: str  # HH:MM
    end_time: str    # HH:MM
    duration_hours: float
    recurrence_rule: Optional[str] = None  # iCal RRULE
    minimum_staff: int = 1
    required_ranks: List[str] = Field(default_factory=list)
    required_specialties: List[str] = Field(default_factory=list)
    station_id: Optional[UUID] = None
    beat_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class ShiftInstance(BaseModel):
    id: UUID
    tenant_id: UUID
    template_id: Optional[UUID] = None
    schedule_id: UUID
    agency_type: str
    shift_date: datetime
    start_time: datetime
    end_time: datetime
    status: ShiftStatus = ShiftStatus.OPEN
    minimum_staff: int = 1
    station_id: Optional[UUID] = None
    beat_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    notes: Optional[str] = None
    created_by: UUID
    updated_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    correlation_id: Optional[str] = None
    audit_event_id: Optional[UUID] = None


class ShiftAssignment(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    person_id: UUID
    person_name: str
    rank: Optional[str] = None
    specialty: Optional[str] = None
    status: AssignmentStatus = AssignmentStatus.CONFIRMED
    assigned_by: UUID
    assigned_at: datetime
    unassigned_by: Optional[UUID] = None
    unassigned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class AvailabilityWindow(BaseModel):
    id: UUID
    tenant_id: UUID
    person_id: UUID
    start_time: datetime
    end_time: datetime
    available: bool = True
    reason: Optional[str] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class TimeOffRequest(BaseModel):
    id: UUID
    tenant_id: UUID
    person_id: UUID
    start_date: datetime
    end_date: datetime
    reason: Optional[str] = None
    status: TimeOffStatus = TimeOffStatus.PENDING
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    denial_reason: Optional[str] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class OvertimeOffer(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    offered_to: UUID
    offered_by: UUID
    status: OvertimeStatus = OvertimeStatus.OFFERED
    offered_at: datetime
    expires_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    declined_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class OvertimeAcceptance(BaseModel):
    id: UUID
    tenant_id: UUID
    offer_id: UUID
    person_id: UUID
    accepted_at: datetime
    audit_event_id: Optional[UUID] = None


class ShiftSwapRequest(BaseModel):
    id: UUID
    tenant_id: UUID
    requester_id: UUID
    requester_shift_id: UUID
    target_person_id: UUID
    target_shift_id: UUID
    status: SwapStatus = SwapStatus.REQUESTED
    requested_at: datetime
    reviewed_by: Optional[UUID] = None
    reviewed_at: Optional[datetime] = None
    denial_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class HoldoverOrder(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    person_id: UUID
    reason: str
    status: HoldoverStatus = HoldoverStatus.PENDING
    ordered_by: UUID
    ordered_at: datetime
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    duration_hours: float = 4.0
    ai_recommended: bool = False
    human_review_required: bool = True
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class StaffingRule(BaseModel):
    id: UUID
    tenant_id: UUID
    agency_type: str
    rule_type: str
    name: str
    description: Optional[str] = None
    parameters: dict = Field(default_factory=dict)
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class MinimumStaffingRule(BaseModel):
    id: UUID
    tenant_id: UUID
    agency_type: str
    station_id: Optional[UUID] = None
    shift_type: Optional[str] = None
    minimum_count: int
    rank_requirements: List[str] = Field(default_factory=list)
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class RankCoverageRule(BaseModel):
    id: UUID
    tenant_id: UUID
    agency_type: str
    rank: str
    minimum_per_shift: int
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class BeatCoverageRule(BaseModel):
    id: UUID
    tenant_id: UUID
    beat_id: UUID
    beat_name: str
    minimum_officers: int
    required_rank: Optional[str] = None
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class ZoneCoverageRule(BaseModel):
    id: UUID
    tenant_id: UUID
    zone_id: UUID
    zone_name: str
    minimum_units: int
    agency_type: str
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class UnionRule(BaseModel):
    id: UUID
    tenant_id: UUID
    union_name: str
    rule_key: str
    description: str
    parameters: dict = Field(default_factory=dict)
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class SeniorityRule(BaseModel):
    id: UUID
    tenant_id: UUID
    rule_key: str
    description: str
    parameters: dict = Field(default_factory=dict)
    active: bool = True
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class CourtAppearance(BaseModel):
    id: UUID
    tenant_id: UUID
    person_id: UUID
    court_date: datetime
    court_time: str
    case_number: Optional[str] = None
    location: Optional[str] = None
    shift_id: Optional[UUID] = None
    conflict_detected: bool = False
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class TrainingAssignment(BaseModel):
    id: UUID
    tenant_id: UUID
    person_id: UUID
    training_name: str
    start_time: datetime
    end_time: datetime
    mandatory: bool = False
    shift_id: Optional[UUID] = None
    conflict_detected: bool = False
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class SpecialEvent(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    description: Optional[str] = None
    event_date: datetime
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    multi_agency: bool = False
    agencies_involved: List[str] = Field(default_factory=list)
    status: str = "planned"
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class SpecialDetail(BaseModel):
    id: UUID
    tenant_id: UUID
    event_id: UUID
    person_id: UUID
    agency_type: str
    role: str
    shift_id: Optional[UUID] = None
    assigned_by: UUID
    assigned_at: datetime
    created_at: datetime
    updated_at: datetime


class PatrolBeat(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    code: str
    district_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    description: Optional[str] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class PatrolZone(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    code: str
    district_id: Optional[UUID] = None
    description: Optional[str] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class Squad(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    agency_type: str
    supervisor_id: Optional[UUID] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class Station(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    code: str
    agency_type: str
    address: Optional[str] = None
    active: bool = True
    created_at: datetime
    updated_at: datetime


class Apparatus(BaseModel):
    id: UUID
    tenant_id: UUID
    station_id: UUID
    name: str
    unit_number: str
    apparatus_type: str  # engine, ladder, medic, patrol, etc.
    active: bool = True
    created_at: datetime
    updated_at: datetime


class VehicleAssignment(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    person_id: UUID
    vehicle_id: UUID
    vehicle_unit: str
    assigned_by: UUID
    assigned_at: datetime
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class EquipmentAssignment(BaseModel):
    id: UUID
    tenant_id: UUID
    shift_id: UUID
    person_id: UUID
    equipment_id: UUID
    equipment_name: str
    assigned_by: UUID
    assigned_at: datetime
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[UUID] = None


class ScheduleAuditEvent(BaseModel):
    id: UUID
    tenant_id: UUID
    event_type: str
    actor_id: UUID
    actor_name: Optional[str] = None
    record_id: UUID
    record_type: str
    schedule_id: Optional[UUID] = None
    shift_id: Optional[UUID] = None
    before_state: Optional[dict] = None
    after_state: Optional[dict] = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    correlation_id: Optional[str] = None


class ScheduleAIAssessment(BaseModel):
    id: UUID
    tenant_id: UUID
    capability_key: str
    actor_id: UUID
    schedule_id: Optional[UUID] = None
    shift_id: Optional[UUID] = None
    assessment_type: str
    findings: List[dict] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    blocking_issues: List[str] = Field(default_factory=list)
    human_review_required: bool = True
    policy_references: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    created_at: datetime
    audit_event_id: Optional[UUID] = None
