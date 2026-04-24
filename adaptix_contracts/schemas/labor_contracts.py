"""Labor domain contracts for cross-domain communication.

Defines contracts for the Adaptix Labor Service: workforce lifecycle,
shift scheduling, assignment decisions, open-shift marketplace,
leave/trade requests, fatigue scoring, compliance enforcement,
compensation resolution, and payroll export events.

These contracts are the authoritative source for all labor domain
data exchanged across Adaptix services.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EmploymentStatus(str, Enum):
    """Lifecycle status of a labor employee."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    REHIRED = "rehired"


class LaborDomain(str, Enum):
    """Operational domain for a labor entity."""

    EMS = "ems"
    FIRE = "fire"
    LAW = "law"
    HEMS = "hems"
    MULTI = "multi"


class ShiftStatus(str, Enum):
    """Lifecycle status of a labor shift."""

    DRAFT = "draft"
    PUBLISHED = "published"
    LOCKED = "locked"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AssignmentStatus(str, Enum):
    """Status of a shift assignment."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    OVERRIDDEN = "overridden"
    CANCELLED = "cancelled"


class TradeStatus(str, Enum):
    """Status of a shift trade proposal."""

    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    DENIED = "denied"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class LeaveStatus(str, Enum):
    """Status of a leave request."""

    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CANCELLED = "cancelled"


class ClaimStatus(str, Enum):
    """Status of an open-shift claim."""

    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    EXPIRED = "expired"


class CommandPosture(str, Enum):
    """Operational posture governing scheduling decisions."""

    NORMAL = "normal"
    SURGE = "surge"
    DISASTER = "disaster"
    COST_CONTROL = "cost_control"
    MUTUAL_AID = "mutual_aid"
    COMPLIANCE_FIRST = "compliance_first"


class PayrollExportStatus(str, Enum):
    """Status of a payroll export run."""

    DRAFT = "draft"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    LOCKED = "locked"


class PolicyStatus(str, Enum):
    """Lifecycle status of a labor policy version."""

    DRAFT = "draft"
    PUBLISHED = "published"
    SUPERSEDED = "superseded"


# ---------------------------------------------------------------------------
# Read contracts
# ---------------------------------------------------------------------------

class LaborShiftContract(BaseModel):
    """Cross-domain read contract for a scheduled labor shift."""

    shift_id: str
    tenant_id: str
    domain: LaborDomain
    status: ShiftStatus
    shift_date: date
    start_time: str
    end_time: str
    station_id: Optional[str] = None
    unit_id: Optional[str] = None
    minimum_staffing: int
    is_locked: bool
    created_at: datetime


class LaborAssignmentContract(BaseModel):
    """Cross-domain read contract for a shift assignment."""

    assignment_id: str
    tenant_id: str
    shift_id: str
    slot_id: str
    employee_id: str
    status: AssignmentStatus
    override_reason: Optional[str] = None
    assigned_by: str
    assigned_at: datetime


class LaborEmployeeReadinessContract(BaseModel):
    """Cross-domain read contract for an employee readiness snapshot."""

    employee_id: str
    tenant_id: str
    unit_id: Optional[str] = None
    readiness_score: float
    cert_valid: bool
    rest_valid: bool
    pairing_valid: bool
    coverage_valid: bool
    no_ot_risk: bool
    evaluated_at: datetime


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class LaborShiftPublishedEvent(BaseModel):
    """Published when a shift transitions from draft to published."""

    event_type: str = "labor.shift.published"

    shift_id: str
    tenant_id: str
    domain: LaborDomain
    shift_date: date
    start_time: str
    end_time: str
    station_id: Optional[str] = None
    unit_id: Optional[str] = None
    published_by: str
    occurred_at: datetime


class LaborShiftLockedEvent(BaseModel):
    """Published when a shift is locked and no longer editable."""

    event_type: str = "labor.shift.locked"

    shift_id: str
    tenant_id: str
    locked_by: str
    occurred_at: datetime


class LaborAssignmentCommittedEvent(BaseModel):
    """Published when an employee is assigned to a shift slot."""

    event_type: str = "labor.assignment.committed"

    assignment_id: str
    shift_id: str
    slot_id: str
    tenant_id: str
    employee_id: str
    command_posture: CommandPosture
    override_occurred: bool
    override_reason: Optional[str] = None
    assigned_by: str
    total_distortion_score: Optional[float] = None
    occurred_at: datetime


class LaborOpenShiftClaimSubmittedEvent(BaseModel):
    """Published when an employee submits a claim on an open shift."""

    event_type: str = "labor.open_shift.claim_submitted"

    claim_id: str
    open_shift_id: str
    tenant_id: str
    employee_id: str
    fatigue_score_at_claim: Optional[float] = None
    ot_impact_hours: Optional[float] = None
    occurred_at: datetime


class LaborShiftTradeProposedEvent(BaseModel):
    """Published when a shift trade is proposed between two employees."""

    event_type: str = "labor.shift_trade.proposed"

    trade_id: str
    tenant_id: str
    requesting_employee_id: str
    receiving_employee_id: str
    shift_id_offered: str
    shift_id_requested: str
    supervisor_approval_required: bool
    occurred_at: datetime


class LaborLeaveRequestSubmittedEvent(BaseModel):
    """Published when a leave request is submitted."""

    event_type: str = "labor.leave_request.submitted"

    leave_request_id: str
    tenant_id: str
    employee_id: str
    leave_type: str
    start_date: date
    end_date: date
    occurred_at: datetime


class LaborComplianceViolationCreatedEvent(BaseModel):
    """Published when a policy compliance violation is detected."""

    event_type: str = "labor.compliance.violation_created"

    violation_id: str
    tenant_id: str
    employee_id: str
    shift_id: Optional[str] = None
    rule_code: str
    severity: str
    detected_at: datetime
    occurred_at: datetime


class LaborFatigueRestrictionAppliedEvent(BaseModel):
    """Published when a fatigue block threshold is exceeded for an employee."""

    event_type: str = "labor.fatigue.restriction_applied"

    tenant_id: str
    employee_id: str
    fatigue_score: float
    consecutive_hours: float
    rolling_hours: float
    is_blocked: bool
    evaluated_at: datetime
    occurred_at: datetime


class LaborPayrollExportSubmittedEvent(BaseModel):
    """Published when a payroll export run is submitted to an external system."""

    event_type: str = "labor.payroll_export.submitted"

    export_run_id: str
    tenant_id: str
    external_system: str
    pay_period_start: date
    pay_period_end: date
    item_count: int
    submitted_at: datetime
    occurred_at: datetime


class LaborExternalSyncCompletedEvent(BaseModel):
    """Published when an external system integration sync job completes."""

    event_type: str = "labor.external_sync.completed"

    sync_job_id: str
    tenant_id: str
    external_system: str
    sync_direction: str
    records_imported: int
    records_errored: int
    completed_at: datetime
    occurred_at: datetime
