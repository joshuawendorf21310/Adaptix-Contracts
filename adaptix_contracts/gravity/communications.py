"""
GRAVITY COMMUNICATIONS CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from .modules import GravityAIRunPayload


class EmailThreadState(str, Enum):
    OPEN = "open"
    SNOOZED = "snoozed"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class SMSThreadState(str, Enum):
    OPEN = "open"
    RESOLVED = "resolved"
    OPTED_OUT = "opted_out"
    BLOCKED = "blocked"


class CallState(str, Enum):
    COMPLETED = "completed"
    MISSED = "missed"
    VOICEMAIL = "voicemail"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"


class EmailMessageResponse(BaseModel):
    id: str
    thread_id: str
    from_address: str
    from_name: Optional[str] = None
    to_addresses: List[str]
    subject: str
    body_preview: str
    delivery_state: str
    sent_at: Optional[datetime] = None
    received_at: Optional[datetime] = None
    has_attachments: bool
    phi_warning: bool


class EmailThreadResponse(BaseModel):
    id: str
    tenant_id: str
    subject: str
    state: EmailThreadState
    priority: str
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    participant_count: int
    message_count: int
    last_message_at: datetime
    snoozed_until: Optional[datetime] = None
    messages: List[EmailMessageResponse] = []
    ai_suggestion: Optional[GravityAIRunPayload] = None
    tags: List[str] = []
    phi_warning: bool = False
    created_at: datetime
    updated_at: datetime


class EmailThreadListItemResponse(BaseModel):
    id: str
    subject: str
    state: EmailThreadState
    priority: str
    assignee_name: Optional[str] = None
    message_count: int
    last_message_at: datetime
    has_ai_suggestion: bool
    phi_warning: bool


class SendEmailRequest(BaseModel):
    thread_id: Optional[str] = None
    to_addresses: List[str]
    subject: str
    body_html: str
    reply_to_message_id: Optional[str] = None


class SMSMessageResponse(BaseModel):
    id: str
    thread_id: str
    direction: str
    body: str
    delivery_state: str
    sent_at: datetime
    phi_warning: bool


class SMSThreadResponse(BaseModel):
    id: str
    tenant_id: str
    phone_number: str
    contact_name: Optional[str] = None
    state: SMSThreadState
    message_count: int
    last_message_at: datetime
    messages: List[SMSMessageResponse] = []
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    opt_in_status: str
    created_at: datetime
    updated_at: datetime


class SendSMSRequest(BaseModel):
    thread_id: Optional[str] = None
    phone_number: str
    body: str


class PhoneCallResponse(BaseModel):
    id: str
    tenant_id: str
    phone_number: str
    contact_name: Optional[str] = None
    direction: str
    state: CallState
    disposition: Optional[str] = None
    duration_seconds: Optional[int] = None
    patient_id: Optional[str] = None
    patient_name: Optional[str] = None
    notes: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    created_at: datetime


class DispositionCallRequest(BaseModel):
    disposition: str
    notes: Optional[str] = None


class CommunicationActionResponse(BaseModel):
    audit_event_id: str
