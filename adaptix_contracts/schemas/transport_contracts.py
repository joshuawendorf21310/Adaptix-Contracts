"""TransportLink domain contract schemas for cross-domain communication.

Defines all typed request, response, and event contracts for the transport
network coordination lifecycle: intake, scheduling, recurring series,
document packages, signatures, readiness, facility scheduling, and CAD push.

These are the single source of truth consumed across transportlink, cad,
billing, care, crewlink, and the web layer.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TransportRequestTypeContract(str, Enum):
    """Transport modality type."""

    BLS = "bls"
    ALS = "als"
    CCT = "cct"
    WHEELCHAIR = "wheelchair"
    BARIATRIC = "bariatric"
    AIR = "air"


class TransportRequestStatusContract(str, Enum):
    """Lifecycle status of a transport request."""

    DRAFT = "draft"
    INTAKE = "intake"
    QUALIFIED = "qualified"
    SCHEDULED = "scheduled"
    DISPATCH_READY = "dispatch_ready"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RecurrencePatternContract(str, Enum):
    """Supported recurrence intervals for transport series."""

    DAILY = "daily"
    WEEKDAYS = "weekdays"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class TransportRequestCreate(BaseModel):
    """Intake contract for creating a new transport request.

    All fields required for full qualification. Partial intakes must be
    submitted as drafts and are not eligible for scheduling until complete.
    """

    patient_name: str = Field(..., max_length=255)
    patient_dob: Optional[str] = Field(None, description="ISO 8601 date string")
    patient_mrn: Optional[str] = Field(None, max_length=100)
    pickup_facility_id: str = Field(..., description="Registered facility ID")
    destination_facility_id: str = Field(..., description="Registered facility ID")
    transport_type: TransportRequestTypeContract
    level_of_care: str = Field(..., max_length=100)
    requested_pickup_at: datetime
    appointment_at: Optional[datetime] = None
    pcs_required: bool = False
    authorization_required: bool = False
    payer_name: Optional[str] = Field(None, max_length=255)
    payer_id: Optional[str] = Field(None, max_length=100)
    is_recurring: bool = False
    recurrence_pattern: Optional[RecurrencePatternContract] = None
    recurrence_end_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=2000)


class TransportRequestResponse(BaseModel):
    """Read contract for a transport request returned to any consumer."""

    id: str
    tenant_id: str
    patient_name: str
    patient_dob: Optional[str]
    patient_mrn: Optional[str]
    pickup_facility_id: str
    destination_facility_id: str
    transport_type: str
    level_of_care: str
    status: str
    requested_pickup_at: datetime
    appointment_at: Optional[datetime]
    pcs_required: bool
    authorization_required: bool
    authorization_status: Optional[str]
    authorization_number: Optional[str]
    payer_name: Optional[str]
    payer_id: Optional[str]
    is_recurring: bool
    recurrence_pattern: Optional[str]
    recurrence_end_date: Optional[datetime]
    notes: Optional[str]
    documents_ready: bool
    signature_complete: bool
    created_at: datetime
    updated_at: Optional[datetime]


class TripScheduleRequest(BaseModel):
    """Contract for scheduling a trip against a transport request."""

    transport_request_id: str
    scheduled_pickup_at: datetime
    scheduled_dropoff_at: Optional[datetime] = None
    unit_id: Optional[str] = None
    crew_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=2000)


class TripResponse(BaseModel):
    """Read contract for a scheduled transport trip."""

    id: str
    tenant_id: str
    transport_request_id: str
    scheduled_pickup_at: datetime
    scheduled_dropoff_at: Optional[datetime]
    unit_id: Optional[str]
    crew_ids: list[str]
    status: str
    cad_linked: bool
    created_at: datetime
    updated_at: Optional[datetime]


class RecurringSeriesCreate(BaseModel):
    """Contract for creating a recurring transport series."""

    transport_request_id: str
    pattern: RecurrencePatternContract
    series_start_date: datetime
    series_end_date: Optional[datetime] = None
    preferred_pickup_time: str = Field(..., description="HH:MM in 24-hour format")
    max_occurrences: Optional[int] = Field(None, ge=1, le=365)


class RecurringSeriesResponse(BaseModel):
    """Read contract for a recurring transport series."""

    id: str
    tenant_id: str
    transport_request_id: str
    pattern: str
    series_start_date: datetime
    series_end_date: Optional[datetime]
    preferred_pickup_time: str
    max_occurrences: Optional[int]
    occurrences_generated: int
    occurrences_remaining: int
    status: str
    created_at: datetime


class CalendarEventResponse(BaseModel):
    """Read contract for a single calendar event slot."""

    id: str
    trip_id: str
    transport_request_id: str
    patient_name: str
    pickup_facility_id: str
    destination_facility_id: str
    transport_type: str
    scheduled_pickup_at: datetime
    scheduled_dropoff_at: Optional[datetime]
    status: str
    readiness_state: str
    unit_id: Optional[str]
    is_recurring: bool
    series_id: Optional[str]


class SlotSuggestionRequest(BaseModel):
    """Contract for requesting AI slot suggestions."""

    transport_request_id: str
    preferred_date: datetime
    window_hours: int = Field(4, ge=1, le=24)
    avoid_unit_ids: list[str] = Field(default_factory=list)


class SlotSuggestionResponse(BaseModel):
    """Contract for a single suggested scheduling slot."""

    suggested_pickup_at: datetime
    suggested_dropoff_at: Optional[datetime]
    available_unit_ids: list[str]
    conflict_score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str


class DocumentPackageResponse(BaseModel):
    """Read contract for a transport document package."""

    request_id: str
    documents: list[DocumentItemResponse]
    all_requirements_met: bool
    missing_requirements: list[str]


class DocumentItemResponse(BaseModel):
    """Read contract for a single document in a transport package."""

    id: str
    document_type: str
    status: str
    signed: bool
    download_url: Optional[str]
    generated_at: Optional[datetime]
    signed_at: Optional[datetime]


class SignatureStatusResponse(BaseModel):
    """Read contract for a Dropbox Sign embedded signature request."""

    id: str
    transport_request_id: str
    signature_request_id: str
    embedded_sign_url: Optional[str]
    status: str
    signers: list[SignerStatusResponse]
    completed_at: Optional[datetime]
    created_at: datetime


class SignerStatusResponse(BaseModel):
    """Read contract for an individual signer status."""

    signer_email: str
    signer_name: str
    status: str
    signed_at: Optional[datetime]


class ReadinessStateResponse(BaseModel):
    """Read contract for transport request readiness evaluation."""

    request_id: str
    overall_ready: bool
    gates: list[ReadinessGate]
    blocking_count: int
    evaluated_at: datetime


class ReadinessGate(BaseModel):
    """A single readiness gate with pass/fail status and reason."""

    gate: str
    passed: bool
    reason: Optional[str]


class FacilityResponse(BaseModel):
    """Read contract for a registered transport facility."""

    id: str
    tenant_id: str
    name: str
    facility_type: str
    address: str
    city: str
    state: str
    zip_code: str
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    active: bool
    created_at: datetime


class CadPushRequest(BaseModel):
    """Contract for pushing a scheduled trip into CAD active operations."""

    trip_id: str
    force: bool = False
    operator_note: Optional[str] = Field(None, max_length=500)


class CadPushResponse(BaseModel):
    """Response contract for a CAD push operation."""

    trip_id: str
    cad_link_id: str
    pushed_at: datetime
    status: str


class TransportRequestCreatedEvent(BaseModel):
    """Published when a transport request is created."""

    event_type: str = "transportlink.request.created"
    request_id: str
    tenant_id: str
    transport_type: str
    pickup_facility_id: str
    destination_facility_id: str
    created_at: datetime


class TripScheduledEvent(BaseModel):
    """Published when a trip is scheduled against a transport request."""

    event_type: str = "transportlink.trip.scheduled"
    trip_id: str
    request_id: str
    tenant_id: str
    scheduled_pickup_at: datetime
    unit_id: Optional[str]
    created_at: datetime


class SignatureCompletedEvent(BaseModel):
    """Published when all signers have completed a signature request."""

    event_type: str = "transportlink.signature.completed"
    signature_request_id: str
    request_id: str
    tenant_id: str
    document_types: list[str]
    completed_at: datetime


class CadPushRequestedEvent(BaseModel):
    """Published when a trip is pushed to CAD operational state."""

    event_type: str = "transportlink.cad.push_requested"
    trip_id: str
    request_id: str
    tenant_id: str
    unit_id: Optional[str]
    crew_ids: list[str]
    pushed_at: datetime
