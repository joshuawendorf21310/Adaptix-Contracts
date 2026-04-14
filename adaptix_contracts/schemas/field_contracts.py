"""Field domain cross-domain contracts."""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class UnitStatusEvent(BaseModel):
    """Published when a field unit changes status."""
    unit_id: UUID
    tenant_id: UUID
    unit_identifier: str
    previous_status: Optional[str]
    new_status: str
    incident_id: Optional[UUID]
    occurred_at: datetime

class UnitTelemetryEvent(BaseModel):
    """Published when unit telemetry is updated."""
    unit_id: UUID
    tenant_id: UUID
    lat: float
    lon: float
    speed_kmh: Optional[float]
    recorded_at: datetime
