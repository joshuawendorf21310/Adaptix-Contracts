from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from adaptix_contracts.schemas.fire_contracts import (
    FireIncidentContract,
    FireIncidentCreatedEvent,
    FireIncidentStatusUpdatedEvent,
    FireOperationalEventContract,
    FirePatientCareLinkContract,
    NerisReadinessContract,
    ResourceExecutionContract,
    SceneStateSnapshotContract,
)


class FireIncidentType(StrEnum):
    STRUCTURE_FIRE = "STRUCTURE_FIRE"
    VEHICLE_FIRE = "VEHICLE_FIRE"
    WILDLAND_FIRE = "WILDLAND_FIRE"
    ALARM_ACTIVATION = "ALARM_ACTIVATION"
    HAZMAT = "HAZMAT"
    RESCUE = "RESCUE"
    EMS_ASSIST = "EMS_ASSIST"
    PUBLIC_ASSIST = "PUBLIC_ASSIST"
    MUTUAL_AID = "MUTUAL_AID"
    TRAINING_DRILL = "TRAINING_DRILL"
    INVESTIGATION = "INVESTIGATION"
    OTHER = "OTHER"


class FireUnitStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    DISPATCHED = "DISPATCHED"
    ENROUTE = "ENROUTE"
    ARRIVED = "ARRIVED"
    STAGED = "STAGED"
    ASSIGNED = "ASSIGNED"
    OPERATING = "OPERATING"
    REHAB = "REHAB"
    CLEARING = "CLEARING"
    RETURNING = "RETURNING"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    CANCELLED = "CANCELLED"


class FireCommandRoleType(StrEnum):
    INCIDENT_COMMAND = "INCIDENT_COMMAND"
    OPERATIONS = "OPERATIONS"
    SAFETY = "SAFETY"
    STAGING = "STAGING"
    WATER_SUPPLY = "WATER_SUPPLY"
    ACCOUNTABILITY = "ACCOUNTABILITY"
    REHAB = "REHAB"
    DIVISION = "DIVISION"
    GROUP = "GROUP"
    INVESTIGATION = "INVESTIGATION"
    EMS_LIAISON = "EMS_LIAISON"


class FireIncidentStatus(StrEnum):
    ACTIVE = "active"
    CONTAINED = "contained"
    UNDER_CONTROL = "under_control"
    MITIGATED = "mitigated"
    TERMINATED = "terminated"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class FireIncidentLocation(BaseModel):
    address: str
    latitude: float | None = None
    longitude: float | None = None
    jurisdiction: str | None = None
    station_response_area: str | None = None


class FireIncidentTimelineEvent(BaseModel):
    event_type: str
    occurred_at: datetime
    phase: str | None = None
    objective: str | None = None
    outcome: str | None = None
    source_kind: str = "user_entered_truth"
    details: dict[str, object] = Field(default_factory=dict)


class FireIncidentCommand(BaseModel):
    role_type: FireCommandRoleType
    assigned_to: str | None = None
    assigned_by: str | None = None
    objective: str | None = None
    assigned_at: datetime | None = None


class FireAuditEvent(BaseModel):
    event_type: str
    incident_id: str
    tenant_id: str
    actor_user_id: str | None = None
    occurred_at: datetime
    details: dict[str, object] = Field(default_factory=dict)


__all__ = [
    "FireCommandRoleType",
    "FireIncidentCommand",
    "FireIncidentContract",
    "FireIncidentCreatedEvent",
    "FireIncidentLocation",
    "FireIncidentStatus",
    "FireIncidentStatusUpdatedEvent",
    "FireIncidentTimelineEvent",
    "FireIncidentType",
    "FireOperationalEventContract",
    "FirePatientCareLinkContract",
    "FireAuditEvent",
    "FireUnitStatus",
    "NerisReadinessContract",
    "ResourceExecutionContract",
    "SceneStateSnapshotContract",
]