"""Field domain cross-domain contracts."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UnitStatusEvent(BaseModel):
    """Published when a field unit changes status."""

    event_type: str = "field.unit.status_changed"

    unit_id: UUID
    tenant_id: UUID

    unit_identifier: str

    previous_status: Optional[str] = None
    new_status: str

    incident_id: Optional[UUID] = None

    occurred_at: datetime


class UnitTelemetryEvent(BaseModel):
    """Published when unit telemetry is updated."""

    event_type: str = "field.unit.telemetry_updated"

    unit_id: UUID
    tenant_id: UUID

    lat: float
    lon: float

    speed_kmh: Optional[float] = None

    recorded_at: datetime
