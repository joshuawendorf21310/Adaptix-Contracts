"""Adaptix Third-Party Billing public commercial contracts.

Defines all typed request and response schemas for the public billing
commercial entry experience: ROI estimation, proposal generation,
onboarding activation, and migration intake.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BillingAudienceType(str, Enum):
    """Audience segment for the public billing entry surface."""

    AGENCY = "agency"
    BILLING_OPERATOR = "billing_operator"
    MIGRATION_PROSPECT = "migration_prospect"


class BillingEntrySummary(BaseModel):
    """Summary contract for the public billing entry hub (/billing)."""

    service_available: bool
    audience_types: list[BillingAudienceType]
    capability_areas: list[str]
    unavailable_reason: Optional[str] = None


class BillingROIRequest(BaseModel):
    """Inputs required for backend ROI estimation."""

    monthly_claim_volume: int = Field(..., gt=0)
    average_reimbursement_cents: int = Field(..., gt=0)
    current_vendor_fee_pct: float = Field(..., ge=0.0, le=100.0)
    denial_rate_pct: float = Field(..., ge=0.0, le=100.0)
    ar_over_90_days_cents: int = Field(..., ge=0)
    monthly_write_off_cents: int = Field(..., ge=0)
    has_legacy_ar_to_import: bool
    current_system_name: Optional[str] = Field(None, max_length=200)


class BillingROIRangeValue(BaseModel):
    """Directional value range from ROI estimation."""

    low_cents: int
    mid_cents: int
    high_cents: int
    basis: str


class BillingROIResponse(BaseModel):
    """Backend-computed ROI estimation result."""

    estimation_id: str

    vendor_fee_delta_annual_cents: BillingROIRangeValue
    denial_recovery_opportunity_annual_cents: BillingROIRangeValue
    ar_recovery_opportunity_cents: BillingROIRangeValue
    total_opportunity_annual_cents: BillingROIRangeValue

    assumptions: list[str]
    limitations: list[str]

    computed_at: datetime
    next_step_options: list[str]


class BillingProposalRequest(BaseModel):
    """Request for a structured commercial proposal."""

    organization_name: str = Field(..., min_length=1, max_length=200)
    contact_name: str = Field(..., min_length=1, max_length=200)
    contact_email: str = Field(..., min_length=5, max_length=200)

    audience_type: BillingAudienceType
    monthly_claim_volume: int = Field(..., gt=0)

    roi_estimation_id: Optional[str] = None
    migration_intent: bool
    notes: Optional[str] = Field(None, max_length=2000)


class BillingProposalResponse(BaseModel):
    """Outcome of a proposal request submission."""

    proposal_id: str
    status: str = Field(..., description="submitted | processing | error")

    estimated_response_hours: Optional[int] = None
    message: str
    submitted_at: datetime


class BillingOnboardingRequest(BaseModel):
    """Tenant activation and provisioning request."""

    organization_name: str = Field(..., min_length=1, max_length=200)
    contact_email: str = Field(..., min_length=5, max_length=200)
    contact_name: str = Field(..., min_length=1, max_length=200)

    audience_type: BillingAudienceType
    service_region: str = Field(..., min_length=1, max_length=100)

    monthly_claim_volume: int = Field(..., gt=0)

    has_existing_clearinghouse: bool
    clearinghouse_name: Optional[str] = Field(None, max_length=200)

    migration_intent: bool
    proposal_id: Optional[str] = None

    terms_accepted: bool


class BillingOnboardingResponse(BaseModel):
    """Result of an onboarding submission."""

    onboarding_id: str
    status: str = Field(..., description="submitted | provisioning | requires_review | error")

    next_steps: list[str]
    estimated_activation_hours: Optional[int] = None
    message: str
    submitted_at: datetime


class BillingMigrationIntakeRequest(BaseModel):
    """Legacy billing migration intake."""

    organization_name: str = Field(..., min_length=1, max_length=200)
    contact_email: str = Field(..., min_length=5, max_length=200)
    current_vendor_name: str = Field(..., min_length=1, max_length=200)

    has_exportable_ar: bool
    has_exportable_denial_history: bool
    has_exportable_remit_history: bool
    has_exportable_patient_balance_history: bool
    has_exportable_workqueue: bool

    ar_oldest_date: Optional[str] = None
    ar_total_outstanding_cents: Optional[int] = Field(None, ge=0)

    blocking_issues: Optional[str] = Field(None, max_length=2000)
    onboarding_id: Optional[str] = None


class BillingMigrationIntakeResponse(BaseModel):
    """Result of migration intake submission."""

    migration_id: str
    status: str = Field(..., description="received | review_required | blocked | error")

    readiness_summary: str
    identified_blockers: list[str]
    next_steps: list[str]
    submitted_at: datetime
