"""
TransportLink Pydantic Schemas

Request/Response schemas for TransportLink API endpoints.
Provides validation, serialization, and documentation for all TransportLink operations.
"""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from adaptix_contracts.types.enums import (
    FacilityType,
    PCSABNStatus,
    TransportStatus,
    TransportType,
)

# ============================================================================
# FACILITY SCHEMAS
# ============================================================================


class FacilityBasePayload(BaseModel):
    """Base facility information"""

    name: str = Field(min_length=1, max_length=255)
    facility_type: FacilityType
    address: str | None = None
    city: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=2)
    zip_code: str | None = Field(default=None, max_length=10)
    contact_phone: str | None = Field(default=None, max_length=32)
    contact_email: str | None = Field(default=None, max_length=255)
    contact_name: str | None = Field(default=None, max_length=255)
    default_pickup_instructions: str | None = None
    capabilities: dict[str, Any] = Field(default_factory=dict)
    billing_contact_info: dict[str, Any] = Field(default_factory=dict)
    notes: str | None = None


class FacilityCreateRequest(FacilityBasePayload):
    """Request to create a new facility"""

    portal_enabled: bool = Field(default=False)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("facility name must not be empty")
        return normalized


class FacilityUpdateRequest(BaseModel):
    """Request to update facility"""

    version: int = Field(ge=1)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    facility_type: FacilityType | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    contact_phone: str | None = None
    contact_email: str | None = None
    contact_name: str | None = None
    portal_enabled: bool | None = None
    default_pickup_instructions: str | None = None
    capabilities: dict[str, Any] | None = None
    billing_contact_info: dict[str, Any] | None = None
    notes: str | None = None


