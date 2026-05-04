"""Tests for Adaptix Scheduling Contracts."""

import pytest
from uuid import uuid4
from datetime import datetime, timezone

from adaptix_contracts.scheduling.models import (
    Schedule, ScheduleStatus, ShiftInstance, ShiftStatus,
    ShiftAssignment, AssignmentStatus, TimeOffRequest, TimeOffStatus,
    OvertimeOffer, OvertimeStatus, ShiftSwapRequest, SwapStatus,
    HoldoverOrder, HoldoverStatus, ScheduleAuditEvent, ScheduleAIAssessment,
    RiskLevel, MinimumStaffingRule, RankCoverageRule, BeatCoverageRule,
    ZoneCoverageRule, UnionRule, SeniorityRule, CourtAppearance,
    TrainingAssignment, SpecialEvent, PatrolBeat, PatrolZone, Squad,
    Station, Apparatus, VehicleAssignment, EquipmentAssignment,
)
from adaptix_contracts.scheduling.law_enforcement import (
    OfficerProfile, OfficerRank, OfficerBadge, OfficerSpecialty,
    OfficerCertification, OfficerSeniority, PatrolAssignment,
    BeatAssignment, ZoneAssignment, DistrictAssignment, CourtConflict,
    DetailAssignment, K9Assignment, SWATAssignment,
    SchoolResourceAssignment, CorrectionsPostAssignment,
)
from adaptix_contracts.scheduling.fire import (
    FireStationAssignment, ApparatusAssignment, FireMinimumStaffingRule,
    FireRoleCoverageRule, FireSpecialtyCoverage, VolunteerAvailability,
    CallbackRoster, MutualAidStaffingRequest,
)
from adaptix_contracts.scheduling.ems import (
    EMSUnitAssignment, EMSCrewPairing, ALSBLSCoverageRule,
    CredentialCoverageRule, EMSStationCoverage, EMSSkillMixValidation,
)
from adaptix_contracts.scheduling.dispatch import (
    DispatchConsoleAssignment, CallTakerCoverageRule,
    DispatcherCoverageRule, RadioChannelAssignment,
    DispatchSupervisorCoverage, MandatoryBreakCoverageRule,
    HighVolumeForecastWindow,
)
from adaptix_contracts.scheduling.corrections import (
    CorrectionsPost, CorrectionsShiftAssignment,
    CorrectionsReliefCoverage, CorrectionsTransportStaffing,
    CorrectionsPostCoverageRule,
)
from adaptix_contracts.scheduling.ai import (
    SchedulingAIAssessment, StaffingShortageFinding,
    CoverageRiskExplanation, FatigueRiskScore, OvertimeFairnessScore,
    SwapCompatibilityResult, BackfillRecommendation, HoldoverRecommendation,
    PolicyViolationWarning, SeniorityRuleExplanation,
    SupervisorDecisionSummary, StaffingCommandBriefing,
    ALL_AI_CAPABILITIES,
)
from adaptix_contracts.scheduling.events import ALL_SCHEDULING_EVENTS
from adaptix_contracts.events.registry import (
    is_registered, get_all_events,
    SCHEDULE_SHIFT_CREATED, SCHEDULE_SHIFT_ASSIGNED,
)


NOW = datetime.now(timezone.utc)
TID = uuid4()
UID = uuid4()
SID = uuid4()


# ---------------------------------------------------------------------------
# Core model tests
# ---------------------------------------------------------------------------

def test_schedule_model():
    s = Schedule(
        id=uuid4(), tenant_id=TID, name="Week 1", agency_type="ems",
        status=ScheduleStatus.DRAFT, start_date=NOW, end_date=NOW,
        created_by=UID, created_at=NOW, updated_at=NOW,
    )
    assert s.status == ScheduleStatus.DRAFT
    assert s.agency_type == "ems"


def test_shift_instance_model():
    si = ShiftInstance(
        id=uuid4(), tenant_id=TID, schedule_id=SID, agency_type="fire",
        shift_date=NOW, start_time=NOW, end_time=NOW,
        status=ShiftStatus.OPEN, created_by=UID, created_at=NOW, updated_at=NOW,
    )
    assert si.status == ShiftStatus.OPEN


