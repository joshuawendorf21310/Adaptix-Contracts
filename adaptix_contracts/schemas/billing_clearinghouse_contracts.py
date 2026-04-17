"""Billing clearinghouse integration contracts.

Defines all typed request/response/event contracts for external clearinghouse
interactions: claim submission, acknowledgements, remittance ingestion,
and error handling.

This layer isolates external vendor behavior (Office Ally, Availity, etc.)
from the core billing domain.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ClearinghouseProvider(str, Enum):
    """Supported clearinghouse providers."""

    OFFICE_ALLY = "office_ally"
    CHANGE_HEALTHCARE = "change_healthcare"
    AVAILITY = "availity"
    WAYSTAR = "waystar"
    OTHER = "other"


class SubmissionStatus(str, Enum):
    """Submission lifecycle at clearinghouse."""

    QUEUED = "queued"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ERROR = "error"


class AckType(str, Enum):
    """Type of clearinghouse acknowledgement."""

    TA1 = "ta1"  # interchange acknowledgment
    ACK_999 = "999"  # functional acknowledgment
    ACK_277CA = "277ca"  # claim acknowledgment
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Submission Contracts
# ---------------------------------------------------------------------------

class ClaimSubmissionRequest(BaseModel):
    """Request to submit a claim to a clearinghouse."""

    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    edi_payload: str = Field(..., description="X12 837 payload")

    submitted_by_user_id: Optional[str] = None


class ClaimSubmissionResponse(BaseModel):
    """Response after attempting submission to clearinghouse."""

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    status: SubmissionStatus

    external_reference_id: Optional[str] = None
    message: Optional[str] = None

    submitted_at: datetime


# ---------------------------------------------------------------------------
# Acknowledgements
# ---------------------------------------------------------------------------

class ClearinghouseAck(BaseModel):
    """Raw acknowledgement from clearinghouse."""

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    ack_type: AckType

    ack_code: str
    ack_message: Optional[str] = None

    accepted: bool
    received_at: datetime


class ClaimAckStatus(BaseModel):
    """Normalized claim status derived from acknowledgements."""

    claim_id: str
    tenant_id: str

    accepted: bool
    rejected: bool
    errors: list[str] = Field(default_factory=list)

    processed_at: datetime


# ---------------------------------------------------------------------------
# Remittance (ERA)
# ---------------------------------------------------------------------------

class RemittanceIngestRequest(BaseModel):
    """Incoming ERA (835) ingestion request."""

    tenant_id: str
    provider: ClearinghouseProvider

    raw_835_payload: str
    received_at: datetime


class RemittanceClaimPayment(BaseModel):
    """Payment detail for a single claim within a remittance."""

    claim_id: str
    paid_cents: int = Field(..., ge=0)
    adjusted_cents: int = Field(..., ge=0)

    payer_claim_control_number: Optional[str] = None


class RemittanceIngestResponse(BaseModel):
    """Result of ERA ingestion."""

    remit_id: str
    tenant_id: str

    claims_processed: int
    claims_failed: int

    processed_at: datetime


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class ClaimSubmittedToClearinghouseEvent(BaseModel):
    """Published when a claim is sent to a clearinghouse."""

    event_type: str = "billing.clearinghouse.submitted"

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    submitted_at: datetime


class ClearinghouseAckReceivedEvent(BaseModel):
    """Published when an acknowledgement is received."""

    event_type: str = "billing.clearinghouse.ack_received"

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    ack_type: AckType
    accepted: bool

    received_at: datetime


class RemittanceIngestedEvent(BaseModel):
    """Published when an ERA is successfully processed."""

    event_type: str = "billing.clearinghouse.remittance_ingested"

    remit_id: str
    tenant_id: str

    claims_processed: int
    processed_at: datetime
