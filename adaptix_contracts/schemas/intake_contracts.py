# Intake contracts schema
# Owns all request/response schemas for the public intake surface,
# lead scoring, and billing defaults slice.

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IntakeSegment(str, Enum):
    """Segment self-declared by the prospective customer at intake."""
    EMS_AGENCY = "ems_agency"
    FIRE_AGENCY = "fire_agency"
    BILLING_COMPANY = "billing_company"
    GOVERNMENT_PUBLIC_SAFETY = "government_public_safety"
    INVESTOR = "investor"
    PARTNER = "partner"
    DEVELOPER = "developer"


class LeadTemperature(str, Enum):
    """Deterministic lead temperature bucket derived from lead score."""
    COLD = "cold"
    COOL = "cool"
    WARM = "warm"
    HOT = "hot"


class BillingModelChoice(str, Enum):
    """Billing operational model preference declared at intake."""
    FULL_SERVICE = "full_service"
    CLEARINGHOUSE = "clearinghouse"
    IN_HOUSE = "in_house"
    UNDECIDED = "undecided"
    NOT_YET_DECIDED = "not_yet_decided"


class BillingReadinessState(str, Enum):
    """Billing readiness state derived from provided billing defaults."""
    BILLING_NOT_STARTED = "billing_not_started"
    BILLING_PROFILE_STARTED = "billing_profile_started"
    BILLING_PROFILE_COMPLETE = "billing_profile_complete"
    CLEARINGHOUSE_PENDING = "clearinghouse_pending"
    MIGRATION_PENDING = "migration_pending"
    READY_FOR_TEST_CLAIM = "ready_for_test_claim"
    READY_FOR_PRODUCTION_CLAIMS = "ready_for_production_claims"
    BLOCKED = "blocked"


class ClearinghouseProvider(str, Enum):
    """Supported clearinghouse partners."""
    OFFICE_ALLY = "office_ally"
    CHANGE_HEALTHCARE = "change_healthcare"
    AVAILITY = "availity"
    WAYSTAR = "waystar"
    TRIZETTO = "trizetto"
    OTHER = "other"
    NONE = "none"
    NONE_YET = "none_yet"


class PayerType(str, Enum):
    """Payer class for billing configuration."""
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    COMMERCIAL = "commercial"
    MANAGED_CARE = "managed_care"
    WORKERS_COMP = "workers_comp"
    VA = "va"
    SELF_PAY = "self_pay"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Conditional payload sub-schemas
# ---------------------------------------------------------------------------

class EmsFireIntakePayload(BaseModel):
    """Conditional payload for EMS/fire agency segment."""
    unit_count: Optional[int] = None
    station_count: Optional[int] = None
    service_area_population: Optional[int] = None
    current_epcr_vendor: Optional[str] = None
    current_billing_vendor: Optional[str] = None
    current_cad_vendor: Optional[str] = None
    has_narcotics_tracking: Optional[bool] = None
    runs_interfacility_transport: Optional[bool] = None
    has_fire_suppression: Optional[bool] = None
    has_hems: Optional[bool] = None


class ConditionalEmsFireFields(BaseModel):
    """Conditional EMS/fire fields used in intake requests and tests.

    Uses ``extra="allow"`` so that callers may pass additional fields
    without breaking validation as the schema evolves.
    """

    model_config = {"extra": "allow"}

    number_of_units: Optional[int] = None
    current_epcr_system: Optional[str] = None
    current_dispatch_system: Optional[str] = None
    billing_model: Optional[str] = None
    go_live_timeline: Optional[str] = None
    needs_baa: Optional[bool] = None
    requested_modules: Optional[List[str]] = Field(default_factory=list)
    # Legacy / alternate field names kept for backward compat
    unit_count: Optional[int] = None
    station_count: Optional[int] = None
    service_area_population: Optional[int] = None
    current_epcr_vendor: Optional[str] = None
    current_billing_vendor: Optional[str] = None
    current_cad_vendor: Optional[str] = None
    has_narcotics_tracking: Optional[bool] = None
    runs_interfacility_transport: Optional[bool] = None
    has_fire_suppression: Optional[bool] = None
    has_hems: Optional[bool] = None


