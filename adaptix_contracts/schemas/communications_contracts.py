"""Communications domain contract schemas for cross-domain communication."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NotificationRequest(BaseModel):
    """Request to send a notification via the communications domain."""

    tenant_id: str
    recipient_id: str

    channel: str = Field(..., description="email | sms | push")

    subject: Optional[str] = None
    body: str

    correlation_id: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None


class NotificationDeliveredEvent(BaseModel):
    """Published when a notification is confirmed delivered."""

    event_type: str = "communications.notification.delivered"

    notification_id: str
    tenant_id: str
    recipient_id: str

    channel: str
    delivered_at: datetime


class NotificationFailedEvent(BaseModel):
    """Published when a notification delivery fails."""

    event_type: str = "communications.notification.failed"

    notification_id: str
    tenant_id: str
    recipient_id: str

    channel: str
    failure_reason: str
    failed_at: datetime
