"""Shared CRM contracts for Adaptix founder-only CRM module.

Used by Adaptix-Core-Service (crm_routes, crm_service) for investor,
partner, relationship, growth, and opportunity management schemas.
"""

from __future__ import annotations

import enum
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# CRM Enums
# ---------------------------------------------------------------------------


class RelationshipStage(str, enum.Enum):
    PROSPECT = "prospect"
    NEGOTIATION = "negotiation"
    ACTIVE = "active"
    CLOSED = "closed"
    CHURNED = "churned"


class InvestorType(str, enum.Enum):
    ANGEL = "angel"
    VC = "vc"
    STRATEGIC = "strategic"
    FAMILY_OFFICE = "family_office"
    DEBT = "debt"


class CommitmentStatus(str, enum.Enum):
    PLEDGED = "pledged"
    COMMITTED = "committed"
    FUNDED = "funded"
    WITHDRAWN = "withdrawn"


class PartnerType(str, enum.Enum):
    TECHNOLOGY = "technology"
    DISTRIBUTION = "distribution"
    INTEGRATION = "integration"
    RESELLER = "reseller"
    REFERRAL = "referral"


class PartnerStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class OpportunityType(str, enum.Enum):
    PARTNERSHIP = "partnership"
    INVESTMENT = "investment"
    ACQUISITION = "acquisition"
    STRATEGIC = "strategic"
    OTHER = "other"


class OpportunityStatus(str, enum.Enum):
    DISCOVERED = "discovered"
    EVALUATING = "evaluating"
    PURSUING = "pursuing"
    WON = "won"
    LOST = "lost"
    STALLED = "stalled"


# ---------------------------------------------------------------------------
# Relationship contracts
# ---------------------------------------------------------------------------


class RelationshipCreateRequest(BaseModel):
    """Create a new CRM relationship."""

    company_name: str = Field(..., min_length=1, description="Company or organisation name.")
    contact_person: str = Field(..., description="Primary contact person.")
    contact_email: str = Field(..., description="Primary contact email.")
    contact_phone: Optional[str] = Field(None, description="Primary contact phone.")
    stage: RelationshipStage = Field(
        default=RelationshipStage.PROSPECT,
        description="Initial stage.",
    )
    estimated_value: Optional[int] = Field(None, description="Estimated value in USD.")
    notes: Optional[str] = Field(None, description="Free-text notes.")


class RelationshipResponse(BaseModel):
    """CRM relationship record response."""

    id: UUID
    tenant_id: UUID
    company_name: str
    contact_person: str
    contact_email: str
    contact_phone: Optional[str] = None
    stage: str
    estimated_value: Optional[int] = None
    last_contact_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class RelationshipListResponse(BaseModel):
    """Paginated CRM relationship list."""

    total: int
    relationships: List[RelationshipResponse]


class RelationshipStageTransitionRequest(BaseModel):
    """Request to transition a relationship to a new stage."""

    new_stage: RelationshipStage = Field(
        ...,
        description="Target stage.",
    )
    notes: Optional[str] = Field(None, description="Optional notes for the transition.")


# ---------------------------------------------------------------------------
# Investor contracts
# ---------------------------------------------------------------------------