class FacilityResponse(BaseModel):
    """Facility response with full details"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    facility_type: FacilityType
    address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    contact_phone: str | None
    contact_email: str | None
    contact_name: str | None
    portal_enabled: bool
    api_key_created_at: datetime | None
    last_portal_access: datetime | None
    capabilities: dict[str, Any]
    default_pickup_instructions: str | None
    billing_contact_info: dict[str, Any]
    notes: str | None
    extra_metadata: dict[str, Any] = Field(default_factory=dict, alias="extra_metadata")
    created_at: datetime
    updated_at: datetime


class FacilityListResponse(BaseModel):
    """Paginated list of facilities"""

    items: list[FacilityResponse]
    total: int
    limit: int
    offset: int


class FacilityPortalAccessRequest(BaseModel):
    """Request to generate portal access credentials"""

    regenerate: bool = Field(
        default=False, description="Force regenerate API key even if one exists"
    )


class FacilityPortalAccessResponse(BaseModel):
    """Portal access credentials response"""

    facility_id: uuid.UUID
    api_key: str = Field(
        description="Store securely - only shown once"
    )
    created_at: datetime
    instructions: str = Field(
        default="Use this API key in the Authorization header as 'Bearer {api_key}'"
    )


# ============================================================================
# TRANSPORT SCHEMAS
# ============================================================================


class TransportBasePayload(BaseModel):
    """Base transport information"""

    patient_name: str = Field(min_length=1, max_length=255)
    patient_dob: datetime | None = None
    patient_phone: str | None = Field(default=None, max_length=32)
    patient_mrn: str | None = Field(default=None, max_length=64)

    pickup_location: str = Field(min_length=1)
    pickup_special_instructions: str | None = None
    destination: str = Field(min_length=1)
    destination_special_instructions: str | None = None

    appointment_time: datetime | None = None
    pickup_window_start: datetime | None = None
    pickup_window_end: datetime | None = None

    transport_type: TransportType = Field(default=TransportType.SCHEDULED)
    priority_level: int = Field(default=3, ge=1, le=5)

    special_requirements: dict[str, Any] = Field(default_factory=dict)
    medical_necessity_notes: str | None = None
    equipment_needed: list[str] = Field(default_factory=list)

    pcs_abn_status: PCSABNStatus = Field(default=PCSABNStatus.NOT_REQUIRED)
    insurance_info: dict[str, Any] = Field(default_factory=dict)

    notes: str | None = None

    @field_validator("appointment_time", "pickup_window_start", "pickup_window_end", "patient_dob")
    @classmethod
    def ensure_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Datetime values must be timezone-aware")
        return value

    @field_validator("patient_name", "pickup_location", "destination")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Field must not be empty")
        return normalized


class TransportCreateRequest(TransportBasePayload):
    """Request to create a new transport"""

    facility_id: uuid.UUID
    recurring_pattern: str | None = Field(
        default=None,
        max_length=64,
        description="RRULE format for recurring transports",
    )


class TransportUpdateRequest(BaseModel):
    """Request to update transport"""

    version: int = Field(ge=1)
    patient_name: str | None = None
    patient_dob: datetime | None = None
    patient_phone: str | None = None
    patient_mrn: str | None = None
    pickup_location: str | None = None
    pickup_special_instructions: str | None = None
    destination: str | None = None
    destination_special_instructions: str | None = None
    appointment_time: datetime | None = None
    pickup_window_start: datetime | None = None
    pickup_window_end: datetime | None = None
    transport_type: TransportType | None = None
    priority_level: int | None = Field(default=None, ge=1, le=5)
    special_requirements: dict[str, Any] | None = None
    medical_necessity_notes: str | None = None
    equipment_needed: list[str] | None = None
    pcs_abn_status: PCSABNStatus | None = None
    insurance_info: dict[str, Any] | None = None
    notes: str | None = None
    internal_notes: str | None = None

    @field_validator("appointment_time", "pickup_window_start", "pickup_window_end", "patient_dob")
    @classmethod
    def ensure_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Datetime values must be timezone-aware")
        return value


class TransportScheduleRequest(BaseModel):
    """Request to schedule a transport"""

    version: int = Field(ge=1)
    scheduled_pickup_time: datetime
    assigned_unit_id: str | None = Field(default=None, max_length=64)
    assigned_crew_ids: list[uuid.UUID] = Field(default_factory=list)

    @field_validator("scheduled_pickup_time")
    @classmethod
    def ensure_timezone_aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("scheduled_pickup_time must be timezone-aware")
        return value


class TransportStatusTransitionRequest(BaseModel):
    """Request to transition transport status"""

    version: int = Field(ge=1)
    target_status: TransportStatus
    reason: str | None = Field(default=None, max_length=512)
    extra_metadata: dict[str, Any] = Field(default_factory=dict)


class TransportPushToCADRequest(BaseModel):
    """Request to push transport to CAD system"""

    version: int = Field(ge=1)
    cad_priority: int = Field(default=3, ge=1, le=5)
    cad_call_type: str = Field(
        default="SCHEDULED_TRANSPORT", max_length=64
    )
    additional_notes: str | None = None


class TransportResponse(BaseModel):
    """Transport response with full details"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    transport_number: str
    facility_id: uuid.UUID

    # Patient info
    patient_name: str
    patient_dob: datetime | None
    patient_phone: str | None
    patient_mrn: str | None

    # Locations
    pickup_location: str
    pickup_address_normalized: str | None
    pickup_coordinates: dict[str, Any]
    pickup_special_instructions: str | None
    destination: str
    destination_address_normalized: str | None
    destination_coordinates: dict[str, Any]
    destination_special_instructions: str | None

    # Timing
    appointment_time: datetime | None
    pickup_window_start: datetime | None
    pickup_window_end: datetime | None
    scheduled_pickup_time: datetime | None

    # Classification
    transport_type: TransportType
    priority_level: int

    # Medical requirements
    special_requirements: dict[str, Any]
    medical_necessity_notes: str | None
    equipment_needed: list[str]

    # Billing
    pcs_abn_status: PCSABNStatus
    insurance_info: dict[str, Any]

    # State
    status: TransportStatus
    status_changed_at: datetime
    status_changed_by_user_id: uuid.UUID | None

    # Assignment
    assigned_unit_id: str | None
    assigned_crew_ids: list[uuid.UUID]
    assigned_at: datetime | None

    # CAD integration
    cad_incident_id: str | None
    cad_pushed_at: datetime | None
    cad_response_data: dict[str, Any]

    # Recurring
    recurring_pattern: str | None
    recurring_parent_id: uuid.UUID | None
    is_recurring_template: bool

    # Operational timestamps
    actual_pickup_time: datetime | None
    patient_contact_time: datetime | None
    actual_destination_time: datetime | None
    completed_at: datetime | None
    cancelled_at: datetime | None
    cancellation_reason: str | None

    # Metadata
    notes: str | None
    internal_notes: str | None
    extra_metadata: dict[str, Any] = Field(default_factory=dict, alias="extra_metadata")

    # Audit fields
    version: int
    created_at: datetime
    updated_at: datetime


