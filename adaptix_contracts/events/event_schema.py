"""
Event Schema Definitions for Adaptix Unified Operational Graph

This module defines all event types in the system using Pydantic models for
validation, serialization, and type safety. Each event represents a significant
state change in the EMS operational workflow.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventType(str, Enum):
    """All supported event types in Adaptix."""

    # Transport Events
    TRANSPORT_REQUEST_CREATED = "TransportRequestCreated"
    TRANSPORT_SCHEDULED = "TransportScheduled"
    TRANSPORT_PUSHED_TO_CAD = "TransportPushedToCAD"

    # Crew Events
    CREW_PAGE_SENT = "CrewPageSent"
    CREW_ASSIGNMENT_ACCEPTED = "CrewAssignmentAccepted"
    CREW_ASSIGNMENT_CREATED = "CrewAssignmentCreated"
    CREW_ASSIGNMENT_ACKNOWLEDGED = "CrewAssignmentAcknowledged"
    CREW_ASSIGNMENT_STATUS_CHANGED = "CrewAssignmentStatusChanged"
    CREW_ASSIGNMENT_COMPLETED = "CrewAssignmentCompleted"

    # Incident Events
    INCIDENT_CREATED = "IncidentCreated"
    INCIDENT_STATUS_CHANGED = "IncidentStatusChanged"

    # ePCR Events
    EPCR_REPORT_VALIDATED = "EpcrReportValidated"

    # Billing Events
    BILLING_CLAIM_GENERATED = "BillingClaimGenerated"
    BILLING_CLAIM_SUBMITTED = "BillingClaimSubmitted"

    # Fire Events
    FIRE_INCIDENT_CREATED = "FireIncidentCreated"

    # HEMS Events
    HEMS_TRANSPORT_REQUESTED = "HemsTransportRequested"
    HEMS_LAUNCHED = "HemsLaunched"

    # Scheduling Events
    SCHEDULE_PUBLISHED = "SchedulePublished"
    SHIFT_ASSIGNED = "ShiftAssigned"
    SCHEDULE_SHIFT_STARTED = "ScheduleShiftStarted"
    SCHEDULE_SHIFT_ENDED = "ScheduleShiftEnded"
    SCHEDULE_SHIFT_CALLOUT = "ScheduleShiftCallout"
    SCHEDULE_SHIFT_SWAP = "ScheduleShiftSwap"
    SCHEDULE_OVERTIME_STARTED = "ScheduleOvertimeStarted"

    # Transport Events (lifecycle)
    TRANSPORT_COMPLETED = "TransportCompleted"

    # Billing Events (charge capture)
    BILLING_CHARGE_CAPTURED = "BillingChargeCaptured"

    # HEMS Events (flight operations)
    HEMS_MISSION_COMPLETED = "HemsMissionCompleted"

    # Inventory Events
    INVENTORY_LOW_STOCK = "InventoryLowStock"
    INVENTORY_RESTOCK_ORDERED = "InventoryRestockOrdered"
    NARCOTIC_DISCREPANCY = "NarcoticDiscrepancy"

    # MDT Events
    MDT_STATUS_CHANGED = "MdtStatusChanged"
    MDT_UNIT_LOCATION_UPDATED = "MdtUnitLocationUpdated"
    MDT_MESSAGE_SENT = "MdtMessageSent"


class BaseEvent(BaseModel):
    """
    Base event schema with common fields for all events.

    All events in Adaptix inherit from this base model to ensure
    consistent structure, validation, and traceability.
    """

    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this event instance",
    )

    event_type: str = Field(
        ...,
        description="Type of event (e.g., TransportRequestCreated)",
    )

    event_version: str = Field(
        default="1.0",
        description="Schema version for backward compatibility",
    )

    tenant_id: uuid.UUID = Field(
        ...,
        description="Tenant/organization ID for multi-tenancy isolation",
    )

    correlation_id: str | None = Field(
        default=None,
        description="Correlation ID for tracking related events across the system",
    )

    causation_id: str | None = Field(
        default=None,
        description="ID of the event that caused this event (event sourcing)",
    )

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp when event was created",
    )

    source: str = Field(
        default="adaptix.core",
        description="Source system or module that generated the event",
    )

    actor_id: uuid.UUID | None = Field(
        default=None,
        description="User or system actor that triggered the event",
    )

    actor_type: str | None = Field(
        default=None,
        description="Type of actor (user, system, integration)",
    )

    idempotency_key: str | None = Field(
        default=None,
        description="Idempotency key for duplicate prevention",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context and metadata for the event",
    )

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "event_id": "550e8400-e29b-41d4-a716-446655440000",
            "event_type": "TransportRequestCreated",
            "event_version": "1.0",
            "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
            "timestamp": "2026-03-23T10:30:00Z",
            "source": "Adaptix.transport",
        }
    })

    @field_validator("timestamp", mode="before")
    @classmethod
    def ensure_utc_timestamp(cls, v):
        """Ensure timestamp is always UTC."""
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            from dateutil import parser
            return parser.isoparse(v)
        return v


# ================================
# Transport Events
# ================================


class TransportRequestCreated(BaseEvent):
    """Event published when a new transport request is created."""

    event_type: Literal[EventType.TRANSPORT_REQUEST_CREATED] = EventType.TRANSPORT_REQUEST_CREATED
    source: str = "Adaptix.transport"

    transport_id: uuid.UUID = Field(..., description="Unique transport request ID")
    patient_id: uuid.UUID | None = Field(None, description="Patient ID if known")
    pickup_location: str = Field(..., description="Pickup address or facility")
    destination: str = Field(..., description="Destination address or facility")
    transport_type: str = Field(..., description="Type: emergency, non-emergency, scheduled")
    priority: int = Field(..., ge=1, le=5, description="Priority level 1-5 (1=highest)")
    requested_by: str | None = Field(None, description="Who requested the transport")
    scheduled_time: datetime | None = Field(None, description="Scheduled pickup time")


class TransportScheduled(BaseEvent):
    """Event published when a transport is scheduled and assigned to a unit."""

    event_type: Literal[EventType.TRANSPORT_SCHEDULED] = EventType.TRANSPORT_SCHEDULED
    source: str = "Adaptix.transport"

    transport_id: uuid.UUID
    unit_id: uuid.UUID = Field(..., description="Assigned unit/vehicle ID")
    scheduled_pickup: datetime = Field(..., description="Scheduled pickup time")
    estimated_duration_minutes: int | None = Field(None, description="Estimated trip duration")


class TransportPushedToCAD(BaseEvent):
    """Event published when transport details are pushed to CAD system."""

    event_type: Literal[EventType.TRANSPORT_PUSHED_TO_CAD] = EventType.TRANSPORT_PUSHED_TO_CAD
    source: str = "Adaptix.transport"

    transport_id: uuid.UUID
    cad_incident_number: str = Field(..., description="CAD incident/call number")
    cad_system: str = Field(..., description="CAD system identifier")
    push_status: str = Field(..., description="Success, failure, or pending")


# ================================
# Crew Events
# ================================


class CrewPageSent(BaseEvent):
    """Event published when crew notification page is sent."""

    event_type: Literal[EventType.CREW_PAGE_SENT] = EventType.CREW_PAGE_SENT
    source: str = "Adaptix.crewlink"

    page_id: uuid.UUID = Field(..., description="Unique page notification ID")
    transport_id: uuid.UUID | None = Field(None, description="Related transport ID")
    incident_id: uuid.UUID | None = Field(None, description="Related incident ID")
    crew_member_ids: list[uuid.UUID] = Field(..., description="List of crew member IDs paged")
    page_method: str = Field(..., description="Method: sms, push, email, voice")
    message_content: str = Field(..., description="Page message content")


class CrewAssignmentAccepted(BaseEvent):
    """Event published when a crew member accepts an assignment."""

    event_type: Literal[EventType.CREW_ASSIGNMENT_ACCEPTED] = EventType.CREW_ASSIGNMENT_ACCEPTED
    source: str = "Adaptix.crewlink"

    assignment_id: uuid.UUID = Field(..., description="Assignment ID")
    transport_id: uuid.UUID | None = Field(None, description="Related transport ID")
    incident_id: uuid.UUID | None = Field(None, description="Related incident ID")
    crew_member_id: uuid.UUID = Field(..., description="Crew member who accepted")
    accepted_at: datetime = Field(..., description="Acceptance timestamp")
    response_time_seconds: int | None = Field(None, description="Time to accept from page sent")


class CrewAssignmentCreatedEvent(BaseEvent):
    """Event published when a crew assignment is created."""

    event_type: Literal[EventType.CREW_ASSIGNMENT_CREATED] = EventType.CREW_ASSIGNMENT_CREATED
    source: str = "Adaptix.crewlink"

    incident_id: uuid.UUID = Field(..., description="Related incident ID")
    assignment_id: uuid.UUID = Field(..., description="Assignment ID")
    crew_member_ids: list[uuid.UUID] = Field(default_factory=list, description="Assigned crew members")
    unit_id: uuid.UUID | None = Field(None, description="Assigned unit ID")
    priority: str = Field(..., description="Assignment priority")


class CrewAssignmentAcknowledgedEvent(BaseEvent):
    """Event published when a crew member acknowledges an assignment."""

    event_type: Literal[EventType.CREW_ASSIGNMENT_ACKNOWLEDGED] = EventType.CREW_ASSIGNMENT_ACKNOWLEDGED
    source: str = "Adaptix.crewlink"

    assignment_id: uuid.UUID = Field(..., description="Assignment ID")
    crew_member_id: uuid.UUID = Field(..., description="Crew member acknowledging the assignment")
    incident_id: uuid.UUID | None = Field(None, description="Related incident ID")
    response: str = Field(..., description="ACCEPT, DECLINE, or UNAVAILABLE")
    eta_minutes: int | None = Field(None, description="Estimated minutes to arrive")


class CrewAssignmentStatusChangedEvent(BaseEvent):
    """Event published when an assignment/unit status changes."""

    event_type: Literal[EventType.CREW_ASSIGNMENT_STATUS_CHANGED] = EventType.CREW_ASSIGNMENT_STATUS_CHANGED
    source: str = "Adaptix.crewlink"

    assignment_id: uuid.UUID = Field(..., description="Assignment ID")
    crew_member_id: uuid.UUID = Field(..., description="Crew member updating status")
    incident_id: uuid.UUID | None = Field(None, description="Related incident ID")
    new_status: str = Field(..., description="Updated assignment status")
    latitude: float | None = Field(None, description="Current latitude")
    longitude: float | None = Field(None, description="Current longitude")


# ================================
# Incident Events
# ================================


class IncidentCreated(BaseEvent):
    """Event published when a new incident is created in CAD."""

    event_type: Literal[EventType.INCIDENT_CREATED] = EventType.INCIDENT_CREATED
    source: str = "Adaptix.cad"

    incident_id: uuid.UUID = Field(..., description="Unique incident ID")
    incident_number: str = Field(..., description="Human-readable incident number")
    incident_type: str = Field(..., description="Type: medical, fire, rescue, etc.")
    location: str = Field(..., description="Incident location address")
    priority: int = Field(..., ge=1, le=5, description="Priority level")
    dispatched_units: list[str] = Field(default_factory=list, description="Units dispatched")


class IncidentStatusChanged(BaseEvent):
    """Event published when incident status changes."""

    event_type: Literal[EventType.INCIDENT_STATUS_CHANGED] = EventType.INCIDENT_STATUS_CHANGED
    source: str = "Adaptix.cad"

    incident_id: uuid.UUID
    incident_number: str
    old_status: str = Field(..., description="Previous status")
    new_status: str = Field(..., description="New status")
    status_reason: str | None = Field(None, description="Reason for status change")


# ================================
# ePCR Events
# ================================


class EpcrReportValidated(BaseEvent):
    """Event published when ePCR report passes validation."""

    event_type: Literal[EventType.EPCR_REPORT_VALIDATED] = EventType.EPCR_REPORT_VALIDATED
    source: str = "Adaptix.epcr"

    epcr_id: uuid.UUID = Field(..., description="ePCR report ID")
    incident_id: uuid.UUID = Field(..., description="Related incident ID")
    patient_id: uuid.UUID = Field(..., description="Patient ID")
    validation_status: str = Field(..., description="Validation status: passed, warnings")
    nemsis_compliant: bool = Field(..., description="NEMSIS 3.5.1 compliance status")
    completed_by: uuid.UUID = Field(..., description="Crew member who completed report")


# ================================
# Billing Events
# ================================


class BillingClaimGenerated(BaseEvent):
    """Event published when a billing claim is auto-generated."""

    event_type: Literal[EventType.BILLING_CLAIM_GENERATED] = EventType.BILLING_CLAIM_GENERATED
    source: str = "Adaptix.billing"

    claim_id: uuid.UUID = Field(..., description="Billing claim ID")
    epcr_id: uuid.UUID = Field(..., description="Source ePCR ID")
    incident_id: uuid.UUID = Field(..., description="Related incident ID")
    patient_id: uuid.UUID = Field(..., description="Patient ID")
    claim_amount: float = Field(..., description="Claim amount in dollars")
    payer_type: str = Field(..., description="Payer type: medicare, medicaid, commercial, etc.")


class BillingClaimSubmitted(BaseEvent):
    """Event published when billing claim is submitted to clearinghouse."""

    event_type: Literal[EventType.BILLING_CLAIM_SUBMITTED] = EventType.BILLING_CLAIM_SUBMITTED
    source: str = "Adaptix.billing"

    claim_id: uuid.UUID
    submission_id: str = Field(..., description="Clearinghouse submission ID")
    clearinghouse: str = Field(..., description="Clearinghouse name")
    submitted_at: datetime = Field(..., description="Submission timestamp")
    batch_id: str | None = Field(None, description="Batch ID if part of batch submission")


# ================================
# Fire Events
# ================================


class FireIncidentCreated(BaseEvent):
    """Event published when a fire incident is created."""

    event_type: Literal[EventType.FIRE_INCIDENT_CREATED] = EventType.FIRE_INCIDENT_CREATED
    source: str = "Adaptix.fire"

    fire_incident_id: uuid.UUID = Field(..., description="Fire incident ID")
    incident_id: uuid.UUID | None = Field(None, description="Related CAD incident ID")
    incident_number: str = Field(..., description="Fire incident number")
    incident_type: str = Field(..., description="Type: structure, vehicle, wildland, etc.")
    alarm_level: int = Field(..., ge=1, le=5, description="Alarm level")
    location: str = Field(..., description="Fire location address")


# ================================
# HEMS Events
# ================================


class HemsTransportRequested(BaseEvent):
    """Event published when HEMS transport is requested."""

    event_type: Literal[EventType.HEMS_TRANSPORT_REQUESTED] = EventType.HEMS_TRANSPORT_REQUESTED
    source: str = "Adaptix.hems"

    hems_request_id: uuid.UUID = Field(..., description="HEMS request ID")
    incident_id: uuid.UUID = Field(..., description="Related incident ID")
    patient_id: uuid.UUID | None = Field(None, description="Patient ID if known")
    request_reason: str = Field(..., description="Reason for air transport")
    pickup_location: str = Field(..., description="Pickup location coordinates or address")
    destination: str = Field(..., description="Destination facility")


class HemsLaunched(BaseEvent):
    """Event published when HEMS aircraft is launched."""

    event_type: Literal[EventType.HEMS_LAUNCHED] = EventType.HEMS_LAUNCHED
    source: str = "Adaptix.hems"

    hems_request_id: uuid.UUID
    aircraft_id: str = Field(..., description="Aircraft call sign or ID")
    launch_time: datetime = Field(..., description="Launch timestamp")
    estimated_arrival_minutes: int | None = Field(None, description="ETA in minutes")
    crew_members: list[str] = Field(default_factory=list, description="Crew member names")


# ================================
# Scheduling Events
# ================================


class SchedulePublished(BaseEvent):
    """Event published when crew schedule is published."""

    event_type: Literal[EventType.SCHEDULE_PUBLISHED] = EventType.SCHEDULE_PUBLISHED
    source: str = "Adaptix.scheduling"

    schedule_id: uuid.UUID = Field(..., description="Schedule ID")
    schedule_period: str = Field(..., description="Schedule period (e.g., '2026-03-01 to 2026-03-31')")
    published_by: uuid.UUID = Field(..., description="User who published schedule")
    affected_crew_members: list[uuid.UUID] = Field(
        default_factory=list, description="Crew members affected by schedule"
    )


class ShiftAssigned(BaseEvent):
    """Event published when a shift is assigned to a crew member."""

    event_type: Literal[EventType.SHIFT_ASSIGNED] = EventType.SHIFT_ASSIGNED
    source: str = "Adaptix.scheduling"

    shift_id: uuid.UUID = Field(..., description="Shift ID")
    crew_member_id: uuid.UUID = Field(..., description="Assigned crew member ID")
    shift_start: datetime = Field(..., description="Shift start time")
    shift_end: datetime = Field(..., description="Shift end time")
    unit_id: uuid.UUID | None = Field(None, description="Assigned unit/vehicle ID")
    position: str | None = Field(None, description="Position: paramedic, EMT, driver, etc.")


# ================================
# Inventory Events
# ================================


class InventoryLowStock(BaseEvent):
    """Event published when inventory item falls below threshold."""

    event_type: Literal[EventType.INVENTORY_LOW_STOCK] = EventType.INVENTORY_LOW_STOCK
    source: str = "Adaptix.inventory"

    item_id: uuid.UUID = Field(..., description="Inventory item ID")
    item_name: str = Field(..., description="Item name")
    item_category: str = Field(..., description="Item category: medical, equipment, etc.")
    current_quantity: int = Field(..., description="Current quantity in stock")
    threshold_quantity: int = Field(..., description="Minimum threshold quantity")
    location: str | None = Field(None, description="Storage location")


class NarcoticDiscrepancy(BaseEvent):
    """Event published when narcotic inventory discrepancy is detected."""

    event_type: Literal[EventType.NARCOTIC_DISCREPANCY] = EventType.NARCOTIC_DISCREPANCY
    source: str = "Adaptix.inventory"

    discrepancy_id: uuid.UUID = Field(..., description="Discrepancy report ID")
    drug_name: str = Field(..., description="Narcotic drug name")
    expected_quantity: int = Field(..., description="Expected quantity")
    actual_quantity: int = Field(..., description="Actual quantity counted")
    discrepancy_amount: int = Field(..., description="Discrepancy (expected - actual)")
    location: str = Field(..., description="Storage location or unit")
    detected_by: uuid.UUID | None = Field(None, description="User who detected discrepancy")


# ================================
# MDT Events
# ================================


class MdtStatusChanged(BaseEvent):
    """Event published when MDT unit status changes."""

    event_type: Literal[EventType.MDT_STATUS_CHANGED] = EventType.MDT_STATUS_CHANGED
    source: str = "Adaptix.mdt"

    unit_id: uuid.UUID = Field(..., description="Unit/vehicle ID")
    device_id: str = Field(..., description="MDT device identifier")
    old_status: str = Field(..., description="Previous status")
    new_status: str = Field(
        ..., description="New status: available, dispatched, enroute, on_scene, transporting, etc."
    )
    location_lat: float | None = Field(None, description="GPS latitude")
    location_lon: float | None = Field(None, description="GPS longitude")
    crew_members: list[uuid.UUID] = Field(default_factory=list, description="Current crew members")


class MdtUnitLocationUpdated(BaseEvent):
    """Event published when MDT unit location is updated."""

    event_type: Literal[EventType.MDT_UNIT_LOCATION_UPDATED] = EventType.MDT_UNIT_LOCATION_UPDATED
    source: str = "Adaptix.mdt"

    unit_id: uuid.UUID = Field(..., description="Unit/vehicle ID")
    latitude: float = Field(..., description="GPS latitude")
    longitude: float = Field(..., description="GPS longitude")
    heading: float | None = Field(None, description="Heading in degrees")
    speed_mph: float | None = Field(None, description="Speed in MPH")


class MdtMessageSent(BaseEvent):
    """Event published when an MDT message is sent."""

    event_type: Literal[EventType.MDT_MESSAGE_SENT] = EventType.MDT_MESSAGE_SENT
    source: str = "Adaptix.mdt"

    message_id: uuid.UUID = Field(..., description="MDT message ID")
    unit_id: uuid.UUID = Field(..., description="Unit sending/receiving")
    priority: str = Field(default="normal", description="Message priority")


# ================================
# Scheduling Lifecycle Events (Phase 5)
# ================================


class ScheduleShiftStartedEvent(BaseEvent):
    """Event published when a shift starts."""

    event_type: Literal[EventType.SCHEDULE_SHIFT_STARTED] = EventType.SCHEDULE_SHIFT_STARTED
    source: str = "Adaptix.scheduling"

    shift_id: uuid.UUID
    crew_member_id: uuid.UUID
    unit_id: uuid.UUID | None = None
    shift_start: datetime | None = None
    shift_end: datetime | None = None
    position: str | None = None


class ScheduleShiftEndedEvent(BaseEvent):
    """Event published when a shift ends."""

    event_type: Literal[EventType.SCHEDULE_SHIFT_ENDED] = EventType.SCHEDULE_SHIFT_ENDED
    source: str = "Adaptix.scheduling"

    shift_id: uuid.UUID
    crew_member_id: uuid.UUID
    unit_id: uuid.UUID | None = None


class ScheduleShiftCalloutEvent(BaseEvent):
    """Event published when a crew member calls out of a shift."""

    event_type: Literal[EventType.SCHEDULE_SHIFT_CALLOUT] = EventType.SCHEDULE_SHIFT_CALLOUT
    source: str = "Adaptix.scheduling"

    shift_id: uuid.UUID
    crew_member_id: uuid.UUID
    reason: str = ""
    callout_at: datetime | None = None


class ScheduleShiftSwapEvent(BaseEvent):
    """Event published when a shift swap is completed."""

    event_type: Literal[EventType.SCHEDULE_SHIFT_SWAP] = EventType.SCHEDULE_SHIFT_SWAP
    source: str = "Adaptix.scheduling"

    shift_id: uuid.UUID
    offering_crew_id: uuid.UUID
    receiving_crew_id: uuid.UUID
    swap_date: str = ""


# ================================
# Transport Lifecycle Events (Phase 5)
# ================================


class TransportCompletedEvent(BaseEvent):
    """Event published when a transport completes."""

    event_type: Literal[EventType.TRANSPORT_COMPLETED] = EventType.TRANSPORT_COMPLETED
    source: str = "Adaptix.transportlink"

    transport_id: uuid.UUID
    transport_type: str = ""
    loaded_miles: float = 0.0
    service_level: str = ""
    patient_id: uuid.UUID | None = None
    completed_at: datetime | None = None


class BillingChargeCapturedEvent(BaseEvent):
    """Event published when billing charge is auto-captured from transport."""

    event_type: Literal[EventType.BILLING_CHARGE_CAPTURED] = EventType.BILLING_CHARGE_CAPTURED
    source: str = "Adaptix.billing"

    claim_id: uuid.UUID
    transport_id: uuid.UUID
    total_amount: float = 0.0
    hcpcs_codes: list[str] = Field(default_factory=list)
    line_count: int = 0


# ================================
# HEMS Flight Events (Phase 5)
# ================================


class HemsMissionCompletedEvent(BaseEvent):
    """Event published when a HEMS mission completes with flight data."""

    event_type: Literal[EventType.HEMS_MISSION_COMPLETED] = EventType.HEMS_MISSION_COMPLETED
    source: str = "Adaptix.hems"

    mission_id: uuid.UUID
    aircraft_id: uuid.UUID | None = None
    flight_time_minutes: int | None = None
    loaded_miles: float | None = None
    billing_codes: list[str] = Field(default_factory=list)


# ================================
# Inventory Events (Phase 5)
# ================================


class InventoryRestockOrdered(BaseEvent):
    """Event published when a restocking PO is created."""

    event_type: Literal[EventType.INVENTORY_RESTOCK_ORDERED] = EventType.INVENTORY_RESTOCK_ORDERED
    source: str = "Adaptix.inventory"

    purchase_order_id: uuid.UUID
    supplier_id: uuid.UUID | None = None
    item_count: int = 0
    total_cost: float = 0.0


# Type alias for all event types
EventModel = (
    TransportRequestCreated
    | TransportScheduled
    | TransportPushedToCAD
    | CrewPageSent
    | CrewAssignmentAccepted
    | CrewAssignmentCreatedEvent
    | CrewAssignmentAcknowledgedEvent
    | CrewAssignmentStatusChangedEvent
    | IncidentCreated
    | IncidentStatusChanged
    | EpcrReportValidated
    | BillingClaimGenerated
    | BillingClaimSubmitted
    | FireIncidentCreated
    | HemsTransportRequested
    | HemsLaunched
    | SchedulePublished
    | ShiftAssigned
    | ScheduleShiftStartedEvent
    | ScheduleShiftEndedEvent
    | ScheduleShiftCalloutEvent
    | ScheduleShiftSwapEvent
    | TransportCompletedEvent
    | BillingChargeCapturedEvent
    | HemsMissionCompletedEvent
    | InventoryLowStock
    | InventoryRestockOrdered
    | NarcoticDiscrepancy
    | MdtStatusChanged
    | MdtUnitLocationUpdated
    | MdtMessageSent
)
