"""Billing domain core contracts for cross-domain communication.

Defines foundational billing entities, claim lifecycle, remittance,
payments, denials, clearinghouse interaction events, payer references,
and claim line-level billing details.

These contracts are the authoritative source for all billing domain
data exchanged across Adaptix services.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ClaimStatus(str, Enum):
    """Lifecycle status of a billing claim."""

    DRAFT = "draft"
    READY = "ready"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DENIED = "denied"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    CLOSED = "closed"


class DenialStatus(str, Enum):
    """Lifecycle status of a denial."""

    OPEN = "open"
    IN_APPEAL = "in_appeal"
    RESOLVED = "resolved"
    WRITTEN_OFF = "written_off"


class PaymentStatus(str, Enum):
    """Lifecycle status of a payment."""

    POSTED = "posted"
    PENDING = "pending"
    FAILED = "failed"


class ClearinghouseStatus(str, Enum):
    """Claim submission state at the clearinghouse layer."""

    QUEUED = "queued"
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    ERROR = "error"


class ClearinghouseProvider(str, Enum):
    """Supported clearinghouse providers."""

    OFFICE_ALLY = "office_ally"
    CHANGE_HEALTHCARE = "change_healthcare"
    AVAILITY = "availity"
    WAYSTAR = "waystar"
    OTHER = "other"


class PayerType(str, Enum):
    """Classification of payer entities."""

    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    COMMERCIAL = "commercial"
    SELF_PAY = "self_pay"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Core Contracts
# ---------------------------------------------------------------------------

class ClaimLineItem(BaseModel):
    """A single billable service line on a claim."""

    line_id: str
    procedure_code: str
    modifier_codes: list[str] = Field(default_factory=list)
    diagnosis_codes: list[str] = Field(default_factory=list)

    units: int = Field(..., gt=0)
    charge_cents: int = Field(..., ge=0)

    description: Optional[str] = None


class AdjustmentContract(BaseModel):
    """Financial adjustment applied to a claim."""

    adjustment_id: str
    claim_id: str
    tenant_id: str

    adjustment_type: str
    amount_cents: int = Field(..., ge=0)

    reason_code: Optional[str] = None
    applied_at: datetime


class PayerContract(BaseModel):
    """Read-only payer reference contract."""

    payer_id: str
    payer_name: str
    payer_type: PayerType

    electronic_claims_supported: bool
    electronic_remittance_supported: bool

    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None


class ClaimContract(BaseModel):
    """Canonical claim record for cross-domain consumption."""

    claim_id: str
    tenant_id: str
    patient_id: str

    encounter_id: Optional[str] = None
    transport_request_id: Optional[str] = None

    payer_id: Optional[str] = None
    payer_name: Optional[str] = None

    status: ClaimStatus

    total_charge_cents: int = Field(..., ge=0)
    total_paid_cents: int = Field(0, ge=0)
    total_adjustment_cents: int = Field(0, ge=0)
    balance_cents: int = Field(..., ge=0)

    line_items: list[ClaimLineItem] = Field(default_factory=list)

    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class DenialContract(BaseModel):
    """Denial record tied to a claim."""

    denial_id: str
    claim_id: str
    tenant_id: str

    reason_code: str
    reason_description: str

    denied_amount_cents: int = Field(..., ge=0)
    status: DenialStatus

    received_at: datetime
    updated_at: datetime


class PaymentContract(BaseModel):
    """Payment record applied to a claim."""

    payment_id: str
    claim_id: str
    tenant_id: str

    amount_cents: int = Field(..., ge=0)
    payer_name: Optional[str] = None

    status: PaymentStatus
    posted_at: datetime


class RemittanceContract(BaseModel):
    """Remittance (ERA/EOB) summary contract."""

    remit_id: str
    tenant_id: str
    payer_name: str

    total_paid_cents: int = Field(..., ge=0)
    total_adjusted_cents: int = Field(..., ge=0)

    received_at: datetime


class ClearinghouseSubmission(BaseModel):
    """Claim submission tracking via clearinghouse."""

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    status: ClearinghouseStatus

    submitted_at: Optional[datetime] = None
    response_received_at: Optional[datetime] = None
    error_message: Optional[str] = None


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class ClaimCreatedEvent(BaseModel):
    """Published when a claim is created."""

    event_type: str = "billing.claim.created"

    claim_id: str
    tenant_id: str
    patient_id: str

    created_at: datetime


class ClaimSubmittedEvent(BaseModel):
    """Published when a claim is submitted."""

    event_type: str = "billing.claim.submitted"

    claim_id: str
    tenant_id: str
    submission_id: str
    provider: ClearinghouseProvider
    submitted_at: datetime


class ClaimStatusUpdatedEvent(BaseModel):
    """Published when a claim status changes."""

    event_type: str = "billing.claim.status_updated"

    claim_id: str
    tenant_id: str
    old_status: ClaimStatus
    new_status: ClaimStatus
    updated_at: datetime


class DenialCreatedEvent(BaseModel):
    """Published when a denial is created."""

    event_type: str = "billing.denial.created"

    denial_id: str
    claim_id: str
    tenant_id: str
    created_at: datetime


class PaymentPostedEvent(BaseModel):
    """Published when a payment is applied to a claim."""

    event_type: str = "billing.payment.posted"

    payment_id: str
    claim_id: str
    tenant_id: str
    amount_cents: int = Field(..., ge=0)
    payer_id: Optional[str] = None
    posted_at: datetime


class RemittanceReceivedEvent(BaseModel):
    """Published when a remittance is received."""

    event_type: str = "billing.remittance.received"

    remit_id: str
    tenant_id: str
    received_at: datetime


class ClearinghouseAckReceivedEvent(BaseModel):
    """Published when a clearinghouse acknowledgement is received."""

    event_type: str = "billing.clearinghouse.ack_received"

    submission_id: str
    claim_id: str
    tenant_id: str

    provider: ClearinghouseProvider
    ack_code: str
    ack_message: Optional[str] = None

    received_at: datetime
