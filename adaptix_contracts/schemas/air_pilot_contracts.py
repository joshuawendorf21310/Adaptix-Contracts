"""Air pilot domain cross-domain contracts."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PilotGoNoGoEvent(BaseModel):
    """Published when a go/no-go decision is made."""

    event_type: str = "air_pilot.go_no_go_decision"

    decision_id: UUID
    tenant_id: UUID
    pilot_id: UUID
    mission_request_id: Optional[UUID]

    decision: str  # go, no_go, conditional
    evaluated_at: datetime

    fatigue_go: Optional[bool]
    medical_go: Optional[bool]
    proficiency_go: Optional[bool]
    weather_go: Optional[bool]


class PilotReadinessStatus(BaseModel):
    """Pilot readiness summary for cross-domain consumption."""

    pilot_id: UUID
    tenant_id: UUID

    overall_readiness: str  # ready, restricted, grounded
    duty_hours_last_24h: float
    medical_valid: bool
    proficiency_current: bool