def test_shift_assignment_model():
    sa = ShiftAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        person_name="Officer Smith", status=AssignmentStatus.CONFIRMED,
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert sa.status == AssignmentStatus.CONFIRMED


def test_time_off_request_model():
    tor = TimeOffRequest(
        id=uuid4(), tenant_id=TID, person_id=UID,
        start_date=NOW, end_date=NOW, status=TimeOffStatus.PENDING,
        created_by=UID, created_at=NOW, updated_at=NOW,
    )
    assert tor.status == TimeOffStatus.PENDING


def test_overtime_offer_model():
    oo = OvertimeOffer(
        id=uuid4(), tenant_id=TID, shift_id=SID,
        offered_to=UID, offered_by=UID, status=OvertimeStatus.OFFERED,
        offered_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert oo.status == OvertimeStatus.OFFERED


def test_swap_request_model():
    sr = ShiftSwapRequest(
        id=uuid4(), tenant_id=TID, requester_id=UID,
        requester_shift_id=SID, target_person_id=UID, target_shift_id=SID,
        status=SwapStatus.REQUESTED, requested_at=NOW,
        created_at=NOW, updated_at=NOW,
    )
    assert sr.status == SwapStatus.REQUESTED


def test_holdover_order_model():
    ho = HoldoverOrder(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        reason="Staffing shortage", status=HoldoverStatus.PENDING,
        ordered_by=UID, ordered_at=NOW, human_review_required=True,
        created_at=NOW, updated_at=NOW,
    )
    assert ho.human_review_required is True
    assert ho.status == HoldoverStatus.PENDING


def test_audit_event_model():
    ae = ScheduleAuditEvent(
        id=uuid4(), tenant_id=TID, event_type="schedule.shift.created",
        actor_id=UID, record_id=SID, record_type="shift",
        created_at=NOW,
    )
    assert ae.event_type == "schedule.shift.created"


def test_ai_assessment_model():
    aa = ScheduleAIAssessment(
        id=uuid4(), tenant_id=TID, capability_key="sched_ai.staffing_shortage",
        actor_id=UID, assessment_type="staffing_shortage",
        human_review_required=True, risk_level=RiskLevel.HIGH,
        created_at=NOW,
    )
    assert aa.human_review_required is True
    assert aa.risk_level == RiskLevel.HIGH


# ---------------------------------------------------------------------------
# Law enforcement model tests
# ---------------------------------------------------------------------------

def test_officer_profile_model():
    op = OfficerProfile(
        id=uuid4(), tenant_id=TID, person_id=UID,
        badge_number="1234", rank="Officer",
        created_at=NOW, updated_at=NOW,
    )
    assert op.badge_number == "1234"


def test_beat_assignment_model():
    ba = BeatAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        beat_id=uuid4(), beat_name="Beat 1",
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert ba.beat_name == "Beat 1"


def test_k9_assignment_model():
    k9 = K9Assignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, handler_id=UID,
        k9_unit_id=uuid4(), k9_name="Rex",
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert k9.k9_name == "Rex"


def test_swat_assignment_model():
    swat = SWATAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        swat_role="entry", assigned_by=UID, assigned_at=NOW,
        created_at=NOW, updated_at=NOW,
    )
    assert swat.swat_role == "entry"


def test_corrections_post_assignment_model():
    cpa = CorrectionsPostAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        post_name="Housing Block A", post_type="housing",
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert cpa.post_type == "housing"


# ---------------------------------------------------------------------------
# Fire model tests
# ---------------------------------------------------------------------------

def test_apparatus_assignment_model():
    aa = ApparatusAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID,
        apparatus_id=uuid4(), apparatus_unit="E1", apparatus_type="engine",
        station_id=uuid4(), minimum_crew=3,
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert aa.apparatus_type == "engine"
    assert aa.minimum_crew == 3


