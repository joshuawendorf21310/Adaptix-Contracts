"""Air (HEMS) domain contract schemas for cross-domain communication."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AirMissionCreatedEvent(BaseModel):
    """Published when a HEMS mission is created."""

    event_type: str = "air.mission.created"
    mission_id: str
    tenant_id: str
    aircraft_id: str
    mission_type: str
    created_at: datetime


class AirMissionStatusUpdatedEvent(BaseModel):
    """Published when HEMS mission status changes."""

    event_type: str = "air.mission.status_updated"
    mission_id: str
    tenant_id: str
    old_status: str
    new_status: str
    updated_at: datetime


class AirMissionContract(BaseModel):
    """Read-only HEMS mission contract for cross-domain consumption."""

    id: str
    tenant_id: str
    aircraft_id: str
    mission_type: str
    status: str
    patient_count: int
    created_at: datetime


class AirLandingZoneContract(BaseModel):
    """Landing zone contract for cross-domain routing."""

    id: str
    tenant_id: str
    name: str
    latitude: float
    longitude: float
    is_active: bool