class TransportListResponse(BaseModel):
    """Paginated list of transports"""

    items: list[TransportResponse]
    total: int
    limit: int
    offset: int


class TransportSummaryResponse(BaseModel):
    """Condensed transport summary for lists"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    transport_number: str
    facility_id: uuid.UUID
    patient_name: str
    pickup_location: str
    destination: str
    appointment_time: datetime | None
    scheduled_pickup_time: datetime | None
    transport_type: TransportType
    status: TransportStatus
    priority_level: int
    assigned_unit_id: str | None
    created_at: datetime
    updated_at: datetime


class TransportSummaryListResponse(BaseModel):
    """Paginated list of transport summaries"""

    items: list[TransportSummaryResponse]
    total: int
    limit: int
    offset: int


# ============================================================================
# TRANSPORT NOTE SCHEMAS
# ============================================================================


class TransportNoteCreateRequest(BaseModel):
    """Request to add a note to transport"""

    note_text: str = Field(min_length=1)
    note_type: str = Field(default="general", max_length=32)
    is_internal: bool = Field(default=False)

    @field_validator("note_text")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("note_text must not be empty")
        return normalized


class TransportNoteResponse(BaseModel):
    """Transport note response"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    transport_id: uuid.UUID
    tenant_id: uuid.UUID
    author_user_id: uuid.UUID
    author_name: str
    note_text: str
    note_type: str
    is_internal: bool
    created_at: datetime


# ============================================================================
# RECURRING TRANSPORT SCHEMAS
# ============================================================================


class RecurringTransportCreateRequest(BaseModel):
    """Request to create recurring transport series"""

    template: TransportCreateRequest
    recurrence_rule: str = Field(
        description="RRULE format (e.g., 'FREQ=WEEKLY;BYDAY=MO,WE,FR;COUNT=12')"
    )
    generate_count: int = Field(
        default=4,
        ge=1,
        le=52,
        description="Number of future instances to generate initially",
    )


class RecurringTransportResponse(BaseModel):
    """Response for recurring transport creation"""

    template_id: uuid.UUID
    recurrence_rule: str
    generated_transports: list[TransportResponse]
    total_generated: int


# ============================================================================
# DASHBOARD/ANALYTICS SCHEMAS
# ============================================================================


class TransportScheduleDayView(BaseModel):
    """Daily schedule view for dashboard"""

    date: datetime
    total_transports: int
    by_status: dict[TransportStatus, int]
    by_facility: dict[uuid.UUID, int]
    urgent_count: int
    unassigned_count: int


class FacilityTransportStats(BaseModel):
    """Transport statistics for a facility"""

    facility_id: uuid.UUID
    facility_name: str
    total_transports: int
    completed: int
    cancelled: int
    in_progress: int
    avg_completion_time_minutes: float | None
    on_time_percentage: float | None


# ============================================================================
# DOCUMENT REQUIREMENT SCHEMAS
# ============================================================================


