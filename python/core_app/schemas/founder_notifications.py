"""Pydantic schemas for Founder Notification System."""

from __future__ import annotations

from datetime import datetime, time
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Severity / Category literals
# ---------------------------------------------------------------------------

SeverityLevel = Literal["info", "warning", "critical", "emergency"]
NotificationCategory = Literal[
    "billing", "compliance", "infrastructure", "security", "operations", "custom",
]

# ---------------------------------------------------------------------------
# Notification Policy
# ---------------------------------------------------------------------------


class NotificationPolicyBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    category: NotificationCategory
    min_severity: SeverityLevel = "warning"
    channels: list[str] = Field(default_factory=lambda: ["sms"])
    enabled: bool = True
    quiet_hours_start: time | None = None
    quiet_hours_end: time | None = None
    quiet_hours_tz: str = "UTC"


class NotificationPolicyCreate(NotificationPolicyBase):
    tenant_id: UUID


class NotificationPolicyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    category: NotificationCategory | None = None
    min_severity: SeverityLevel | None = None
    channels: list[str] | None = None
    enabled: bool | None = None
    quiet_hours_start: time | None = None
    quiet_hours_end: time | None = None
    quiet_hours_tz: str | None = None


class NotificationPolicyResponse(NotificationPolicyBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Notification Recipient
# ---------------------------------------------------------------------------


class NotificationRecipientBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    phone_e164: str = Field(min_length=10, max_length=20)
    email: str | None = Field(default=None, max_length=320)
    role: str | None = Field(default=None, max_length=100)
    categories: list[NotificationCategory] = Field(
        default_factory=lambda: ["billing", "compliance", "infrastructure", "security", "operations"],
    )
    min_severity: SeverityLevel = "warning"
    enabled: bool = True
    quiet_hours_start: time | None = None
    quiet_hours_end: time | None = None
    quiet_hours_tz: str = "UTC"


class NotificationRecipientCreate(NotificationRecipientBase):
    tenant_id: UUID


class NotificationRecipientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    phone_e164: str | None = Field(default=None, min_length=10, max_length=20)
    email: str | None = None
    role: str | None = None
    categories: list[NotificationCategory] | None = None
    min_severity: SeverityLevel | None = None
    enabled: bool | None = None
    quiet_hours_start: time | None = None
    quiet_hours_end: time | None = None
    quiet_hours_tz: str | None = None


class NotificationRecipientResponse(NotificationRecipientBase):
    id: UUID
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Test SMS / Test Critical Route
# ---------------------------------------------------------------------------


class NotificationTestRequest(BaseModel):
    recipient_phone: str = Field(min_length=10, max_length=20)
    message: str = Field(default="Adaptix test notification", max_length=500)
    category: NotificationCategory = "operations"
    severity: SeverityLevel = "info"


class NotificationTestResponse(BaseModel):
    success: bool
    delivered_count: int = 0
    message: str = ""
    event_id: UUID | None = None


# ---------------------------------------------------------------------------
# Alert Events (log of all processed alerts)
# ---------------------------------------------------------------------------


class AlertEventItem(BaseModel):
    id: UUID
    tenant_id: UUID
    source: str
    category: str
    severity: SeverityLevel
    fingerprint: str | None = None
    status: str
    title: str
    message: str | None = None
    raw_payload: dict[str, Any] | None = None
    delivered_count: int = 0
    acknowledged_at: datetime | None = None
    acknowledged_by: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertEventListResponse(BaseModel):
    events: list[AlertEventItem]
    total: int


class AlertEventAckRequest(BaseModel):
    acknowledged_by: str = Field(min_length=1, max_length=200)
    note: str | None = Field(default=None, max_length=1000)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class FounderNotificationHealthResponse(BaseModel):
    policy_count: int
    recipient_count: int
    active_events_count: int
    config_version: int
    provider_ok: bool
