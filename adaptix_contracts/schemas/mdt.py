"""
MDT (Mobile Data Terminal) Schemas
Pydantic schemas for request/response validation
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from adaptix_contracts.types.enums import (
    AvailabilityStatus,
    MdtStatus,
    MessagePriority,
    NoteType,
    ResourceRequestStatus,
    UnitStatusCode,
)

# ========== SESSION SCHEMAS ==========


class MdtSessionStartRequest(BaseModel):
    """Request to start an MDT session"""
    unit_id: uuid.UUID
    device_id: str = Field(min_length=1, max_length=255)
    device_metadata: dict = Field(default_factory=dict)


class MdtSessionEndRequest(BaseModel):
    """Request to end an MDT session"""
    session_id: uuid.UUID


class MdtSessionResponse(BaseModel):
    """MDT session response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    unit_id: uuid.UUID
    user_id: uuid.UUID
    device_id: str
    login_time: datetime
    logout_time: datetime | None
    status: MdtStatus
    last_activity_at: datetime
    device_metadata: dict | None = Field(default_factory=dict)
    session_metadata: dict | None = Field(default_factory=dict)
    created_at: datetime | None = None
    updated_at: datetime


# ========== UNIT STATUS SCHEMAS ==========


class LocationData(BaseModel):
    """Location data for unit status updates"""
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    heading: float | None = Field(default=None, ge=0, lt=360)
    speed: float | None = Field(default=None, ge=0)
    altitude: float | None = None
    accuracy: float | None = None


class UnitStatusUpdateRequest(BaseModel):
    """Request to update unit status"""
    status: UnitStatusCode
    location: LocationData | None = None
    location_metadata: dict = Field(default_factory=dict)


class UnitStatusResponse(BaseModel):
    """Unit status response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    unit_id: uuid.UUID
    status: UnitStatusCode
    location_lat: float | None
    location_lon: float | None
    heading: float | None
    speed: float | None
    status_changed_at: datetime
    status_changed_by: uuid.UUID
    location_metadata: dict
    created_at: datetime
    updated_at: datetime


# ========== LOCATION TRACKING SCHEMAS ==========


class LocationUpdateRequest(BaseModel):
    """Request to update unit location"""
    location: LocationData
    location_metadata: dict = Field(default_factory=dict)


class LocationHistoryResponse(BaseModel):
    """Location history response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    unit_id: uuid.UUID
    session_id: uuid.UUID | None
    latitude: float
    longitude: float
    heading: float | None
    speed: float | None
    altitude: float | None
    accuracy: float | None
    recorded_at: datetime
    location_metadata: dict
    created_at: datetime


# ========== MESSAGE SCHEMAS ==========


class MdtMessageSendRequest(BaseModel):
    """Request to send an MDT message"""
    to_unit_id: uuid.UUID | None = None
    to_user_id: uuid.UUID | None = None
    message_text: str = Field(min_length=1, max_length=10000)
    priority: MessagePriority = MessagePriority.ROUTINE
    incident_id: uuid.UUID | None = None
    message_metadata: dict = Field(default_factory=dict)


class MdtMessageAcknowledgeRequest(BaseModel):
    """Request to acknowledge a message"""
    message_id: uuid.UUID


class MdtMessageResponse(BaseModel):
    """MDT message response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    from_user_id: uuid.UUID | None
    to_unit_id: uuid.UUID | None
    to_user_id: uuid.UUID | None
    message_text: str
    priority: MessagePriority
    read_at: datetime | None
    acknowledged_at: datetime | None
    incident_id: uuid.UUID | None
    message_metadata: dict
    created_at: datetime
    updated_at: datetime


class MdtMessageListResponse(BaseModel):
    """List of MDT messages"""
    items: list[MdtMessageResponse]
    total: int


# ========== INCIDENT NOTE SCHEMAS ==========


class IncidentNoteCreateRequest(BaseModel):
    """Request to create an incident note"""
    incident_id: uuid.UUID
    note_text: str = Field(min_length=1, max_length=50000)
    note_type: NoteType = NoteType.SCENE_NOTE
    note_metadata: dict = Field(default_factory=dict)


class IncidentNoteResponse(BaseModel):
    """Incident note response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    incident_id: uuid.UUID
    user_id: uuid.UUID
    note_text: str
    note_type: NoteType
    device_id: str | None
    session_id: uuid.UUID | None
    note_metadata: dict
    created_at: datetime
    updated_at: datetime


class IncidentNoteListResponse(BaseModel):
    """List of incident notes"""
    items: list[IncidentNoteResponse]
    total: int


# ========== RESOURCE REQUEST SCHEMAS ==========


class ResourceRequestCreateRequest(BaseModel):
    """Request to create a resource request"""
    incident_id: uuid.UUID
    requesting_unit_id: uuid.UUID
    resource_type: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=1, default=1)
    priority: MessagePriority = MessagePriority.ROUTINE
    reason: str | None = None
    request_metadata: dict = Field(default_factory=dict)


class ResourceRequestUpdateRequest(BaseModel):
    """Request to update resource request status"""
    status: ResourceRequestStatus


class ResourceRequestResponse(BaseModel):
    """Resource request response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    incident_id: uuid.UUID
    requesting_unit_id: uuid.UUID
    requesting_user_id: uuid.UUID
    resource_type: str
    quantity: int
    priority: MessagePriority
    reason: str | None
    status: ResourceRequestStatus
    approved_by: uuid.UUID | None
    approved_at: datetime | None
    fulfilled_at: datetime | None
    fulfilled_by: uuid.UUID | None
    request_metadata: dict
    created_at: datetime
    updated_at: datetime


class ResourceRequestListResponse(BaseModel):
    """List of resource requests"""
    items: list[ResourceRequestResponse]
    total: int


# ========== AVAILABLE UNIT SCHEMAS ==========


class NearbyUnitsQuery(BaseModel):
    """Query parameters for finding nearby units"""
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    radius_miles: float = Field(ge=0.1, le=100, default=25)
    unit_type: str | None = None
    required_capabilities: list[str] = Field(default_factory=list)


class AvailableUnitResponse(BaseModel):
    """Available unit response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    unit_id: uuid.UUID
    unit_name: str
    unit_type: str
    capabilities: list
    certifications: list
    current_location_lat: float | None
    current_location_lon: float | None
    location_updated_at: datetime | None
    availability_status: AvailabilityStatus
    eta_minutes: int | None
    current_assignment_id: uuid.UUID | None
    unit_metadata: dict
    active: bool
    created_at: datetime
    updated_at: datetime


class AvailableUnitListResponse(BaseModel):
    """List of available units"""
    items: list[AvailableUnitResponse]
    total: int


# ========== UNIT ASSIGNMENT SCHEMAS ==========


class UnitAssignmentResponse(BaseModel):
    """Unit assignment response"""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    unit_id: uuid.UUID
    incident_id: uuid.UUID
    assigned_at: datetime
    assigned_by: uuid.UUID
    acknowledged_at: datetime | None
    en_route_at: datetime | None
    on_scene_at: datetime | None
    cleared_at: datetime | None
    assignment_role: str
    active: bool
    assignment_metadata: dict
    created_at: datetime
    updated_at: datetime


class UnitAssignmentListResponse(BaseModel):
    """List of unit assignments"""
    items: list[UnitAssignmentResponse]
    total: int


# ========== INCIDENT DETAIL SCHEMAS (MDT View) ==========


class IncidentLocationData(BaseModel):
    """Location data for an incident"""
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    cross_streets: str | None = None
    location_notes: str | None = None


class IncidentDetailsForMdt(BaseModel):
    """Incident details optimized for MDT display"""
    id: uuid.UUID
    incident_number: str
    dispatch_time: datetime | None
    arrival_time: datetime | None
    disposition: str | None
    status: str
    location: IncidentLocationData | None
    chief_complaint: str | None = None
    priority: str | None = None
    units_assigned: list[uuid.UUID] = Field(default_factory=list)
    notes_count: int = 0
    resource_requests_count: int = 0
    created_at: datetime
    updated_at: datetime


# ========== TRACKING AND ANALYTICS SCHEMAS ==========


class UnitActivitySummary(BaseModel):
    """Summary of unit activity"""
    unit_id: uuid.UUID
    unit_name: str
    current_status: UnitStatusCode
    status_duration_minutes: int
    last_location: LocationData | None
    last_location_update: datetime | None
    active_assignment: uuid.UUID | None
    incidents_today: int
    time_on_scene_minutes: int


class MdtHealthCheckResponse(BaseModel):
    """MDT health check response"""
    active_sessions: int
    available_units: int
    units_on_call: int
    pending_resource_requests: int
    unread_messages: int
    system_status: str = "operational"