class TransportDocumentRequirementUpsertRequest(BaseModel):
    """Request to create or update a document requirement"""

    document_code: str = Field(min_length=1, max_length=64)
    document_name: str = Field(min_length=1, max_length=255)
    required_for_phase: str = Field(
        default="pre_pickup",
        description="Phase when document is required: pre_pickup, in_transit, or handoff"
    )
    source_scope: str = Field(
        default="sending",
        description="Scope of document source: sending, receiving, or shared"
    )
    is_blocking: bool = Field(default=True)
    due_at: datetime | None = None
    external_reference: str | None = Field(default=None, max_length=255)
    extra_metadata: dict = Field(default_factory=dict)


class TransportDocumentReceiveRequest(BaseModel):
    """Request to mark a document as received"""

    external_reference: str | None = Field(default=None, max_length=255)
    extra_metadata: dict = Field(default_factory=dict)


class TransportDocumentChaseRequest(BaseModel):
    """Request to chase/follow up on a document"""

    reason: str = Field(min_length=1, max_length=500)
    chase_channel: str = Field(
        default="manual",
        description="Channel for chase: portal, phone, fax, hl7, or manual"
    )
    extra_metadata: dict = Field(default_factory=dict)


class TransportDocumentRequirementResponse(BaseModel):
    """Response for document requirement"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    transport_id: uuid.UUID
    document_code: str
    document_name: str
    required_for_phase: str
    source_scope: str
    status: str
    is_blocking: bool
    due_at: datetime | None
    received_at: datetime | None
    received_by_user_id: uuid.UUID | None
    waived_at: datetime | None
    waiver_reason: str | None
    last_chased_at: datetime | None
    chase_count: int
    external_reference: str | None
    extra_metadata: dict
    created_at: datetime
    updated_at: datetime


# ============================================================================
# TRANSPORT READINESS SCHEMAS
# ============================================================================


class TransportReadinessCheckpointUpsertRequest(BaseModel):
    """Request to create or update a readiness checkpoint"""

    checkpoint_type: str = Field(
        description="Type of checkpoint: sending or receiving"
    )
    status: str = Field(
        description="Status: pending, ready, or blocked"
    )
    summary: str | None = Field(default=None, max_length=1000)
    blocker_codes: list[str] = Field(default_factory=list)
    extra_metadata: dict = Field(default_factory=dict)


class TransportReadinessCheckpointResponse(BaseModel):
    """Response for readiness checkpoint"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    transport_id: uuid.UUID
    checkpoint_type: str
    status: str
    summary: str | None
    blocker_codes: list
    acknowledged_at: datetime | None
    acknowledged_by_user_id: uuid.UUID | None
    extra_metadata: dict
    created_at: datetime
    updated_at: datetime


class TransportReadinessPublicationRequest(BaseModel):
    """Request to publish readiness to downstream systems"""

    downstream_systems: list[str] = Field(
        min_length=1,
        description="Downstream systems: cad, care, billing"
    )
    response_data: dict = Field(default_factory=dict)


class TransportReadinessPublicationResponse(BaseModel):
    """Response for readiness publication"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    transport_id: uuid.UUID
    downstream_system: str
    readiness_state: str
    payload: dict
    published_at: datetime
    published_by_user_id: uuid.UUID | None
    correlation_id: str | None
    acknowledged: bool
    response_data: dict


class TransportContinuityTimelineEventResponse(BaseModel):
    """Response for transport continuity timeline event"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    transport_id: uuid.UUID
    event_type: str
    event_category: str
    message: str
    event_payload: dict
    actor_user_id: uuid.UUID | None
    occurred_at: datetime


class TransportReadinessResponse(BaseModel):
    """Response for transport readiness status"""

    transport_id: uuid.UUID
    readiness_state: str = Field(description="ready or blocked")
    packet_complete: bool
    pickup_ready: bool
    transfer_ready: bool
    blockers: list[str] = Field(default_factory=list)
    required_documents: list[TransportDocumentRequirementResponse] = Field(
        default_factory=list
    )
    checkpoints: list[TransportReadinessCheckpointResponse] = Field(
        default_factory=list
    )
    publications: list[TransportReadinessPublicationResponse] = Field(
        default_factory=list
    )


