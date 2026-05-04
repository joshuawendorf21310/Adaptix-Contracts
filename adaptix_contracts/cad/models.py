"""CAD domain Pydantic models for cross-service contracts.

All models are read-only contracts. CAD owns dispatch coordination only.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ─── Enums ────────────────────────────────────────────────────────────────────

class TransportType(str, Enum):
    SCHEDULED = "SCHEDULED"
    UNSCHEDULED = "UNSCHEDULED"
    INTERFACILITY = "INTERFACILITY"
    DISCHARGE = "DISCHARGE"
    FACILITY_TO_FACILITY = "FACILITY_TO_FACILITY"
    SCENE_TO_FACILITY_MEDICAL = "SCENE_TO_FACILITY_MEDICAL"
    COMMUNITY_PARAMEDICINE = "COMMUNITY_PARAMEDICINE"
    STANDBY = "STANDBY"
    HEMS = "HEMS"


class LevelOfCare(str, Enum):
    BLS = "BLS"
    ALS = "ALS"
    CCT = "CCT"
    SCT = "SCT"
    WHEELCHAIR = "WHEELCHAIR"
    STRETCHER = "STRETCHER"
    HEMS = "HEMS"
    UNKNOWN = "UNKNOWN"


class UnitStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    ENROUTE_TO_ORIGIN = "ENROUTE_TO_ORIGIN"
    ARRIVED_AT_ORIGIN = "ARRIVED_AT_ORIGIN"
    PATIENT_CONTACT = "PATIENT_CONTACT"
    LOADED = "LOADED"
    TRANSPORTING = "TRANSPORTING"
    ARRIVED_AT_DESTINATION = "ARRIVED_AT_DESTINATION"
    TRANSFER_OF_CARE = "TRANSFER_OF_CARE"
    CLEARING = "CLEARING"
    AVAILABLE_POST_CALL = "AVAILABLE_POST_CALL"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    RESTRICTED = "RESTRICTED"
    CANCELLED = "CANCELLED"


class VehicleTrackingStatus(str, Enum):
    GPS_ACTIVE = "GPS_ACTIVE"
    GPS_STALE = "GPS_STALE"
    GPS_UNAVAILABLE = "GPS_UNAVAILABLE"
    MANUAL_STATUS_ONLY = "MANUAL_STATUS_ONLY"
    TELEMETRY_ERROR = "TELEMETRY_ERROR"


class HemsStatus(str, Enum):
    REQUESTED = "REQUESTED"
    ELIGIBILITY_REVIEW = "ELIGIBILITY_REVIEW"
    WEATHER_REVIEW = "WEATHER_REVIEW"
    AIRCRAFT_REVIEW = "AIRCRAFT_REVIEW"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    CANCELLED = "CANCELLED"
    LAUNCHED = "LAUNCHED"
    ARRIVED = "ARRIVED"
    COMPLETED = "COMPLETED"
    GROUND_FALLBACK_RECOMMENDED = "GROUND_FALLBACK_RECOMMENDED"


# ─── Facility Models ──────────────────────────────────────────────────────────

class CadOriginFacility(BaseModel):
    facility_name: Optional[str] = None
    facility_address: Optional[str] = None
    facility_department: Optional[str] = None
    facility_room_bed: Optional[str] = None
    facility_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CadDestinationFacility(BaseModel):
    facility_name: Optional[str] = None
    facility_address: Optional[str] = None
    facility_department: Optional[str] = None
    facility_room_bed: Optional[str] = None
    facility_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ─── Patient / Payer Context ──────────────────────────────────────────────────

class CadPatientContext(BaseModel):
    """Minimum patient identifiers available at CAD intake. CAD does NOT own clinical data."""
    patient_first_name: Optional[str] = None
    patient_last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_id_external: Optional[str] = None
    mrn: Optional[str] = None
    mobility_status: Optional[str] = None
    oxygen_required: bool = False
    monitoring_required: bool = False
    isolation_required: bool = False
    bariatric_required: bool = False
    escort_required: bool = False


class CadPayerContext(BaseModel):
    """Payer awareness from CAD intake. CAD does NOT own billing workflow."""
    payer_type: Optional[str] = None
    payer_name: Optional[str] = None
    authorization_number: Optional[str] = None
    pcs_likely_required: bool = False
    abn_awareness: bool = False
    aob_awareness: bool = False
    document_dependency_notes: Optional[str] = None


# ─── Transport Request ────────────────────────────────────────────────────────

class CadTransportRequestReason(BaseModel):
    reason_code: Optional[str] = None
    reason_text: Optional[str] = None
    diagnosis_context: Optional[str] = None
    medical_necessity_notes: Optional[str] = None


class CadMedicalTransportIntake(BaseModel):
    intake_id: str
    tenant_id: str
    transport_type: TransportType
    scheduled: bool = False
    recurring: bool = False
    caller_name: Optional[str] = None
    caller_callback: Optional[str] = None
    requesting_facility: Optional[str] = None
    requesting_department: Optional[str] = None
    origin: CadOriginFacility = Field(default_factory=CadOriginFacility)
    destination: CadDestinationFacility = Field(default_factory=CadDestinationFacility)
    requested_pickup_time: Optional[datetime] = None
    appointment_time: Optional[datetime] = None
    transport_reason: Optional[CadTransportRequestReason] = None
    patient_context: Optional[CadPatientContext] = None
    payer_context: Optional[CadPayerContext] = None
    preferred_unit_type: Optional[str] = None
    requested_crew_level: Optional[str] = None
    sending_clinician: Optional[str] = None
    receiving_clinician: Optional[str] = None
    special_handling_notes: Optional[str] = None
    equipment_requirements: List[str] = Field(default_factory=list)
    status: str = "new"
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    tenant_correlation_id: Optional[str] = None


# ─── Dispatch ─────────────────────────────────────────────────────────────────

class CadTransportDispatch(BaseModel):
    dispatch_id: str
    intake_id: str
    tenant_id: str
    transport_type: TransportType
    level_of_care: LevelOfCare
    priority: Optional[str] = None
    unit_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    crew_ids: List[str] = Field(default_factory=list)
    origin: CadOriginFacility = Field(default_factory=CadOriginFacility)
    destination: CadDestinationFacility = Field(default_factory=CadDestinationFacility)
    status: str = "created"
    dispatcher_notes: Optional[str] = None
    facility_notes: Optional[str] = None
    crew_notes: Optional[str] = None
    delay_reason: Optional[str] = None
    cancellation_reason: Optional[str] = None
    supervisor_review_flag: bool = False
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None


# ─── Assessments ──────────────────────────────────────────────────────────────

class CadLevelOfCareAssessment(BaseModel):
    assessment_id: str
    intake_id: str
    tenant_id: str
    recommended_level: LevelOfCare
    explanation: Optional[str] = None
    indicators: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None
    risk_level: Optional[str] = None
    rule_version: Optional[str] = None
    policy_reference: Optional[str] = None
    human_review_required: bool = True
    assessed_at: datetime
    assessed_by: Optional[str] = None


class CadMedicalNecessityAssessment(BaseModel):
    assessment_id: str
    intake_id: str
    tenant_id: str
    qualifies_for_transport: bool
    support_text: Optional[str] = None
    indicators: List[str] = Field(default_factory=list)
    missing_documentation: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None
    risk_level: Optional[str] = None
    reason_codes: List[str] = Field(default_factory=list)
    human_review_required: bool = True
    ai_may_not_approve: bool = True
    rule_version: Optional[str] = None
    assessed_at: datetime
    assessed_by: Optional[str] = None


class CadPCSRequirementAwareness(BaseModel):
    intake_id: str
    pcs_likely_required: bool
    explanation: Optional[str] = None
    policy_reference: Optional[str] = None


class CadABNRequirementAwareness(BaseModel):
    intake_id: str
    abn_awareness: bool
    explanation: Optional[str] = None


class CadAOBRequirementAwareness(BaseModel):
    intake_id: str
    aob_awareness: bool
    explanation: Optional[str] = None


# ─── Unit / Crew Recommendations ─────────────────────────────────────────────

class CadUnitRecommendation(BaseModel):
    recommendation_id: str
    intake_id: str
    tenant_id: str
    recommended_unit_id: Optional[str] = None
    recommended_unit_type: Optional[str] = None
    explanation: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None
    human_review_required: bool = True
    recommended_at: datetime


class CadCrewRecommendation(BaseModel):
    recommendation_id: str
    intake_id: str
    tenant_id: str
    recommended_crew_ids: List[str] = Field(default_factory=list)
    explanation: Optional[str] = None
    credential_warnings: List[str] = Field(default_factory=list)
    fatigue_warnings: List[str] = Field(default_factory=list)
    human_review_required: bool = True
    recommended_at: datetime


class CadUnitAssignment(BaseModel):
    assignment_id: str
    dispatch_id: str
    tenant_id: str
    unit_id: str
    vehicle_id: Optional[str] = None
    crew_ids: List[str] = Field(default_factory=list)
    assigned_at: datetime
    assigned_by: str
    reassignment: bool = False
    reassignment_reason: Optional[str] = None


# ─── Vehicle Tracking ─────────────────────────────────────────────────────────

class CadVehicleTrackingSnapshot(BaseModel):
    snapshot_id: str
    vehicle_id: str
    unit_id: Optional[str] = None
    tenant_id: str
    dispatch_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None
    speed_mph: Optional[float] = None
    accuracy_meters: Optional[float] = None
    tracking_status: VehicleTrackingStatus = VehicleTrackingStatus.GPS_UNAVAILABLE
    telemetry_source: Optional[str] = None
    captured_at: datetime
    is_stale: bool = False


class CadVehicleTelemetryPoint(BaseModel):
    telemetry_id: str
    vehicle_id: str
    unit_id: Optional[str] = None
    tenant_id: str
    dispatch_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[float] = None
    speed_mph: Optional[float] = None
    odometer: Optional[float] = None
    accuracy_meters: Optional[float] = None
    source: Optional[str] = None
    received_at: datetime


class CadUnitStatusUpdate(BaseModel):
    status_id: str
    unit_id: str
    dispatch_id: Optional[str] = None
    tenant_id: str
    old_status: Optional[UnitStatus] = None
    new_status: UnitStatus
    manual_override: bool = False
    override_reason: Optional[str] = None
    updated_at: datetime
    updated_by: Optional[str] = None
    mdt_source: bool = False


# ─── Timeline ─────────────────────────────────────────────────────────────────

class CadTransportTimeline(BaseModel):
    dispatch_id: str
    tenant_id: str
    call_received_at: Optional[datetime] = None
    unit_notified_at: Optional[datetime] = None
    unit_enroute_at: Optional[datetime] = None
    unit_arrived_origin_at: Optional[datetime] = None
    patient_contact_at: Optional[datetime] = None
    unit_loaded_at: Optional[datetime] = None
    transport_begin_at: Optional[datetime] = None
    arrived_destination_at: Optional[datetime] = None
    transfer_of_care_at: Optional[datetime] = None
    unit_clear_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None
    dispatch_created_at: Optional[datetime] = None
    unit_assigned_at: Optional[datetime] = None


# ─── Routing / ETA ────────────────────────────────────────────────────────────

class CadRoutingEta(BaseModel):
    eta_id: str
    dispatch_id: str
    tenant_id: str
    pickup_eta_minutes: Optional[float] = None
    destination_eta_minutes: Optional[float] = None
    route_distance_miles: Optional[float] = None
    eta_confidence: Optional[str] = None
    routing_risk: Optional[str] = None
    provider_credential_gated: bool = False
    manual_override: bool = False
    override_reason: Optional[str] = None
    calculated_at: datetime


class CadGeocodeResult(BaseModel):
    geocode_id: str
    input_address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    formatted_address: Optional[str] = None
    confidence: Optional[str] = None
    provider_credential_gated: bool = False
    geocoded_at: datetime


# ─── HEMS ─────────────────────────────────────────────────────────────────────

class CadHemsRequest(BaseModel):
    request_id: str
    tenant_id: str
    intake_id: Optional[str] = None
    dispatch_id: Optional[str] = None
    request_reason: Optional[str] = None
    pickup_location: Optional[CadOriginFacility] = None
    destination_facility: Optional[CadDestinationFacility] = None
    landing_zone_details: Optional[str] = None
    patient_context: Optional[CadPatientContext] = None
    sending_clinician: Optional[str] = None
    receiving_facility: Optional[str] = None
    status: HemsStatus = HemsStatus.REQUESTED
    cancellation_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    created_by: str


class CadHemsEligibilityAssessment(BaseModel):
    assessment_id: str
    request_id: str
    tenant_id: str
    eligible: bool
    explanation: Optional[str] = None
    missing_fields: List[str] = Field(default_factory=list)
    ground_alternative_available: bool = False
    human_review_required: bool = True
    ai_may_not_accept: bool = True
    assessed_at: datetime


class CadHemsBriefing(BaseModel):
    briefing_id: str
    request_id: str
    tenant_id: str
    briefing_text: str
    weather_status: Optional[str] = None
    weather_credential_gated: bool = False
    aircraft_availability: Optional[str] = None
    pilot_availability: Optional[str] = None
    medical_crew_availability: Optional[str] = None
    generated_at: datetime


class CadGroundFallbackRecommendation(BaseModel):
    recommendation_id: str
    request_id: str
    tenant_id: str
    recommended: bool
    reason: Optional[str] = None
    explanation: Optional[str] = None
    human_review_required: bool = True
    recommended_at: datetime


# ─── Handoffs ─────────────────────────────────────────────────────────────────

class CadTransportLinkHandoff(BaseModel):
    handoff_id: str
    dispatch_id: str
    intake_id: Optional[str] = None
    tenant_id: str
    transport_request_id: Optional[str] = None
    patient_context: Optional[CadPatientContext] = None
    origin: Optional[CadOriginFacility] = None
    destination: Optional[CadDestinationFacility] = None
    level_of_care: Optional[LevelOfCare] = None
    medical_necessity_assessment: Optional[str] = None
    pcs_awareness: bool = False
    abn_awareness: bool = False
    aob_awareness: bool = False
    scheduling_status: Optional[str] = None
    dispatch_readiness: Optional[str] = None
    handoff_status: str = "created"
    handoff_failure_reason: Optional[str] = None
    downstream_id: Optional[str] = None
    created_at: datetime


class CadEpcrHandoff(BaseModel):
    handoff_id: str
    dispatch_id: str
    tenant_id: str
    hems_request_id: Optional[str] = None
    transport_type: Optional[TransportType] = None
    level_of_care: Optional[LevelOfCare] = None
    timeline: Optional[CadTransportTimeline] = None
    unit_id: Optional[str] = None
    vehicle_id: Optional[str] = None
    crew_ids: List[str] = Field(default_factory=list)
    patient_context: Optional[CadPatientContext] = None
    origin: Optional[CadOriginFacility] = None
    destination: Optional[CadDestinationFacility] = None
    mileage_estimate: Optional[float] = None
    medical_necessity_support_text: Optional[str] = None
    handoff_status: str = "created"
    handoff_failure_reason: Optional[str] = None
    downstream_epcr_id: Optional[str] = None
    created_at: datetime


class CadBillingHandoff(BaseModel):
    handoff_id: str
    dispatch_id: str
    tenant_id: str
    payer_context: Optional[CadPayerContext] = None
    level_of_care: Optional[LevelOfCare] = None
    medical_necessity_text: Optional[str] = None
    transport_mileage: Optional[float] = None
    route_eta_minutes: Optional[float] = None
    document_dependency_awareness: Optional[str] = None
    handoff_status: str = "created"
    handoff_failure_reason: Optional[str] = None
    downstream_billing_id: Optional[str] = None
    created_at: datetime


class CadCrewLinkPageRequest(BaseModel):
    page_id: str
    dispatch_id: str
    tenant_id: str
    crew_ids: List[str] = Field(default_factory=list)
    crew_briefing: Optional[str] = None
    route_briefing: Optional[str] = None
    facility_handoff_notes: Optional[str] = None
    acknowledgement_status: str = "pending"
    acknowledged_at: Optional[datetime] = None
    escalated: bool = False
    created_at: datetime


# ─── MDT / Scheduling ─────────────────────────────────────────────────────────

class CadMdtSyncEvent(BaseModel):
    sync_id: str
    dispatch_id: str
    unit_id: str
    tenant_id: str
    sync_type: str
    payload_summary: Optional[str] = None
    mdt_online: bool = True
    last_sync_at: datetime
    offline_queued: bool = False


class CadSchedulingAvailabilitySnapshot(BaseModel):
    snapshot_id: str
    tenant_id: str
    unit_id: Optional[str] = None
    crew_id: Optional[str] = None
    available: bool
    shift_end_at: Optional[datetime] = None
    fatigue_warning: bool = False
    credential_warning: bool = False
    credential_expiry_notes: Optional[str] = None
    captured_at: datetime


class CadVoiceRoomRequest(BaseModel):
    room_id: str
    dispatch_id: str
    tenant_id: str
    crew_ids: List[str] = Field(default_factory=list)
    room_status: str = "created"
    communications_audit_id: Optional[str] = None
    created_at: datetime


# ─── AI Assessment ────────────────────────────────────────────────────────────

class CadAIAssessment(BaseModel):
    assessment_id: str
    dispatch_id: Optional[str] = None
    intake_id: Optional[str] = None
    tenant_id: str
    assessment_type: str
    summary: Optional[str] = None
    recommendations: List[str] = Field(default_factory=list)
    input_fields_used: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None
    risk_level: Optional[str] = None
    policy_references: List[str] = Field(default_factory=list)
    human_review_required: bool = True
    ai_may_not_dispatch: bool = True
    ai_may_not_request_hems: bool = True
    ai_may_not_create_epcr: bool = True
    ai_may_not_create_billing: bool = True
    assessed_at: datetime


# ─── Audit ────────────────────────────────────────────────────────────────────

class CadAuditEvent(BaseModel):
    audit_id: str
    tenant_id: str
    actor_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: str
    changes_before: Optional[Dict[str, Any]] = None
    changes_after: Optional[Dict[str, Any]] = None
    override: bool = False
    override_reason: Optional[str] = None
    supervisor_required: bool = False
    occurred_at: datetime
