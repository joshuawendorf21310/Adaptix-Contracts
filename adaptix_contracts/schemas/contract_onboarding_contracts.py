"""Contract onboarding lifecycle contracts for Adaptix Contracts.

Adaptix Contracts is the system of record for contract onboarding. Dropbox
Sign is only the embedded signature provider. These schemas define the shared
contract intake, status, signature callback, activation, and audit events used
by Web, Billing, Core provisioning, and Founder workflows.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ContractLifecycleStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    READY_FOR_SIGNATURE = "ready_for_signature"
    SENT_FOR_SIGNATURE = "sent_for_signature"
    SIGNED = "signed"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ACTIVATED = "activated"
    AMENDED = "amended"
    CANCELED = "canceled"
    RENEWAL_PENDING = "renewal_pending"


class ContractServiceScope(str, Enum):
    EMS = "ems"
    FIRE = "fire"
    TRANSPORT = "transport"
    AIR = "air"
    BILLING_ONLY = "billing_only"
    MIXED = "mixed"


class ContractPayerMix(BaseModel):
    medicare_pct: float = Field(..., ge=0, le=100)
    medicaid_pct: float = Field(..., ge=0, le=100)
    commercial_pct: float = Field(..., ge=0, le=100)
    self_pay_pct: float = Field(..., ge=0, le=100)


class ContractPricingTerms(BaseModel):
    monthly_minimum_cents: int = Field(..., ge=0)
    per_run_rate_cents: int = Field(..., ge=0)
    retainer_cents: int = Field(default=0, ge=0)
    mileage_rate_cents: int = Field(default=0, ge=0)
    wait_time_rate_cents: int = Field(default=0, ge=0)
    no_load_fee_cents: int = Field(default=0, ge=0)
    cancellation_fee_cents: int = Field(default=0, ge=0)
    sla_penalty_cents: int = Field(default=0, ge=0)


class ContractBillingRules(BaseModel):
    billing_activation_gate: str = "signed_contract_required"
    stripe_is_contract_system: bool = False
    requires_signed_contract_before_billing: bool = True
    requires_signed_contract_before_module_activation: bool = True


class ContractModuleTerms(BaseModel):
    requested_modules: list[str] = Field(default_factory=list)
    module_entitlements_after_signature: list[str] = Field(default_factory=list)


class ContractIntakeRequest(BaseModel):
    organization_name: str = Field(..., min_length=1, max_length=255)
    contact_name: str = Field(..., min_length=1, max_length=255)
    contact_email: EmailStr
    service_scope: ContractServiceScope
    payer_mix: ContractPayerMix
    pricing_terms: ContractPricingTerms
    billing_rules: ContractBillingRules = Field(default_factory=ContractBillingRules)
    module_terms: ContractModuleTerms = Field(default_factory=ContractModuleTerms)
    notes: str | None = Field(None, max_length=4000)


class ContractRecord(BaseModel):
    contract_id: UUID
    tenant_id: UUID | None = None
    organization_name: str
    contact_email: EmailStr
    status: ContractLifecycleStatus
    service_scope: ContractServiceScope
    pricing_terms: ContractPricingTerms
    billing_rules: ContractBillingRules
    module_terms: ContractModuleTerms
    dropbox_signature_request_id: str | None = None
    signed_artifact_url: str | None = None
    created_at: datetime
    updated_at: datetime
    activated_at: datetime | None = None


class DropboxSignExecutionRequest(BaseModel):
    contract_id: UUID
    embedded_signing: bool = True
    signer_name: str = Field(..., min_length=1)
    signer_email: EmailStr


class DropboxSignExecutionResponse(BaseModel):
    contract_id: UUID
    status: ContractLifecycleStatus
    provider: str = "dropbox_sign"
    signature_request_id: str | None = None
    signature_request_hash: str | None = None
    sign_url: str | None = None
    unavailable_reason: str | None = None


class DropboxSignCallbackEvent(BaseModel):
    event_type: str
    event_hash: str
    event_time: str
    signature_request_id: str
    signer_email: EmailStr | None = None
    signed_artifact_url: str | None = None


class ContractActivationRequest(BaseModel):
    contract_id: UUID
    signed_contract_required: bool = True
    billing_configuration_required: bool = True
    tenant_provisioning_required: bool = True


class ContractActivationResponse(BaseModel):
    contract_id: UUID
    status: ContractLifecycleStatus
    tenant_id: UUID | None = None
    billing_configuration_state: str
    module_activation_state: str
    activation_blockers: list[str] = Field(default_factory=list)


class ContractStatusChangedEvent(BaseModel):
    event_type: str = "contracts.status_changed"
    contract_id: UUID
    tenant_id: UUID | None = None
    old_status: ContractLifecycleStatus
    new_status: ContractLifecycleStatus
    correlation_id: str | None = None
    occurred_at: datetime
