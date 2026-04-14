"""Patient portal contract schemas for cross-domain communication.

Defines all typed request and response contracts for the patient-facing
financial trust layer: verification, account summary, statement history,
payment workflows, payment plans, disputes, document history,
communication history, AI charge explanations, and support escalation.

Primary consumer: billing. Secondary: care (encounter artifacts), transportlink
(transport-linked financial continuity).
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PatientVerificationMethod(str, Enum):
    """Supported identity verification methods for patient portal access."""

    NAME_DOB_ACCOUNT = "name_dob_account"
    NAME_DOB_LAST4_SSN = "name_dob_last4_ssn"
    TOKEN_LINK = "token_link"


class PaymentMethod(str, Enum):
    """Payment method types accepted at the patient portal."""

    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ACH = "ach"
    CHECK = "check"


class DisputeReason(str, Enum):
    """Reason categories for a patient billing dispute."""

    INSURANCE_SHOULD_COVER = "insurance_should_cover"
    SERVICE_NOT_RECEIVED = "service_not_received"
    AMOUNT_INCORRECT = "amount_incorrect"
    DUPLICATE_CHARGE = "duplicate_charge"
    FINANCIAL_HARDSHIP = "financial_hardship"
    OTHER = "other"


class PatientVerifyRequest(BaseModel):
    """Contract for patient portal identity verification."""

    verification_method: PatientVerificationMethod
    patient_name: str = Field(..., max_length=255)
    date_of_birth: str = Field(..., description="ISO 8601 date: YYYY-MM-DD")
    account_last4: Optional[str] = Field(None, min_length=4, max_length=4)
    ssn_last4: Optional[str] = Field(None, min_length=4, max_length=4)
    access_token: Optional[str] = Field(None, description="Used with token_link method")


class PatientVerifyResponse(BaseModel):
    """Response contract after successful patient verification."""

    session_token: str
    patient_account_id: str
    patient_name: str
    verified_at: datetime
    session_expires_at: datetime


class PatientAccountSummary(BaseModel):
    """Summary read contract for the patient account dashboard."""

    account_id: str
    patient_name: str
    outstanding_balance_cents: int
    last_statement_date: Optional[datetime]
    active_payment_plan: bool
    open_disputes: int
    unread_documents: int
    last_communication_at: Optional[datetime]


class StatementSummaryResponse(BaseModel):
    """Read contract for a single statement in the patient statement list."""

    id: str
    account_id: str
    statement_date: datetime
    service_date: Optional[datetime]
    total_billed_cents: int
    insurance_paid_cents: int
    adjustments_cents: int
    patient_responsibility_cents: int
    amount_paid_cents: int
    balance_due_cents: int
    status: str
    due_date: Optional[datetime]


class StatementLineItem(BaseModel):
    """A single line item within a patient statement detail."""

    description: str
    service_date: Optional[datetime]
    billed_cents: int
    insurance_paid_cents: int
    patient_responsibility_cents: int
    code: Optional[str]


class StatementDetailResponse(BaseModel):
    """Full detail read contract for a patient statement."""

    id: str
    account_id: str
    statement_date: datetime
    service_date: Optional[datetime]
    total_billed_cents: int
    insurance_paid_cents: int
    adjustments_cents: int
    patient_responsibility_cents: int
    amount_paid_cents: int
    balance_due_cents: int
    status: str
    due_date: Optional[datetime]
    line_items: list[StatementLineItem]
    transport_id: Optional[str]
    encounter_id: Optional[str]


class PaymentOptionResponse(BaseModel):
    """Read contract for available payment options and eligibility."""

    accepts_credit_card: bool
    accepts_ach: bool
    payment_plan_eligible: bool
    minimum_payment_cents: int
    outstanding_balance_cents: int
    payment_plan_minimum_monthly_cents: Optional[int]


class PaymentSubmitRequest(BaseModel):
    """Contract for submitting a patient payment."""

    account_id: str
    statement_id: Optional[str] = None
    amount_cents: int = Field(..., gt=0)
    payment_method: PaymentMethod
    payment_token: str = Field(..., description="Stripe token or ACH authorization token")
    apply_to_oldest: bool = Field(True, description="Auto-apply to oldest balance if no statement specified")


class PaymentSubmitResponse(BaseModel):
    """Response contract after a payment is processed."""

    payment_id: str
    account_id: str
    amount_cents: int
    status: str
    receipt_url: Optional[str]
    processed_at: datetime


class PaymentPlanRequest(BaseModel):
    """Contract for requesting a patient payment plan."""

    account_id: str
    total_balance_cents: int
    requested_monthly_payment_cents: int = Field(..., gt=0)
    preferred_payment_day: int = Field(..., ge=1, le=28)
    payment_method: PaymentMethod
    payment_token: str


class PaymentPlanResponse(BaseModel):
    """Read contract for a patient payment plan."""

    plan_id: str
    account_id: str
    total_balance_cents: int
    monthly_payment_cents: int
    estimated_months: int
    payment_day_of_month: int
    status: str
    next_payment_date: Optional[datetime]
    created_at: datetime


class DisputeSubmitRequest(BaseModel):
    """Contract for submitting a patient billing dispute."""

    account_id: str
    statement_id: Optional[str] = None
    reason: DisputeReason
    description: str = Field(..., min_length=10, max_length=2000)
    supporting_info: Optional[str] = Field(None, max_length=2000)


class DisputeSubmitResponse(BaseModel):
    """Response contract after a dispute is opened."""

    dispute_id: str
    account_id: str
    status: str
    estimated_resolution_days: int
    submitted_at: datetime


class PatientDocumentResponse(BaseModel):
    """Read contract for a patient-accessible document."""

    id: str
    document_type: str
    document_name: str
    service_date: Optional[datetime]
    transport_id: Optional[str]
    signed: bool
    signed_at: Optional[datetime]
    download_url: Optional[str]
    created_at: datetime


class CommunicationEventResponse(BaseModel):
    """Read contract for a single entry in the patient communication history."""

    id: str
    channel: str
    direction: str
    subject: Optional[str]
    summary: str
    sent_at: datetime
    delivery_status: str


class AiExplanationRequest(BaseModel):
    """Contract for requesting an AI plain-language explanation of charges."""

    account_id: str
    statement_id: Optional[str] = None
    question: Optional[str] = Field(None, max_length=500, description="Optional specific question from patient")


class AiExplanationResponse(BaseModel):
    """Response contract for an AI-generated charge explanation."""

    account_id: str
    statement_id: Optional[str]
    explanation: str
    disclaimer: str
    generated_at: datetime
    model_version: str


class SupportEscalationRequest(BaseModel):
    """Contract for a patient requesting billing support escalation."""

    account_id: str
    issue_type: str = Field(..., max_length=100)
    description: str = Field(..., min_length=10, max_length=2000)
    preferred_contact_method: str = Field(..., description="email or phone")
    preferred_contact_value: str = Field(..., max_length=255)


class SupportEscalationResponse(BaseModel):
    """Response contract after a support escalation ticket is created."""

    ticket_id: str
    account_id: str
    status: str
    expected_response_hours: int
    created_at: datetime