class BillingCompanyIntakePayload(BaseModel):
    """Conditional payload for third-party billing company segment."""

    model_config = {"extra": "allow"}

    client_agency_count: Optional[int] = None
    monthly_claims_volume: Optional[int] = None
    # Alias used by lead_scoring_service
    monthly_claim_volume: Optional[int] = None
    current_platform: Optional[str] = None
    npi: Optional[str] = None
    tax_id: Optional[str] = None
    clearinghouse: Optional[ClearinghouseProvider] = None
    migration_needed: Optional[bool] = None


class InvestorIntakePayload(BaseModel):
    """Conditional payload for investor segment."""
    fund_name: Optional[str] = None
    investment_stage: Optional[str] = None
    check_size_range: Optional[str] = None
    portfolio_sectors: Optional[List[str]] = Field(default_factory=list)
    how_did_you_find_us: Optional[str] = None


class ConditionalInvestorFields(BaseModel):
    """Conditional investor fields used in intake requests and tests.

    Uses ``extra="allow"`` so that callers may pass additional fields
    without breaking validation as the schema evolves.
    """

    model_config = {"extra": "allow"}

    investor_type: Optional[str] = None
    check_size_range: Optional[str] = None
    wants_demo: Optional[bool] = None
    # Legacy / alternate field names kept for backward compat
    fund_name: Optional[str] = None
    investment_stage: Optional[str] = None
    portfolio_sectors: Optional[List[str]] = Field(default_factory=list)
    how_did_you_find_us: Optional[str] = None


class DeveloperIntakePayload(BaseModel):
    """Conditional payload for developer / integration partner segment."""

    model_config = {"extra": "allow"}

    integration_type: Optional[str] = None
    target_module: Optional[str] = None
    company_name: Optional[str] = None
    github_org: Optional[str] = None
    use_case_description: Optional[str] = None
    sandbox_needed: Optional[bool] = None


# ---------------------------------------------------------------------------
# Lead scoring output (used in IntakeInitializeResponse)
# ---------------------------------------------------------------------------

class LeadScoringResult(BaseModel):
    """Output of the lead scoring classifier."""
    score: int = Field(ge=0, le=100)
    temperature: LeadTemperature
    scorer_version: str
    breakdown: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Intake initialize request / response
# ---------------------------------------------------------------------------

class IntakeInitializeRequest(BaseModel):
    """
    Public intake initialization request.

    Sent by ``POST /api/v1/intake/initialize``. No auth required.
    Idempotent: duplicate submissions for the same email + org + type
    return the prior result without creating duplicates.
    """
    # Core identity fields
    email: EmailStr
    full_name: str
    organization_name: str
    role_title: Optional[str] = None
    organization_type: IntakeSegment

    # Location / volume signals
    state_region: str
    monthly_volume: Optional[int] = None

    # Intent signal
    primary_goal: Optional[str] = None

    # Optional contact enrichment
    phone_optional: Optional[str] = None
    website_optional: Optional[str] = None

    # Legal gate
    terms_accepted: bool = False

    # Conditional segment payloads
    # Accept both legacy payload types and the newer Conditional* variants.
    # Union ordering: ConditionalEmsFireFields first so tests using that schema
    # get a proper model instance (not a raw dict) when Pydantic validates.
    ems_fire: Optional[ConditionalEmsFireFields] = None
    billing_company: Optional[BillingCompanyIntakePayload] = None
    investor: Optional[ConditionalInvestorFields] = None
    developer: Optional[DeveloperIntakePayload] = None


class IntakeInitializeResponse(BaseModel):
    """
    Response returned after a successful intake initialization.

    Contains routing, scoring, and provisioning state.
    """
    intake_id: UUID
    organization_id: UUID
    contact_id: UUID
    tenant_id: Optional[UUID] = None
    onboarding_session_id: Optional[UUID] = None

    segment: IntakeSegment
    lead_score: int = Field(ge=0, le=100)
    lead_temperature: LeadTemperature

    redirect_url: str
    provisioned: bool = False
    required_next_step: Optional[str] = None
    founder_action_required: bool = False


# ---------------------------------------------------------------------------
# Billing defaults request / response
# ---------------------------------------------------------------------------

