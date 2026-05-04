"""
GRAVITY NOTIFICATIONS CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK

Authoritative contracts for the unified notification system.
All modules route user-visible action feedback through this system.
"""

from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from .modules import GravityNotificationSeverity, GravityNotificationState


class NotificationCreateRequest(BaseModel):
    tenant_id: str
    title: str
    message: Optional[str] = None
    severity: GravityNotificationSeverity
    module: str
    source_record_id: Optional[str] = None
    source_record_type: Optional[str] = None
    action_url: Optional[str] = None


class NotificationResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    message: Optional[str] = None
    severity: GravityNotificationSeverity
    state: GravityNotificationState
    module: str
    source_record_id: Optional[str] = None
    source_record_type: Optional[str] = None
    action_url: Optional[str] = None
    created_at: datetime
    read_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    snoozed_until: Optional[datetime] = None
    escalated_at: Optional[datetime] = None
    audit_event_id: Optional[str] = None


class NotificationListResponse(BaseModel):
    items: List[NotificationResponse]
    total: int
    unread_count: int


class NotificationSnoozeRequest(BaseModel):
    snoozed_until: datetime


class NotificationActionResponse(BaseModel):
    notification: NotificationResponse
    audit_event_id: str
