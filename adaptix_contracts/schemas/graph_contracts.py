"""Graph (Microsoft Graph integration) domain contracts.

Defines contracts for the Adaptix Graph Service: a stateless proxy
providing authenticated access to Microsoft Graph APIs for the
Founder Command dashboard — email, files, and calendar.

This service owns no persistent state. All contracts are pure
request/response types for cross-domain consumers.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Read contracts
# ---------------------------------------------------------------------------

class GraphEmailSummaryContract(BaseModel):
    """Summary of a single inbox email message."""

    message_id: str
    subject: str
    sender_address: str
    sender_name: Optional[str] = None
    received_at: datetime
    is_read: bool


class GraphEmailDetailContract(BaseModel):
    """Full detail for a single email message."""

    message_id: str
    subject: str
    sender_address: str
    sender_name: Optional[str] = None
    body_preview: str
    body_html: Optional[str] = None
    received_at: datetime
    is_read: bool


class GraphDriveFileContract(BaseModel):
    """Metadata for a single OneDrive/SharePoint file."""

    item_id: str
    name: str
    size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None
    last_modified_at: Optional[datetime] = None
    web_url: Optional[str] = None
    mime_type: Optional[str] = None


class GraphCalendarEventContract(BaseModel):
    """A single calendar event from Microsoft Graph."""

    event_id: str
    subject: str
    start_datetime: datetime
    end_datetime: datetime
    is_cancelled: bool = False
    attendees: List[str] = []


class GraphAvailabilitySlotContract(BaseModel):
    """A free time slot returned by availability check."""

    start: datetime
    end: datetime


class GraphServiceStatusContract(BaseModel):
    """Status of the Microsoft Graph integration configuration."""

    microsoft_graph_configured: bool
    status: str


# ---------------------------------------------------------------------------
# Request contracts
# ---------------------------------------------------------------------------

class GraphSendEmailRequest(BaseModel):
    """Request to send an email via Microsoft Graph."""

    to: str
    subject: str
    body: str
    body_type: str = "HTML"
    cc: List[str] = []
    bcc: List[str] = []


class GraphCreateCalendarEventRequest(BaseModel):
    """Request to create a calendar event via Microsoft Graph."""

    subject: str
    start: str
    end: str
    time_zone: str = "UTC"
    attendees: List[str] = []
    body: Optional[str] = None