class BillingDefaultsRequest(BaseModel):
    """
    Request to set or update billing defaults for an intake submission.

    ``POST /api/v1/intake/{intake_id}/billing-defaults``
    """

    model_config = {"extra": "allow"}

    # Required for billing profile completion
    npi: Optional[str] = None
    tax_id: Optional[str] = None

    # Billing model and clearinghouse preferences
    billing_model: Optional[BillingModelChoice] = None
    clearinghouse_provider: Optional[ClearinghouseProvider] = None
    clearinghouse: Optional[ClearinghouseProvider] = None
    payer_types: Optional[List[PayerType]] = Field(default_factory=list)
    # Alias used by billing_defaults_service.py
    payer_mix: Optional[List[PayerType]] = Field(default_factory=list)

    # Office Ally specific credentials (if chosen clearinghouse)
    office_ally_login_id: Optional[str] = None
    office_ally_password: Optional[str] = None

    # Additional identifiers
    taxonomy_code: Optional[str] = None
    state_license_number: Optional[str] = None
    medicaid_provider_id: Optional[str] = None

    # Contact for billing inquiries
    billing_contact_name: Optional[str] = None
    billing_contact_email: Optional[str] = None
    billing_contact_phone: Optional[str] = None

    # Address
    billing_address_line1: Optional[str] = None
    billing_address_line2: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_zip: Optional[str] = None

    # Additional fields used by tests
    existing_software: Optional[str] = None
    average_monthly_transport_volume: Optional[int] = None
    wants_migration_support: Optional[bool] = None


class BillingDefaultsResponse(BaseModel):
    """
    Response returned after storing/retrieving billing defaults.
    """
    id: UUID
    intake_id: UUID
    npi: Optional[str] = None
    tax_id: Optional[str] = None
    billing_model: Optional[BillingModelChoice] = None
    clearinghouse_provider: Optional[ClearinghouseProvider] = None
    payer_types: List[PayerType] = Field(default_factory=list)
    # payer_mix is an alias for payer_types used by Core-Service
    payer_mix: Optional[List[PayerType]] = Field(default_factory=list)
    # clearinghouse is an alias for clearinghouse_provider used by Core-Service
    clearinghouse: Optional[ClearinghouseProvider] = None
    profile_complete: bool = False
    readiness_state: BillingReadinessState = BillingReadinessState.BILLING_NOT_STARTED
    # billing_readiness_state is an alias for readiness_state used by Core-Service
    billing_readiness_state: Optional[BillingReadinessState] = None
    # Additional fields used by Core-Service
    taxonomy_code: Optional[str] = None
    state_license_number: Optional[str] = None
    medicaid_provider_id: Optional[str] = None
    billing_contact_name: Optional[str] = None
    billing_contact_email: Optional[str] = None
    billing_contact_phone: Optional[str] = None
    billing_address_line1: Optional[str] = None
    billing_address_line2: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_zip: Optional[str] = None
    # Additional fields used by Core-Service tests
    existing_software: Optional[str] = None
    average_monthly_transport_volume: Optional[int] = None
    wants_migration_support: Optional[bool] = None
    created_at: datetime
    updated_at: datetime


# ---------------------------------------------------------------------------
# AdaptixModule enum (canonical module registry)
# ---------------------------------------------------------------------------

class AdaptixModule(str, Enum):
    """Canonical Adaptix module identifiers."""
    CORE = "core"
    BILLING = "billing"
    EPCR = "epcr"
    NEMSIS = "nemsis"
    CAD = "cad"
    TRANSPORTLINK = "transportlink"
    FIRE = "fire"
    NERIS = "neris"
    CREWLINK = "crewlink"
    INVENTORY = "inventory"
    MEDICATIONS = "medications"
    NARCOTICS = "narcotics"
    WORKFORCE = "workforce"
    AIR = "air"
    AIR_PILOT = "air_pilot"
    COMMUNICATIONS = "communications"
    TELEPHONY = "telephony"
    GRAPH = "graph"
    SEARCH = "search"
    CALENDAR = "calendar"
    FINANCE = "finance"
    CRM = "crm"
    INVESTOR = "investor"
    PARTNER = "partner"
    FOUNDER = "founder"
    LABOR = "labor"
    DOCUMENTS = "documents"
    COMPLIANCE = "compliance"
    LEGAL = "legal"
    ANALYTICS = "analytics"
    FIELD = "field"  # Android field app module


