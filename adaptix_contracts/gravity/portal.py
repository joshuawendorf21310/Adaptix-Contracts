"""
GRAVITY PORTAL CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class PortalDocumentState(str, Enum):
    REQUESTED = "requested"
    PENDING = "pending"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    RESUBMISSION_REQUIRED = "resubmission_required"


class PortalDocumentRequestResponse(BaseModel):
    id: str
    tenant_id: str
    patient_id: str
    document_type: str
    title: str
    description: Optional[str] = None
    required: bool
    state: PortalDocumentState
    rejection_reason: Optional[str] = None
    due_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PortalDocumentStatusResponse(BaseModel):
    total_required: int
    submitted: int
    accepted: int
    rejected: int
    pending: int
    completion_pct: float


class PortalDocumentListResponse(BaseModel):
    items: List[PortalDocumentRequestResponse]
    status: PortalDocumentStatusResponse


class PortalDocumentSubmissionResponse(BaseModel):
    id: str
    request_id: str
    patient_id: str
    file_name: str
    file_size_bytes: int
    mime_type: str
    state: str
    rejection_reason: Optional[str] = None
    submitted_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None


class PatientHomeResponse(BaseModel):
    """
    Aggregated patient home data.
    Single endpoint aggregates all patient-facing data.
    """
    patient_profile: dict
    open_actions: List[dict]
    invoice_summary: dict
    document_summary: PortalDocumentStatusResponse
    communication_summary: dict
    timeline: List[dict]
    alerts: List[dict]
    permissions: dict
