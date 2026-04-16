"""Fire domain contract schemas for cross-domain communication."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FireIncidentCreatedEvent(BaseModel):
    """Published when a fire incident is created."""

    event_type: str = "fire.incident.created"

    incident_id: str
    tenant_id: str
    incident_number: str

    address: str
    incident_type: str

    created_at: datetime


class FireIncidentStatusUpdatedEvent(BaseModel):
    """Published when fire incident status changes."""

    event_type: str = "fire.incident.status_updated"

    incident_id: str
    tenant_id: str
    incident_number: str

    old_status: str
    new_status: str

    updated_at: datetime


class FireIncidentContract(BaseModel):
    """Read-only fire incident contract for cross-domain consumption."""

    id: str
    tenant_id: str

    incident_number: str
    address: str
    incident_type: str

    status: str
    created_at: datetime


class NerisReadinessContract(BaseModel):
    """NERIS export readiness status for a fire incident."""

    incident_id: str

    ready: bool

    missing_fields: list[str] = Field(default_factory=list)
    filled_fields: list[str] = Field(default_factory=list)

    total_required: int
    total_filled: int
