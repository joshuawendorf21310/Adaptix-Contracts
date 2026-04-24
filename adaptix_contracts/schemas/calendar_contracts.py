"""Shared calendar authority contracts for Adaptix Core."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CalendarAvailabilityResponse(BaseModel):
    """Current provider connectivity state for calendar sync."""

    microsoft_graph_configured: bool
    provider_name: str = "microsoft_graph"
    degraded: bool
    detail: str


class CalendarEventCreateRequest(BaseModel):
    """Request payload to create a platform-owned calendar event."""

    subject: str = Field(min_length=1, max_length=500)
    body: str | None = Field(default=None, max_length=4000)
    start_at: datetime
    end_at: datetime
    timezone_name: str = Field(default="UTC", min_length=1, max_length=100)
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class CalendarEventUpdateRequest(BaseModel):
    """Partial update payload for a platform-owned calendar event."""

    subject: str | None = Field(default=None, min_length=1, max_length=500)
    body: str | None = Field(default=None, max_length=4000)
    start_at: datetime | None = None
    end_at: datetime | None = None
    timezone_name: str | None = Field(default=None, min_length=1, max_length=100)
    metadata_json: dict[str, Any] | None = None


class CalendarEventResponse(BaseModel):
    """Calendar authority response payload."""

    id: str
    tenant_id: str
    owner_user_id: str | None = None
    subject: str
    body: str | None = None
    start_at: datetime
    end_at: datetime
    timezone_name: str
    status: str
    provider_name: str
    provider_event_id: str | None = None
    sync_status: str
    sync_error: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class CalendarAuditEntry(BaseModel):
    """Audit trail entry for calendar authority changes."""

    id: str
    calendar_event_id: str
    tenant_id: str
    user_id: str | None = None
    action: str
    details_json: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime