"""Voice domain cross-domain contracts."""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class VoiceRoomCreatedEvent(BaseModel):
    """Published when a voice room is created for an incident."""
    room_id: UUID
    tenant_id: UUID
    incident_id: UUID
    case_id: UUID
    room_name: str
    created_at: datetime

class VoiceRoomClosedEvent(BaseModel):
    """Published when a voice room is closed."""
    room_id: UUID
    tenant_id: UUID
    incident_id: UUID
    closed_at: datetime
    participant_count: int
