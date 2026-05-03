"""TransportLink signature contracts for Adaptix platform.

Covers PCS, AOB, ABN, and combined signature packet workflows.
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class SignaturePacketStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    PARTIALLY_SIGNED = "partially_signed"
    COMPLETED = "completed"
    DECLINED = "declined"
    EXPIRED = "expired"
    ERROR = "error"
    MANUAL_OVERRIDE = "manual_override"
    CREDENTIAL_GATED = "credential_gated"


class SignatureDocumentType(str, Enum):
    PCS = "pcs"  # Physician Certification Statement
    AOB = "aob"  # Assignment of Benefits
    ABN = "abn"  # Advance Beneficiary Notice
    COMBINED = "combined"  # Combined signature packet


class SignerStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    VIEWED = "viewed"
    SIGNED = "signed"
    DECLINED = "declined"


class SignaturePacketRequest(BaseModel):
    request_id: str
    tenant_id: str
    actor_id: str
    document_types: list[SignatureDocumentType]
    patient_name: str
    payer: Optional[str] = None
    idempotency_key: Optional[str] = None


class SignaturePacketResponse(BaseModel):
    packet_id: str
    request_id: str
    tenant_id: str
    status: SignaturePacketStatus
    provider_request_id: Optional[str] = None
    sign_url: Optional[str] = None
    document_types: list[SignatureDocumentType]
    created_at: datetime
    credential_gated: bool = False
    credential_gated_reason: Optional[str] = None


class SignatureStatusResponse(BaseModel):
    packet_id: str
    request_id: str
    tenant_id: str
    status: SignaturePacketStatus
    signers: list[dict] = []
    signed_document_url: Optional[str] = None
    completed_at: Optional[datetime] = None
    ready_for_cad: bool = False
    ready_for_billing: bool = False
    blocking_reasons: list[str] = []


class SignatureManualOverrideRequest(BaseModel):
    request_id: str
    tenant_id: str
    actor_id: str
    supervisor_id: Optional[str] = None
    reason: str
    document_type: SignatureDocumentType
    override_justification: str


class SignatureManualOverrideResponse(BaseModel):
    override_id: str
    request_id: str
    tenant_id: str
    actor_id: str
    document_type: SignatureDocumentType
    reason: str
    audit_event_emitted: bool = True
    occurred_at: datetime


class SignatureWebhookEvent(BaseModel):
    event_type: str
    provider: str = "dropbox_sign"
    provider_request_id: str
    tenant_id: Optional[str] = None
    idempotency_key: str
    received_at: datetime
    payload: dict[str, Any] = {}
