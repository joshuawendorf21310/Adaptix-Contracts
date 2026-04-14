"""CAD transport lane contract schemas for cross-domain communication.

Defines all typed contracts for CAD's visibility into scheduled transports:
scheduled lanes, dispatch-ready queues, exception queues, activation,
and bidirectional status synchronization with TransportLink.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CadTransportLaneStatus(str, Enum):
    """Visibility status of a transport trip within CAD lanes."""

    SCHEDULED = "scheduled"
    DISPATCH_READY = "dispatch_ready"
    ACTIVATED = "activated"
    EXCEPTION = "exception"
    CANCELLED = "cancelled"


class ScheduledTransportLaneItem(BaseModel):
    """Read contract for a single trip in the CAD scheduled transport lane.

    Displayed in the upcoming transport lane. Not a noisy popup.
    Provides dispatcher with full context without interrupting active operations.
    """

    trip_id: str
    request_id: str
    tenant_id: str
    patient_name: str
    transport_type: str
    level_of_care: str
    pickup_facility_name: str
    destination_facility_name: str
    scheduled_pickup_at: datetime
    scheduled_dropoff_at: Optional[datetime]
    unit_id: Optional[str]
    crew_ids: list[str]
    readiness_state: str
    documents_ready: bool
    signature_complete: bool
    authorization_status: Optional[str]
    lane_status: CadTransportLaneStatus
    minutes_until_pickup: Optional[int]


class DispatchReadyItem(BaseModel):
    """Read contract for a trip that has met all readiness gates.

    Only appears in dispatch-ready queue when all gates pass:
    - documents ready
    - signatures complete
    - authorization resolved
    - unit available
    """

    trip_id: str
    request_id: str
    tenant_id: str
    patient_name: str
    transport_type: str
    level_of_care: str
    pickup_facility_name: str
    destination_facility_name: str
    scheduled_pickup_at: datetime
    unit_id: Optional[str]
    crew_ids: list[str]
    readiness_confirmed_at: datetime
    minutes_until_pickup: int


class CadTransportException(BaseModel):
    """Read contract for a transport trip with unresolved blockers.

    Appears in the exception queue requiring dispatcher attention.
    """

    trip_id: str
    request_id: str
    tenant_id: str
    patient_name: str
    scheduled_pickup_at: datetime
    exception_type: str
    exception_reason: str
    flagged_at: datetime
    blocking_gates: list[str]


class CadTransportActivateRequest(BaseModel):
    """Contract for activating a dispatch-ready transport into CAD operations."""

    trip_id: str
    assigned_unit_id: Optional[str] = None
    assigned_crew_ids: list[str] = Field(default_factory=list)
    operator_note: Optional[str] = Field(None, max_length=500)


class CadTransportActivateResponse(BaseModel):
    """Response contract for transport activation in CAD."""

    trip_id: str
    cad_case_id: Optional[str]
    activated_at: datetime
    status: str


class CadTransportSyncPayload(BaseModel):
    """Contract for CAD pushing a status update back to TransportLink.

    Sent when CAD changes trip status during active operations.
    TransportLink must reflect this in the transport timeline.
    """

    trip_id: str
    tenant_id: str
    new_status: str
    unit_id: Optional[str]
    synced_at: datetime
    operator_note: Optional[str]


class CadTransportSyncResponse(BaseModel):
    """Confirmation that TransportLink accepted the status sync."""

    trip_id: str
    transport_status_updated: bool
    timeline_event_id: Optional[str]
    accepted_at: datetime


class TransportActivatedEvent(BaseModel):
    """Published when CAD activates a transport into operational state."""

    event_type: str = "cad.transport.activated"
    trip_id: str
    request_id: str
    tenant_id: str
    cad_case_id: Optional[str]
    activated_at: datetime


class TransportStatusSyncedEvent(BaseModel):
    """Published when CAD syncs a transport status change back to TransportLink."""

    event_type: str = "cad.transport.status_synced"
    trip_id: str
    request_id: str
    tenant_id: str
    new_status: str
    synced_at: datetime
