"""Pydantic schemas for patient financial APIs."""
from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from core_app.models.patient_financial import (
    PatientAccountStatus,
    PatientDisputeStatus,
    PatientPaymentStatus,
    PaymentPlanFrequency,
    PaymentPlanStatus,
)


class PatientChargeInput(BaseModel):
    claim_id: UUID | None = None
    amount: Decimal = Field(gt=0)


class CreatePatientAccountRequest(BaseModel):
    patient_id: UUID | None = None
    initial_charges: list[PatientChargeInput] = Field(default_factory=list)


class CreatePaymentPlanRequest(BaseModel):
    patient_account_id: UUID
    total_amount: Decimal = Field(gt=0)
    installment_amount: Decimal = Field(gt=0)
    frequency: PaymentPlanFrequency
    start_date: date


class RecordPatientPaymentRequest(BaseModel):
    patient_account_id: UUID
    amount: Decimal = Field(gt=0)
    payment_method: str = Field(min_length=1, max_length=50)
    transaction_id: str = Field(min_length=1, max_length=100)
    payment_plan_id: UUID | None = None


class OpenDisputeRequest(BaseModel):
    patient_account_id: UUID
    claim_id: UUID | None = None
    dispute_type: str = Field(min_length=1, max_length=50)
    reason: str = Field(min_length=1)


class ResolveDisputeRequest(BaseModel):
    resolution: PatientDisputeStatus
    notes: str | None = None


class PatientAccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    patient_id: UUID | None
    account_number: str
    balance: Decimal
    insurance_pending: Decimal
    status: PatientAccountStatus
    opened_at: datetime
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PaymentPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    patient_account_id: UUID
    total_amount: Decimal
    installment_amount: Decimal
    frequency: PaymentPlanFrequency
    remaining_amount: Decimal
    start_date: date
    next_due_date: date | None
    status: PaymentPlanStatus
    created_at: datetime
    updated_at: datetime


class PatientPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    patient_account_id: UUID
    payment_plan_id: UUID | None
    claim_id: UUID | None
    amount: Decimal
    payment_method: str
    transaction_id: str
    stripe_payment_intent_id: str | None
    status: PatientPaymentStatus
    posted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class PatientDisputeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    patient_account_id: UUID
    claim_id: UUID | None
    dispute_type: str
    reason: str
    status: PatientDisputeStatus
    resolved_at: datetime | None
    resolution_notes: str | None
    created_by_user_id: UUID | None
    created_at: datetime
    updated_at: datetime


class PatientAccountListResponse(BaseModel):
    items: list[PatientAccountResponse]
    total: int


class PatientAccountSummaryResponse(BaseModel):
    account: PatientAccountResponse
    active_plans: list[PaymentPlanResponse]
    recent_payments: list[PatientPaymentResponse]
    open_disputes: list[PatientDisputeResponse]


class MutationResultResponse(BaseModel):
    status: Literal["ok"] = "ok"