# ---------------------------------------------------------------------------
# Event schemas required by test_intake_contracts.py
# ---------------------------------------------------------------------------

class IntakeSubmittedEvent(BaseModel):
    """Event emitted when an intake form is submitted."""
    model_config = {"extra": "allow"}
    event_type: Literal["IntakeSubmitted"] = "IntakeSubmitted"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    contact_id: Optional[UUID] = None
    segment: Optional[IntakeSegment] = None
    email: Optional[str] = None
    organization_name: Optional[str] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class LeadScoredEvent(BaseModel):
    """Event emitted when a lead is scored."""
    model_config = {"extra": "allow"}
    event_type: Literal["LeadScored"] = "LeadScored"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    lead_score: Optional[int] = None
    lead_temperature: Optional[LeadTemperature] = None
    scorer_version: Optional[str] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class TenantProvisionedEvent(BaseModel):
    """Event emitted when a tenant is provisioned."""
    model_config = {"extra": "allow"}
    event_type: Literal["TenantProvisioned"] = "TenantProvisioned"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    provisioned_modules: List[AdaptixModule] = []
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class OnboardingSessionCreatedEvent(BaseModel):
    """Event emitted when an onboarding session is created."""
    model_config = {"extra": "allow"}
    event_type: Literal["OnboardingSessionCreated"] = "OnboardingSessionCreated"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    onboarding_session_id: Optional[UUID] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class GoLiveReadinessCalculatedEvent(BaseModel):
    """Event emitted when go-live readiness is calculated."""
    model_config = {"extra": "allow"}
    event_type: Literal["GoLiveReadinessCalculated"] = "GoLiveReadinessCalculated"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    readiness_state: Optional[BillingReadinessState] = None
    readiness_score: Optional[int] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class ContractSignatureCompletedEvent(BaseModel):
    """Event emitted when a contract signature is completed."""
    model_config = {"extra": "allow"}
    event_type: Literal["ContractSignatureCompleted"] = "ContractSignatureCompleted"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    tenant_id: Optional[UUID] = None
    contract_type: Optional[str] = None
    signer_email: Optional[str] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class FounderNextActionCreatedEvent(BaseModel):
    """Event emitted when a founder next action is created."""
    model_config = {"extra": "allow"}
    event_type: Literal["FounderNextActionCreated"] = "FounderNextActionCreated"
    event_id: UUID
    intake_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    action_type: Optional[str] = None
    priority: Optional[str] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


class GrowthPostPublishedEvent(BaseModel):
    """Event emitted when a growth/marketing post is published."""
    model_config = {"extra": "allow"}
    event_type: Literal["GrowthPostPublished"] = "GrowthPostPublished"
    event_id: UUID
    post_id: Optional[UUID] = None
    post_type: Optional[str] = None
    title: Optional[str] = None
    occurred_at: Optional[datetime] = None
    correlation_id: Optional[UUID] = None


__all__ = [
    # Enums
    "IntakeSegment",
    "LeadTemperature",
    "BillingModelChoice",
    "BillingReadinessState",
    "ClearinghouseProvider",
    "PayerType",
    "AdaptixModule",
    # Sub-schemas (legacy)
    "EmsFireIntakePayload",
    "BillingCompanyIntakePayload",
    "InvestorIntakePayload",
    "DeveloperIntakePayload",
    "LeadScoringResult",
    # Sub-schemas (Conditional* variants used by tests and newer callers)
    "ConditionalEmsFireFields",
    "ConditionalInvestorFields",
    # Core request/response
    "IntakeInitializeRequest",
    "IntakeInitializeResponse",
    "BillingDefaultsRequest",
    "BillingDefaultsResponse",
    # Events
    "IntakeSubmittedEvent",
    "LeadScoredEvent",
    "TenantProvisionedEvent",
    "OnboardingSessionCreatedEvent",
    "GoLiveReadinessCalculatedEvent",
    "ContractSignatureCompletedEvent",
    "FounderNextActionCreatedEvent",
    "GrowthPostPublishedEvent",
]