class InvestorCreateRequest(BaseModel):
    """Create a new investor record."""

    name: str = Field(..., min_length=1, description="Investor name.")
    investor_type: InvestorType = Field(
        ...,
        description="Investor type.",
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
    status: CommitmentStatus = Field(
        default=CommitmentStatus.PLEDGED,
        description="Commitment status.",
    )
    notes: Optional[str] = Field(None, description="Free-text notes.")


class InvestorCommitmentResponse(BaseModel):
    """Investor commitment response."""

    id: UUID
    tenant_id: UUID
    investor_id: UUID
    round_id: UUID
    committed_amount: float
    funded_amount: float = 0.0
    status: str = "pledged"
    created_at: datetime
    updated_at: datetime


class InvestorRoundSummaryResponse(BaseModel):
    """Full funding round summary including all commitments."""

    round: InvestorRoundResponse
    commitments: List[InvestorCommitmentResponse]
    total_pledged: float
    total_funded: float
    funding_percentage: float


# ---------------------------------------------------------------------------
# Partner contracts
# ---------------------------------------------------------------------------


class PartnerCreateRequest(BaseModel):
    """Create a new partner record."""

    name: str = Field(..., min_length=1, description="Partner name.")
    partner_type: PartnerType = Field(
        ...,
        description="Partner type.",
    )
    status: PartnerStatus = Field(
        default=PartnerStatus.ACTIVE,
        description="Partner status.",
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
    monthly_recurring_revenue: int = Field(default=0, ge=0, description="MRR in cents.")
    deals_closed: int = Field(default=0, ge=0)
    churn_rate: float = Field(default=0.0, ge=0, description="Churn rate percentage.")


class PartnerPerformanceResponse(BaseModel):
    """Partner performance record response."""

    id: UUID
    tenant_id: UUID
    partner_id: UUID
    period: str
    monthly_recurring_revenue: int
    deals_closed: int
    churn_rate: float
    created_at: datetime


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
    monthly_recurring_revenue: int = Field(..., ge=0, description="MRR in cents.")
    churn_rate: float = Field(..., ge=0, description="Churn rate percentage.")
    lifetime_value: int = Field(..., ge=0, description="LTV in cents.")
    customer_acquisition_cost: int = Field(..., ge=0, description="CAC in cents.")
    net_retention_rate: float = Field(..., description="NRR as percentage, e.g. 115.0.")


class GrowthMetricResponse(BaseModel):
    """Growth metric record response."""

    id: UUID
    tenant_id: UUID
    period: str
    monthly_recurring_revenue: int
    churn_rate: float
    lifetime_value: int
    customer_acquisition_cost: int
    net_retention_rate: float
    growth_rate: Optional[float] = None
    created_at: datetime


class GrowthDashboardResponse(BaseModel):
    """Aggregated growth intelligence dashboard."""

    current_period: Optional[GrowthMetricResponse] = None
    prior_period: Optional[GrowthMetricResponse] = None
    mrr_growth_pct: Optional[float] = None
    churn_delta: Optional[float] = None


class GrowthTrendResponse(BaseModel):
    """Growth trend analysis over multiple periods."""

    periods: List[str] = Field(default_factory=list)
    mrr_trend: List[int] = Field(default_factory=list)
    churn_trend: List[float] = Field(default_factory=list)
    ltv_trend: List[int] = Field(default_factory=list)
    cac_trend: List[int] = Field(default_factory=list)
    nrr_trend: List[float] = Field(default_factory=list)
    growth_rates: List[float] = Field(default_factory=list)


class GrowthForecastRequest(BaseModel):
    """Request a growth forecast."""

    months_ahead: int = Field(default=12, ge=1, le=60, description="Number of months to forecast.")
    growth_model: str = Field(default="linear", description="Forecast model: linear | conservative.")


class GrowthForecastResponse(BaseModel):
    """Growth forecast response."""

    forecast_periods: List[str] = Field(default_factory=list)
    forecasted_mrr: List[int] = Field(default_factory=list)
    forecasted_churn: List[float] = Field(default_factory=list)
    forecasted_ltv: List[int] = Field(default_factory=list)
    forecasted_cac: List[int] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Founder opportunity contracts
# ---------------------------------------------------------------------------


class FounderOpportunityCreateRequest(BaseModel):
    """Create a founder-level opportunity."""

    title: str = Field(..., min_length=1, description="Opportunity title.")
    opportunity_type: OpportunityType = Field(
        ...,
        description="Type: partnership | investment | acquisition | strategic | other.",
    )
    description: Optional[str] = Field(None, description="Opportunity description.")
    status: OpportunityStatus = Field(
        default=OpportunityStatus.DISCOVERED,
        description="Initial status.",
    )
    estimated_value: Optional[int] = Field(None, ge=0, description="Estimated value in USD.")
    likelihood_percentage: Optional[float] = Field(None, ge=0.0, le=100.0, description="Win probability 0-100.")
    target_date: Optional[date] = Field(None, description="Target close date.")
    notes: Optional[str] = Field(None, description="Free-text notes.")


class FounderOpportunityUpdateRequest(BaseModel):
    """Update a founder opportunity."""

    title: Optional[str] = Field(None, min_length=1)
    status: Optional[OpportunityStatus] = Field(None, description="discovered | evaluating | pursuing | won | lost | stalled.")
    description: Optional[str] = None
    estimated_value: Optional[int] = Field(None, ge=0)
    likelihood_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    target_date: Optional[date] = None
    notes: Optional[str] = None


class FounderOpportunityResponse(BaseModel):
    """Founder opportunity record response."""

    id: UUID
    tenant_id: UUID
    title: str
    opportunity_type: str
    status: str
    description: Optional[str] = None
    estimated_value: Optional[int] = None
    likelihood_percentage: Optional[float] = None
    target_date: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    outcome_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class FounderOpportunityListResponse(BaseModel):
    """Founder opportunity list."""

    total: int
    opportunities: List[FounderOpportunityResponse]
    total_potential_value: int = 0
