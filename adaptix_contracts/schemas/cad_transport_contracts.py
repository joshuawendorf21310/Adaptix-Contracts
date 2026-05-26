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


class CadTransportLinkStatus(str, Enum):
    """Lifecycle status for the durable CAD/TransportLink link record."""

    VISIBLE = "visible"
    DISPATCH_READY = "dispatch_ready"
    ACTIVATED = "activated"
    SYNCING = "syncing"
    COMPLETED = "completed"
    UNLINKED = "unlinked"
    ERROR = "error"


class CadTransportLinkContract(BaseModel):
    """Shared cross-domain shape for the durable CAD link record."""

    trip_id: str
    request_id: str
    tenant_id: str
    status: CadTransportLinkStatus
    patient_name: Optional[str] = None
    transport_type: Optional[str] = None
    level_of_care: Optional[str] = None
    pickup_facility_name: Optional[str] = None
    destination_facility_name: Optional[str] = None
    scheduled_pickup_at: Optional[datetime] = None
    unit_id: Optional[str] = None
    cad_case_id: Optional[str] = None
    activated_at: Optional[datetime] = None
    last_synced_at: Optional[datetime] = None
    error_detail: Optional[str] = None


class CadDispatchReadyEntryContract(BaseModel):
    """Shared queue shape for trips that have passed all readiness gates."""

    trip_id: str
    request_id: str
    tenant_id: str
    patient_name: str
    transport_type: str
    pickup_facility_name: str
    scheduled_pickup_at: datetime
    unit_id: Optional[str] = None
    readiness_confirmed_at: datetime
    minutes_until_pickup: Optional[int] = None
    removed: bool = False
    removed_at: Optional[datetime] = None


class CadTransportExceptionEntryContract(BaseModel):
    """Shared exception-queue shape for blocked CAD-visible transports."""

    trip_id: str
    request_id: str
    tenant_id: str
    patient_name: str
    scheduled_pickup_at: datetime
    exception_type: str
    exception_reason: str
    blocking_gates: list[str] = Field(default_factory=list)
    flagged_at: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class CadTransportStatusSyncContract(BaseModel):
    """Shared immutable sync-history shape for CAD to TransportLink updates."""

    trip_id: str
    tenant_id: str
    new_status: str
    unit_id: Optional[str] = None
    operator_note: Optional[str] = None
    synced_at: datetime
    transport_accepted: bool = False
    transport_timeline_event_id: Optional[str] = None


class ScheduledTransportLaneItem(BaseModel):
    """Read contract for a single trip in the CAD scheduled transport lane."""

    trip_id: str
    request_id: str
    tenant_id: str

    patient_name: str
    transport_type: str
    level_of_care: str

    pickup_facility_name: str
    destination_facility_name: str

    scheduled_pickup_at: datetime
    scheduled_dropoff_at: Optional[datetime] = None

    unit_id: Optional[str] = None
    crew_ids: list[str]

    readiness_state: str
    documents_ready: bool
    signature_complete: bool
    authorization_status: Optional[str] = None

    lane_status: CadTransportLaneStatus
    minutes_until_pickup: Optional[int] = None


class DispatchReadyItem(BaseModel):
    """Read contract for a trip that has met all readiness gates."""

    trip_id: str
    request_id: str
    tenant_id: str

    patient_name: str
    transport_type: str
    level_of_care: str

    pickup_facility_name: str
    destination_facility_name: str

    scheduled_pickup_at: datetime

    unit_id: Optional[str] = None
    crew_ids: list[str]

    readiness_confirmed_at: datetime
    minutes_until_pickup: int


class CadTransportException(BaseModel):
    """Read contract for a transport trip with unresolved blockers."""

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
    operator_note: Optional[str] = Field(default=None, max_length=500)


class CadTransportActivateResponse(BaseModel):
    """Response contract for transport activation in CAD."""

    trip_id: str
    cad_case_id: Optional[str] = None
    activated_at: datetime
    status: str


class CadTransportSyncPayload(BaseModel):
    """Contract for CAD pushing a status update back to TransportLink."""

    trip_id: str
    tenant_id: str
    new_status: str
    unit_id: Optional[str] = None
    synced_at: datetime
    operator_note: Optional[str] = None


class CadTransportSyncResponse(BaseModel):
    """Confirmation that TransportLink accepted the status sync."""

    trip_id: str
    transport_status_updated: bool
    timeline_event_id: Optional[str] = None
    accepted_at: datetime


class TransportActivatedEvent(BaseModel):
    """Published when CAD activates a transport into operational state."""

    event_type: str = "cad.transport.activated"

    trip_id: str
    request_id: str
    tenant_id: str
    cad_case_id: Optional[str] = None

    activated_at: datetime


class TransportStatusSyncedEvent(BaseModel):
    """Published when CAD syncs a transport status change back to TransportLink."""

    event_type: str = "cad.transport.status_synced"

    trip_id: str
    request_id: str
    tenant_id: str
    new_status: str

    synced_at: datetime
