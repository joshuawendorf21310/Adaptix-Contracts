"""Calendar conflict contracts shared by TransportLink and Workforce."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .event import AdaptixCalendarProduct


class AdaptixCalendarConflictReason(str, Enum):
    """Conflict reason codes used for backend validation and rollback."""

    RESOURCE_DOUBLE_BOOKED = "resource_double_booked"
    TENANT_MISMATCH = "tenant_mismatch"
    READINESS_BLOCKED = "readiness_blocked"
    CERTIFICATION_BLOCKED = "certification_blocked"
    FATIGUE_BLOCKED = "fatigue_blocked"
    LOCKED_EVENT = "locked_event"
    VERSION_CONFLICT = "version_conflict"


class AdaptixCalendarConflict(BaseModel):
    """Conflict payload returned by domain calendar validation APIs."""

    id: str
    tenant_id: str = Field(alias="tenantId")
    product: AdaptixCalendarProduct
    event_id: str = Field(alias="eventId")
    conflicting_event_id: str | None = Field(default=None, alias="conflictingEventId")
    resource_id: str | None = Field(default=None, alias="resourceId")
    reason: AdaptixCalendarConflictReason
    message: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }