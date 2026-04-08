import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from adaptix_contracts.types.enums import (
    AlertPriority,
    AssignmentAckStatus,
    AssignmentStatus,
    AssignmentType,
    AvailabilityType,
    DeliveryMethod,
    DeliveryStatus,
    PageStatus,
    PageType,
    UrgencyLevel,
)

# ── Page Schemas ──────────────────────────────────────────────────────────────


class PageCreateRequest(BaseModel):
    """Request to create a new page"""

    page_type: PageType
    urgency_level: UrgencyLevel
    subject: str = Field(min_length=1, max_length=255)
    message: str = Field(min_length=1)
    context_json: dict = Field(default_factory=dict)
    target_recipients: list[str] = Field(min_length=1)  # List of user_id strings
    delivery_channels: list[DeliveryMethod] = Field(
        default_factory=lambda: [DeliveryMethod.PUSH]
    )
    incident_id: uuid.UUID | None = None
    sla_minutes: int | None = Field(default=None, ge=1, le=1440)  # Max 24 hours

    @field_validator("target_recipients")
    @classmethod
    def validate_recipients(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("target_recipients must not be empty")
        # Validate UUID format
        for recipient in value:
            try:
                uuid.UUID(recipient)
            except ValueError as e:
                raise ValueError(
                    f"Invalid UUID in target_recipients: {recipient}"
                ) from e
        return value


class PageAcknowledgeRequest(BaseModel):
    """Request to acknowledge a page"""

    response: str | None = Field(default=None, max_length=255)


class PageRespondRequest(BaseModel):
    """Request to respond to a page (accept/decline)"""

    response: str = Field(min_length=1, max_length=255)
    response_metadata: dict = Field(default_factory=dict)


class PageRecipientResponse(BaseModel):
    """Response model for page recipient"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    page_id: uuid.UUID
    user_id: uuid.UUID
    delivery_method: DeliveryMethod
    delivery_status: DeliveryStatus
    delivered_at: datetime | None
    acknowledged_at: datetime | None
    response: str | None
    response_metadata: dict
    created_at: datetime
    updated_at: datetime


class PageResponse(BaseModel):
    """Response model for page"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    page_type: PageType
    urgency_level: UrgencyLevel
    subject: str
    message: str
    context_json: dict
    target_recipients: list
    delivery_channels: list
    status: PageStatus
    sla_expires_at: datetime | None
    acknowledged_at: datetime | None
    acknowledged_by: uuid.UUID | None
    escalated: bool
    incident_id: uuid.UUID | None
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime


class PageListResponse(BaseModel):
    """Paginated list of pages"""

    items: list[PageResponse]
    total: int
    limit: int
    offset: int


# ── Escalation Rule Schemas ───────────────────────────────────────────────────


class EscalationRuleCreateRequest(BaseModel):
    """Request to create escalation rule"""

    name: str = Field(min_length=1, max_length=255)
    trigger_condition: str = Field(min_length=1, max_length=64)
    wait_minutes: int = Field(ge=1, le=1440)
    escalation_recipients: list[str] = Field(min_length=1)
    escalation_channels: list[DeliveryMethod] = Field(
        default_factory=lambda: [DeliveryMethod.SMS, DeliveryMethod.VOICE]
    )
    applies_to_page_types: list[PageType] = Field(default_factory=list)
    applies_to_urgency: list[UrgencyLevel] = Field(default_factory=list)
    priority: int = Field(default=0, ge=0, le=100)

    @field_validator("escalation_recipients")
    @classmethod
    def validate_recipients(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("escalation_recipients must not be empty")
        for recipient in value:
            try:
                uuid.UUID(recipient)
            except ValueError as e:
                raise ValueError(
                    f"Invalid UUID in escalation_recipients: {recipient}"
                ) from e
        return value


class EscalationRuleUpdateRequest(BaseModel):
    """Request to update escalation rule"""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    trigger_condition: str | None = Field(default=None, min_length=1, max_length=64)
    wait_minutes: int | None = Field(default=None, ge=1, le=1440)
    escalation_recipients: list[str] | None = None
    escalation_channels: list[DeliveryMethod] | None = None
    applies_to_page_types: list[PageType] | None = None
    applies_to_urgency: list[UrgencyLevel] | None = None
    active: bool | None = None
    priority: int | None = Field(default=None, ge=0, le=100)


class EscalationRuleResponse(BaseModel):
    """Response model for escalation rule"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    trigger_condition: str
    wait_minutes: int
    escalation_recipients: list
    escalation_channels: list
    applies_to_page_types: list
    applies_to_urgency: list
    active: bool
    priority: int
    created_at: datetime
    updated_at: datetime


# ── Availability Schemas ──────────────────────────────────────────────────────


class AvailabilityUpdateRequest(BaseModel):
    """Request to update crew availability"""

    available: bool
    availability_type: AvailabilityType
    shift_id: uuid.UUID | None = None
    notes: str | None = Field(default=None, max_length=1000)
    effective_from: datetime
    effective_to: datetime | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("effective_from", "effective_to")
    @classmethod
    def ensure_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Datetime values must be timezone-aware.")
        return value


class AvailabilityResponse(BaseModel):
    """Response model for crew availability"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    user_id: uuid.UUID
    available: bool
    availability_type: AvailabilityType
    shift_id: uuid.UUID | None
    notes: str | None
    effective_from: datetime
    effective_to: datetime | None
    latitude: float | None
    longitude: float | None
    created_at: datetime
    updated_at: datetime


class AvailabilityListResponse(BaseModel):
    """List of availability records"""

    items: list[AvailabilityResponse]
    total: int


# ── Stats & Analytics ─────────────────────────────────────────────────────────


class PageStatsResponse(BaseModel):
    """Page statistics"""

    total_pages: int
    by_status: dict[str, int]
    by_urgency: dict[str, int]
    by_type: dict[str, int]
    avg_acknowledgment_time_seconds: float | None
    escalation_rate: float


# ── Assignment Schemas ───────────────────────────────────────────────────────


class AssignmentCreate(BaseModel):
    """Request to create a crew-to-incident assignment."""

    incident_id: uuid.UUID
    crew_member_ids: list[uuid.UUID] = Field(min_length=1)
    unit_id: uuid.UUID | None = None
    assignment_type: AssignmentType = AssignmentType.DISPATCH
    priority: AlertPriority = AlertPriority.NORMAL
    notes: str | None = Field(default=None, max_length=2000)


class AssignmentAck(BaseModel):
    """Acknowledgment payload for a crew assignment."""

    response: AssignmentAckStatus
    eta_minutes: int | None = Field(default=None, ge=0, le=1440)
    notes: str | None = Field(default=None, max_length=2000)


class AssignmentStatusUpdate(BaseModel):
    """Realtime assignment status update sent by the assigned crew."""

    status: AssignmentStatus
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("status")
    @classmethod
    def validate_status_transition(cls, value: AssignmentStatus) -> AssignmentStatus:
        allowed = {
            AssignmentStatus.EN_ROUTE,
            AssignmentStatus.ON_SCENE,
            AssignmentStatus.AVAILABLE,
            AssignmentStatus.AT_HOSPITAL,
        }
        if value not in allowed:
            raise ValueError(
                "status must be one of: EN_ROUTE, ON_SCENE, AVAILABLE, AT_HOSPITAL"
            )
        return value


class AssignmentResponse(BaseModel):
    """Crew assignment response with aggregated member acknowledgment state."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    incident_id: uuid.UUID
    crew_member_ids: list[uuid.UUID]
    unit_id: uuid.UUID | None
    assignment_type: AssignmentType
    priority: AlertPriority
    notes: str | None
    status: AssignmentStatus
    assigned_at: datetime
    assigned_by: uuid.UUID | None
    ack_status: dict[str, str]

