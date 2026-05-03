"""MDT (Mobile Data Terminal) contracts for Adaptix platform.

MDT provides field units with real-time CAD case display, unit status updates,
crew assignment display, incident notes, and map/route display.
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class UnitStatus(str, Enum):
    AVAILABLE = "available"
    EN_ROUTE = "en_route"
    ARRIVED = "arrived"
    TRANSPORTING = "transporting"
    AT_DESTINATION = "at_destination"
    CLEAR = "clear"
    OUT_OF_SERVICE = "out_of_service"
    STAGING = "staging"


class MDTUnitStatusUpdate(BaseModel):
    """Unit status update from MDT."""
    unit_id: str
    tenant_id: str
    actor_id: str
    case_id: Optional[str] = None
    status: UnitStatus
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    notes: Optional[str] = None
    updated_at: datetime
    idempotency_key: Optional[str] = None


class MDTCaseAssignment(BaseModel):
    """CAD case assignment displayed on MDT."""
    case_id: str
    tenant_id: str
    unit_id: str
    incident_type: Optional[str] = None
    priority: Optional[str] = None
    location: Optional[str] = None
    chief_complaint: Optional[str] = None
    dispatch_notes: Optional[str] = None
    crew_members: list[str] = []
    assigned_at: datetime
    cad_sync_at: Optional[datetime] = None


class MDTIncidentNote(BaseModel):
    """Incident note created from MDT."""
    note_id: str
    case_id: str
    unit_id: str
    tenant_id: str
    actor_id: str
    note_text: str
    created_at: datetime
    phi_safe: bool = True


class MDTRouteRequest(BaseModel):
    """Route/map request from MDT."""
    unit_id: str
    tenant_id: str
    origin_lat: float
    origin_lon: float
    destination_lat: float
    destination_lon: float
    provider_status: str = "credential_gated"


class MDTRouteResponse(BaseModel):
    """Route response for MDT display."""
    unit_id: str
    route_available: bool
    provider_status: str
    estimated_minutes: Optional[int] = None
    distance_miles: Optional[float] = None
    credential_gated: bool = False
    credential_gated_reason: Optional[str] = None


class MDTOfflineState(BaseModel):
    """Offline state for Android MDT."""
    unit_id: str
    tenant_id: str
    last_sync_at: Optional[datetime] = None
    pending_status_updates: int = 0
    pending_notes: int = 0
    offline_since: Optional[datetime] = None
    sync_required: bool = False