def test_mutual_aid_request_model():
    mar = MutualAidStaffingRequest(
        id=uuid4(), tenant_id=TID, requesting_agency_id=uuid4(),
        requested_count=2, status="pending",
        requested_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert mar.status == "pending"


# ---------------------------------------------------------------------------
# EMS model tests
# ---------------------------------------------------------------------------

def test_ems_unit_assignment_model():
    ua = EMSUnitAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID,
        unit_id=uuid4(), unit_number="M1", unit_type="ALS",
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert ua.unit_type == "ALS"


def test_ems_crew_pairing_model():
    cp = EMSCrewPairing(
        id=uuid4(), tenant_id=TID, shift_id=SID, unit_id=uuid4(),
        als_covered=True, bls_covered=True, skill_mix_valid=True,
        created_at=NOW, updated_at=NOW,
    )
    assert cp.skill_mix_valid is True


# ---------------------------------------------------------------------------
# Dispatch model tests
# ---------------------------------------------------------------------------

def test_dispatch_console_assignment_model():
    dca = DispatchConsoleAssignment(
        id=uuid4(), tenant_id=TID, shift_id=SID, person_id=UID,
        console_id=uuid4(), console_name="Console 1", role="dispatcher",
        assigned_by=UID, assigned_at=NOW, created_at=NOW, updated_at=NOW,
    )
    assert dca.role == "dispatcher"


def test_high_volume_forecast_model():
    hvf = HighVolumeForecastWindow(
        id=uuid4(), tenant_id=TID, forecast_date=NOW,
        start_time=NOW, end_time=NOW, predicted_call_volume=150,
        risk_level="high", recommended_staff=8,
        created_at=NOW, updated_at=NOW,
    )
    assert hvf.risk_level == "high"


# ---------------------------------------------------------------------------
# Corrections model tests
# ---------------------------------------------------------------------------

def test_corrections_post_model():
    cp = CorrectionsPost(
        id=uuid4(), tenant_id=TID, facility_id=uuid4(),
        post_name="Control Room", post_code="CR1", post_type="control",
        created_at=NOW, updated_at=NOW,
    )
    assert cp.post_type == "control"


# ---------------------------------------------------------------------------
# AI model tests
# ---------------------------------------------------------------------------

def test_fatigue_risk_score_model():
    frs = FatigueRiskScore(
        person_id=UID, shift_id=SID,
        hours_worked_last_24h=12.0, hours_worked_last_48h=20.0,
        hours_worked_last_7d=48.0, consecutive_shifts=3,
        fatigue_score=0.75, risk_level="high",
        explanation="Officer has worked 48h in 7 days.",
        human_review_required=True,
    )
    assert frs.human_review_required is True
    assert frs.risk_level == "high"


def test_holdover_recommendation_human_review():
    hr = HoldoverRecommendation(
        shift_id=SID, shortage_reason="Call-off",
        human_review_required=True,
        supervisor_approval_required=True,
        explanation="Recommend Officer Jones for holdover.",
    )
    assert hr.human_review_required is True
    assert hr.supervisor_approval_required is True


def test_policy_violation_auto_override_forbidden():
    pv = PolicyViolationWarning(
        person_id=UID, shift_id=SID,
        policy_type="union", policy_key="max_consecutive_shifts",
        violation_description="Exceeds 3 consecutive shifts",
        severity="violation", human_review_required=True,
        auto_override_forbidden=True,
        explanation="Union contract prohibits more than 3 consecutive shifts.",
    )
    assert pv.auto_override_forbidden is True


def test_all_ai_capabilities_present():
    assert len(ALL_AI_CAPABILITIES) == 20


# ---------------------------------------------------------------------------
# Event registry tests
# ---------------------------------------------------------------------------

def test_all_scheduling_events_count():
    assert len(ALL_SCHEDULING_EVENTS) == 27


def test_scheduling_events_registered():
    for event in ALL_SCHEDULING_EVENTS:
        assert is_registered(event), f"Event not registered: {event}"


def test_shift_created_event_registered():
    assert is_registered("schedule.shift.created")


def test_cad_availability_event_registered():
    assert is_registered("schedule.cad.availability.updated")


def test_mdt_availability_event_registered():
    assert is_registered("schedule.mdt.availability.updated")


def test_ai_assessment_event_registered():
    assert is_registered("schedule.ai.assessment.created")


def test_get_all_events_returns_list():
    events = get_all_events()
    assert isinstance(events, list)
    assert len(events) >= 27
