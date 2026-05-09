"""Calendar audit contracts shared by TransportLink and Workforce."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .event import AdaptixCalendarProduct


class AdaptixCalendarAuditAction(str, Enum):
    """Audited calendar mutations required by the reduced implementation."""

    CREATED = "created"
    MOVED = "moved"
    RESIZED = "resized"
    ASSIGNED = "assigned"
    LOCKED = "locked"
    PUBLISHED = "published"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    OVERRIDE = "override"


class AdaptixCalendarAuditEvent(BaseModel):
    """Immutable audit contract for calendar actions."""

    id: str
    tenant_id: str = Field(alias="tenantId")
    product: AdaptixCalendarProduct
    event_id: str = Field(alias="eventId")
    actor_id: str = Field(alias="actorId")
    action: AdaptixCalendarAuditAction
    correlation_id: str | None = Field(default=None, alias="correlationId")
    idempotency_key: str | None = Field(default=None, alias="idempotencyKey")
    details: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(alias="occurredAt")

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }