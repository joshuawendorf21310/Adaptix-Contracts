"""
GRAVITY INCIDENTS CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from .modules import GravityAIRunPayload


class IncidentState(str, Enum):
    ACTIVE = "active"
    ESCALATED = "escalated"
    DE_ESCALATED = "de_escalated"
    CLOSED = "closed"
    REOPENED = "reopened"


class IncidentPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentResourceResponse(BaseModel):
    id: str
    incident_id: str
    resource_type: str
    resource_id: str
    resource_label: str
    assigned_at: datetime
    released_at: Optional[datetime] = None


class IncidentTimelineEventResponse(BaseModel):
    id: str
    incident_id: str
    timestamp: datetime
    event_type: str
    description: str
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None
    severity: Optional[str] = None


class IncidentLinkResponse(BaseModel):
    id: str
    incident_id: str
    linked_type: str
    linked_id: str
    linked_label: Optional[str] = None


class IncidentResponse(BaseModel):
    id: str
    tenant_id: str
    record_id: str
    title: str
    description: Optional[str] = None
    state: IncidentState
    priority: IncidentPriority
    patient_count: int = 0
    scene_address: Optional[str] = None
    scene_lat: Optional[float] = None
    scene_lng: Optional[float] = None
    cad_call_id: Optional[str] = None
    resources: List[IncidentResourceResponse] = []
    links: List[IncidentLinkResponse] = []
    timeline: List[IncidentTimelineEventResponse] = []
    ai_summary: Optional[GravityAIRunPayload] = None
    command_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    actor_id: str
    version: int


class IncidentListItemResponse(BaseModel):
    id: str
    title: str
    state: IncidentState
    priority: IncidentPriority
    patient_count: int
    scene_address: Optional[str] = None
    resource_count: int
    created_at: datetime
    updated_at: datetime


class CreateIncidentRequest(BaseModel):
    title: str
    description: Optional[str] = None
    priority: IncidentPriority
    scene_address: Optional[str] = None
    patient_count: int = 0


class UpdateIncidentRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[IncidentPriority] = None
    command_notes: Optional[str] = None
    version: int


class EscalateIncidentRequest(BaseModel):
    reason: str


class CloseIncidentRequest(BaseModel):
    resolution_note: Optional[str] = None


class AssignResourceRequest(BaseModel):
    resource_type: str
    resource_id: str
    resource_label: str


class IncidentActionResponse(BaseModel):
    incident: IncidentResponse
    audit_event_id: str
