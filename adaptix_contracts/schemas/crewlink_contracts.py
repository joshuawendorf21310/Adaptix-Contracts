"""CrewLink domain contract schemas for cross-domain communication."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CrewPageSentEvent(BaseModel):
    """Published when a page is sent to a crew member."""

    event_type: str = "crewlink.page.sent"
    page_id: str
    tenant_id: str
    crew_member_id: str
    incident_id: Optional[str] = None
    message: str
    sent_at: datetime


class CrewPageAcknowledgedEvent(BaseModel):
    """Published when a crew member acknowledges a page."""

    event_type: str = "crewlink.page.acknowledged"
    page_id: str
    tenant_id: str
    crew_member_id: str
    acknowledged_at: datetime


class CrewMemberContract(BaseModel):
    """Read-only crew member contract for cross-domain consumption."""

    id: str
    tenant_id: str
    employee_id: str
    first_name: str
    last_name: str
    is_active: bool


class CrewRosterSyncContract(BaseModel):
    """Roster synchronization payload for cross-domain sync."""

    tenant_id: str
    synced_at: datetime
    member_count: int
    active_count: int
