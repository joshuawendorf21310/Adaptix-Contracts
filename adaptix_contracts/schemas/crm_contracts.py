"""Shared CRM contracts for Adaptix founder-only CRM module.

Used by Adaptix-Core-Service (crm_routes, crm_service) for investor,
partner, relationship, growth, and opportunity management schemas.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Relationship contracts
# ---------------------------------------------------------------------------


class RelationshipCreateRequest(BaseModel):
    """Create a new CRM relationship."""

    name: str = Field(..., min_length=1, description="Relationship display name.")
    company: Optional[str] = Field(None, description="Company or organisation name.")
    contact_person: Optional[str] = Field(None, description="Primary contact person.")
    contact_email: Optional[str] = Field(None, description="Primary contact email.")
    stage: str = Field(
        default="prospect",
        description="Initial stage: prospect | negotiation | active | closed | churned.",
    )
    source: Optional[str] = Field(None, description="How this relationship was sourced.")
    notes: Optional[str] = Field(None, description="Free-text notes.")
    metadata_json: dict = Field(default_factory=dict)


class RelationshipResponse(BaseModel):
    """CRM relationship record response."""

    id: UUID
    tenant_id: UUID
    name: str
    company: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    stage: str
    source: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class RelationshipListResponse(BaseModel):
    """Paginated CRM relationship list."""

    items: List[RelationshipResponse]
    total: int
    limit: int
    offset: int


class RelationshipStageTransitionRequest(BaseModel):
    """Request to transition a relationship to a new stage."""

    new_stage: str = Field(
        ...,
        description="Target stage: prospect | negotiation | active | closed | churned.",
    )
    reason: Optional[str] = Field(None, description="Optional reason for the transition.")


# ---------------------------------------------------------------------------
# Investor contracts
# ---------------------------------------------------------------------------


class InvestorCreateRequest(BaseModel):
    """Create a new investor record."""

    name: str = Field(..., min_length=1, description="Investor name.")
    investor_type: str = Field(
        ...,
        description="Investor type: angel | vc | strategic | family_office | debt.",
    )
    contact_person: Optional[str] = Field(None, description="Primary contact person.")
    contact_email: Optional[str] = Field(None, description="Primary contact email.")
    notes: Optional[str] = Field(None, description="Free-text notes.")
    metadata_json: dict = Field(default_factory=dict)


class InvestorResponse(BaseModel):
    """Investor record response."""

    id: UUID
    tenant_id: UUID
    name: str
    investor_type: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class InvestorRoundCreateRequest(BaseModel):
    """Create a new funding round."""

    round_name: str = Field(..., min_length=1, description="Round name, e.g. Seed, Series A.")
    target_amount: float = Field(..., gt=0, description="Target raise amount in USD.")
    close_date: Optional[date] = Field(None, description="Expected close date.")
    status: str = Field(
        default="open",
        description="Round status: open | closed | cancelled.",
    )
    notes: Optional[str] = Field(None, description="Free-text notes.")


class InvestorRoundResponse(BaseModel):
    """Funding round response."""

    id: UUID
    tenant_id: UUID
    round_name: str
    target_amount: float
    close_date: Optional[date] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class InvestorCommitmentCreateRequest(BaseModel):
    """Record investor commitment to a funding round."""

    investor_id: UUID = Field(..., description="UUID of the committing investor.")
    round_id: UUID = Field(..., description="UUID of the funding round.")
    committed_amount: float = Field(..., gt=0, description="Committed amount in USD.")
    commitment_date: Optional[date] = Field(None, description="Date of commitment.")
    notes: Optional[str] = Field(None, description="Free-text notes.")


class InvestorCommitmentResponse(BaseModel):
    """Investor commitment response."""

    id: UUID
    tenant_id: UUID
    investor_id: UUID
    round_id: UUID
    committed_amount: float
    commitment_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class InvestorRoundSummaryResponse(BaseModel):
    """Full funding round summary including all commitments."""

    round: InvestorRoundResponse
    commitments: List[InvestorCommitmentResponse]
    total_committed: float
    commitment_count: int
    percent_funded: float


# ---------------------------------------------------------------------------
# Partner contracts
# ---------------------------------------------------------------------------


class PartnerCreateRequest(BaseModel):
    """Create a new partner record."""

    name: str = Field(..., min_length=1, description="Partner name.")
    partner_type: str = Field(
        ...,
        description="Partner type: technology | distribution | integration | reseller | referral.",
    )
    status: str = Field(
        default="active",
        description="Partner status: active | inactive | pending.",
    )
    contact_person: Optional[str] = Field(None, description="Primary contact person.")
    contact_email: Optional[str] = Field(None, description="Primary contact email.")
    notes: Optional[str] = Field(None, description="Free-text notes.")
    metadata_json: dict = Field(default_factory=dict)


class PartnerResponse(BaseModel):
    """Partner record response."""

    id: UUID
    tenant_id: UUID
    name: str
    partner_type: str
    status: str
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class PartnerAgreementCreateRequest(BaseModel):
    """Create a partner agreement record."""

    partner_id: UUID = Field(..., description="UUID of the partner.")
    agreement_type: str = Field(..., description="Agreement type: nda | msa | referral | reseller.")
    effective_date: date = Field(..., description="Agreement effective date.")
    expiry_date: Optional[date] = Field(None, description="Agreement expiry date.")
    notes: Optional[str] = Field(None, description="Free-text notes.")


class PartnerAgreementResponse(BaseModel):
    """Partner agreement response."""

    id: UUID
    tenant_id: UUID
    partner_id: UUID
    agreement_type: str
    effective_date: date
    expiry_date: Optional[date] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PartnerPerformanceCreateRequest(BaseModel):
    """Record partner performance metrics for a period."""

    partner_id: UUID = Field(..., description="UUID of the partner.")
    period: str = Field(..., description="Period label, e.g. 2026-Q1.")
    referrals_sent: int = Field(default=0, ge=0)
    deals_closed: int = Field(default=0, ge=0)
    revenue_attributed: float = Field(default=0.0, ge=0)
    notes: Optional[str] = Field(None, description="Free-text notes.")


class PartnerPerformanceResponse(BaseModel):
    """Partner performance record response."""

    id: UUID
    tenant_id: UUID
    partner_id: UUID
    period: str
    referrals_sent: int
    deals_closed: int
    revenue_attributed: float
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class PartnerDashboardResponse(BaseModel):
    """Partner dashboard aggregation."""

    total_partners: int
    active_partners: int
    top_performers: List[PartnerPerformanceResponse]
    total_revenue_attributed: float


# ---------------------------------------------------------------------------
# Growth intelligence contracts
# ---------------------------------------------------------------------------


class GrowthMetricCreateRequest(BaseModel):
    """Record calculated growth metrics for a period."""

    period: str = Field(..., description="Period label, e.g. 2026-04.")
    arr: Optional[float] = Field(None, ge=0, description="Annual Recurring Revenue in USD.")
    mrr: Optional[float] = Field(None, ge=0, description="Monthly Recurring Revenue in USD.")
    new_customers: Optional[int] = Field(None, ge=0)
    churned_customers: Optional[int] = Field(None, ge=0)
    active_customers: Optional[int] = Field(None, ge=0)
    net_revenue_retention: Optional[float] = Field(None, description="NRR as a decimal, e.g. 1.10.")
    notes: Optional[str] = Field(None, description="Free-text notes.")


class GrowthMetricResponse(BaseModel):
    """Growth metric record response."""

    id: UUID
    tenant_id: UUID
    period: str
    arr: Optional[float] = None
    mrr: Optional[float] = None
    new_customers: Optional[int] = None
    churned_customers: Optional[int] = None
    active_customers: Optional[int] = None
    net_revenue_retention: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class GrowthDashboardResponse(BaseModel):
    """Aggregated growth intelligence dashboard."""

    current_period: Optional[GrowthMetricResponse] = None
    prior_period: Optional[GrowthMetricResponse] = None
    arr_growth_pct: Optional[float] = None
    mrr_growth_pct: Optional[float] = None
    net_new_customers: Optional[int] = None


class GrowthTrendResponse(BaseModel):
    """Growth trend analysis over multiple periods."""

    periods: List[GrowthMetricResponse] = Field(default_factory=list)
    arr_trend: Optional[str] = Field(
        None,
        description="Trend direction: growing | declining | stable.",
    )
    mrr_trend: Optional[str] = Field(None)
    customer_trend: Optional[str] = Field(None)
    period_count: int = Field(default=0)


class GrowthForecastRequest(BaseModel):
    """Request a growth forecast."""

    lookback_periods: int = Field(default=3, ge=1, le=24, description="Number of historical periods to use.")
    forecast_periods: int = Field(default=3, ge=1, le=12, description="Number of periods to forecast.")


class GrowthForecastResponse(BaseModel):
    """Growth forecast response."""

    forecasted_periods: List[dict] = Field(default_factory=list)
    methodology: str = Field(default="linear_regression")
    confidence: Optional[float] = Field(None, description="Confidence score 0-1.")


# ---------------------------------------------------------------------------
# Founder opportunity contracts
# ---------------------------------------------------------------------------


class FounderOpportunityCreateRequest(BaseModel):
    """Create a founder-level opportunity."""

    title: str = Field(..., min_length=1, description="Opportunity title.")
    opportunity_type: str = Field(
        ...,
        description="Type: partnership | investment | acquisition | strategic | other.",
    )
    description: Optional[str] = Field(None, description="Opportunity description.")
    estimated_value: Optional[float] = Field(None, ge=0, description="Estimated value in USD.")
    probability: Optional[float] = Field(None, ge=0.0, le=1.0, description="Win probability 0-1.")
    target_close_date: Optional[date] = Field(None, description="Target close date.")
    contact_person: Optional[str] = Field(None)
    contact_email: Optional[str] = Field(None)
    notes: Optional[str] = Field(None, description="Free-text notes.")
    metadata_json: dict = Field(default_factory=dict)


class FounderOpportunityUpdateRequest(BaseModel):
    """Update a founder opportunity."""

    title: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = Field(None, description="open | won | lost | stalled.")
    description: Optional[str] = None
    estimated_value: Optional[float] = Field(None, ge=0)
    probability: Optional[float] = Field(None, ge=0.0, le=1.0)
    target_close_date: Optional[date] = None
    notes: Optional[str] = None
    metadata_json: Optional[dict] = None


class FounderOpportunityResponse(BaseModel):
    """Founder opportunity record response."""

    id: UUID
    tenant_id: UUID
    title: str
    opportunity_type: str
    status: str
    description: Optional[str] = None
    estimated_value: Optional[float] = None
    probability: Optional[float] = None
    target_close_date: Optional[date] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    notes: Optional[str] = None
    metadata_json: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime


class FounderOpportunityListResponse(BaseModel):
    """Paginated founder opportunity list."""

    items: List[FounderOpportunityResponse]
    total: int
    limit: int
    offset: int
