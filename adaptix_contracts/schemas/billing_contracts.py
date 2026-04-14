"""Adaptix Third-Party Billing public commercial contracts.

Defines all typed request and response schemas for the public billing
commercial entry experience: ROI estimation, proposal generation,
onboarding activation, and migration intake.

These contracts are the single source of truth consumed by the web layer.
No business logic may live in the web layer; all computation must flow
through the backend and be presented via these typed shapes.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class BillingAudienceType(str, Enum):
    """Audience segment for the public billing entry surface.

    Each segment routes to a distinct CTA and intake flow.
    """

    AGENCY = "agency"
    BILLING_OPERATOR = "billing_operator"
    MIGRATION_PROSPECT = "migration_prospect"


class BillingEntrySummary(BaseModel):
    """Summary contract for the public billing entry hub (/billing).

    Rendered by the web layer with no fabricated content.
    Unavailable fields must be shown as unavailable, never as zero.
    """

    service_available: bool
    audience_types: list[BillingAudienceType]
    capability_areas: list[str]
    unavailable_reason: Optional[str] = None


class BillingROIRequest(BaseModel):
    """Inputs required for backend ROI estimation.

    Collected via the public /billing/roi intake form.
    All fields are required because the estimator cannot produce
    directional value analysis from incomplete operational data.
    """

    monthly_claim_volume: int = Field(..., gt=0, description="Average monthly claims submitted")
    average_reimbursement_cents: int = Field(..., gt=0, description="Average reimbursement per claim in cents")
    current_vendor_fee_pct: float = Field(..., ge=0.0, le=100.0, description="Current vendor fee as percentage of collections")
    denial_rate_pct: float = Field(..., ge=0.0, le=100.0, description="Estimated denial rate as percentage of submitted claims")
    ar_over_90_days_cents: int = Field(..., ge=0, description="Total AR outstanding over 90 days in cents")
    monthly_write_off_cents: int = Field(..., ge=0, description="Monthly average write-off amount in cents")
    has_legacy_ar_to_import: bool = Field(..., description="Whether legacy aged AR exists for import and recovery")
    current_system_name: Optional[str] = Field(None, max_length=200, description="Current billing system or vendor name")


class BillingROIRangeValue(BaseModel):
    """A directional value range from the ROI estimation model.

    Expressed as low, mid, and high scenario estimates.
    All values are in cents. The backend must not fabricate
    specific dollar outcomes; ranges must be model-driven.
    """

    low_cents: int
    mid_cents: int
    high_cents: int
    basis: str = Field(..., description="Plain-language explanation of how this range was derived")


class BillingROIResponse(BaseModel):
    """Backend-computed ROI estimation result.

    Directional only. Must include assumptions and explicit limitations.
    The web layer must display the assumptions and limitations alongside
    any financial figures; they must never be hidden.
    """

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
    """Request for a structured commercial proposal.

    Collected via the /billing/proposal flow after or alongside ROI.
    """

    organization_name: str = Field(..., min_length=1, max_length=200)
    contact_name: str = Field(..., min_length=1, max_length=200)
    contact_email: str = Field(..., min_length=5, max_length=200)
    audience_type: BillingAudienceType
    monthly_claim_volume: int = Field(..., gt=0)
    roi_estimation_id: Optional[str] = Field(None, description="If ROI was already computed, link it here")
    migration_intent: bool = Field(..., description="Whether migration from existing vendor is intended")
    notes: Optional[str] = Field(None, max_length=2000)


class BillingProposalResponse(BaseModel):
    """Outcome of a proposal request submission.

    Status must reflect the real submission outcome.
    No fake success responses are acceptable.
    """

    proposal_id: str
    status: str = Field(..., description="submitted | processing | error")
    estimated_response_hours: Optional[int] = None
    message: str
    submitted_at: datetime


class BillingOnboardingRequest(BaseModel):
    """Tenant activation and provisioning request.

    Submitted via the /billing/onboarding wizard.
    Persisted as a draft-capable, resumable flow.
    """

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
    terms_accepted: bool = Field(..., description="Must be true for onboarding to proceed")


class BillingOnboardingResponse(BaseModel):
    """Result of an onboarding submission.

    Reflects real provisioning state. Must report partial
    completion or error states honestly.
    """

    onboarding_id: str
    status: str = Field(..., description="submitted | provisioning | requires_review | error")
    next_steps: list[str]
    estimated_activation_hours: Optional[int] = None
    message: str
    submitted_at: datetime


class BillingMigrationIntakeRequest(BaseModel):
    """Legacy billing migration intake.

    Collects the data needed to plan and execute a full vendor migration,
    including aged AR, denial history, remit history, and workqueue state.
    """

    organization_name: str = Field(..., min_length=1, max_length=200)
    contact_email: str = Field(..., min_length=5, max_length=200)
    current_vendor_name: str = Field(..., min_length=1, max_length=200)
    has_exportable_ar: bool
    has_exportable_denial_history: bool
    has_exportable_remit_history: bool
    has_exportable_patient_balance_history: bool
    has_exportable_workqueue: bool
    ar_oldest_date: Optional[str] = Field(None, description="Approximate date of oldest open AR item (YYYY-MM-DD)")
    ar_total_outstanding_cents: Optional[int] = Field(None, ge=0)
    blocking_issues: Optional[str] = Field(None, max_length=2000, description="Any known migration blockers")
    onboarding_id: Optional[str] = None


class BillingMigrationIntakeResponse(BaseModel):
    """Result of migration intake submission.

    Reflects real processing state, including any known blockers.
    """

    migration_id: str
    status: str = Field(..., description="received | review_required | blocked | error")
    readiness_summary: str
    identified_blockers: list[str]
    next_steps: list[str]
    submitted_at: datetime
