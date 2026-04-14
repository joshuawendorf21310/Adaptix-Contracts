"""Adaptix Third-Party Billing portal home and operational contracts.

Defines typed shapes for the authenticated billing command portal:
priority queue summaries, claims, denials, AR, patient financial,
integration health, analytics, and founder oversight surfaces.

All values are computed by the backend. The web layer renders the
typed response only. Unavailable surfaces must be declared as
unavailable; counts must never be fabricated or defaulted to zero
when the data layer is not yet wired.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SurfaceAvailability(str, Enum):
    """Truthful availability state for a portal surface or data segment."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"
    LOADING = "loading"


class UrgencyLevel(str, Enum):
    """Work item urgency for queue prioritization."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ---------------------------------------------------------------------------
# Portal home
# ---------------------------------------------------------------------------


class BillingPriorityQueueSummary(BaseModel):
    """Summary of highest-priority work items for the portal home.

    Displayed as the primary command surface. Must reflect live
    queue state; never fabricate item counts.
    """

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    new_intake_ready_count: Optional[int] = Field(None, ge=0)
    blocked_claims_count: Optional[int] = Field(None, ge=0)
    claim_defects_count: Optional[int] = Field(None, ge=0)
    timely_filing_risk_count: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingBlockedClaimsSummary(BaseModel):
    """Summary of claims blocked from submission."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_blocked: Optional[int] = Field(None, ge=0)
    top_block_reasons: Optional[list[str]] = None
    estimated_revenue_at_risk_cents: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingDenialQueueSummary(BaseModel):
    """Summary of active denials requiring operator action."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_open_denials: Optional[int] = Field(None, ge=0)
    high_value_denial_count: Optional[int] = Field(None, ge=0)
    appeal_eligible_count: Optional[int] = Field(None, ge=0)
    total_denied_revenue_cents: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingAgedARSummary(BaseModel):
    """Summary of aged AR across aging buckets."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    bucket_0_30_cents: Optional[int] = Field(None, ge=0)
    bucket_31_60_cents: Optional[int] = Field(None, ge=0)
    bucket_61_90_cents: Optional[int] = Field(None, ge=0)
    bucket_91_120_cents: Optional[int] = Field(None, ge=0)
    bucket_over_120_cents: Optional[int] = Field(None, ge=0)
    total_ar_cents: Optional[int] = Field(None, ge=0)
    recoverable_estimate_cents: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingUnderpaymentSummary(BaseModel):
    """Summary of detected underpayments requiring follow-up."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_underpayment_candidates: Optional[int] = Field(None, ge=0)
    estimated_underpayment_cents: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingPatientFinancialSummary(BaseModel):
    """Summary of patient-side financial actions required."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    outstanding_balance_cents: Optional[int] = Field(None, ge=0)
    payment_plans_active: Optional[int] = Field(None, ge=0)
    disputes_open: Optional[int] = Field(None, ge=0)
    statements_pending_delivery: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class BillingIntegrationHealthSummary(BaseModel):
    """Summary of integration health for the portal command surface."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    connectors_healthy: Optional[int] = Field(None, ge=0)
    connectors_failing: Optional[int] = Field(None, ge=0)
    webhook_failures_pending: Optional[int] = Field(None, ge=0)
    credential_expiry_warnings: Optional[int] = Field(None, ge=0)
    mapping_drift_detected: Optional[bool] = None
    as_of: Optional[datetime] = None


class BillingOperatorSummary(BaseModel):
    """Operator-level work context for the portal home.

    Role-scoped view of personal throughput and next actions.
    """

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    operator_name: Optional[str] = None
    role: Optional[str] = None
    claims_worked_today: Optional[int] = Field(None, ge=0)
    revenue_touched_today_cents: Optional[int] = Field(None, ge=0)
    queue_pressure: Optional[str] = Field(None, description="low | medium | high | critical")
    recommended_next_action: Optional[str] = None
    as_of: Optional[datetime] = None


class BillingPortalHomeSummary(BaseModel):
    """Top-level payload for the billing portal home command surface.

    Assembles all queue summaries into one typed response.
    The web layer renders this; it must not query individual
    surfaces independently on the portal home page.
    """

    tenant_id: str
    user_id: str
    generated_at: datetime
    priority_queue: BillingPriorityQueueSummary
    blocked_claims: BillingBlockedClaimsSummary
    denial_queue: BillingDenialQueueSummary
    aged_ar: BillingAgedARSummary
    underpayments: BillingUnderpaymentSummary
    patient_financial: BillingPatientFinancialSummary
    integration_health: BillingIntegrationHealthSummary
    operator: BillingOperatorSummary


# ---------------------------------------------------------------------------
# Claims and coding
# ---------------------------------------------------------------------------


class ClaimDefectSeverity(str, Enum):
    """Severity classification for a detected claim defect."""

    BLOCKING = "blocking"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ClaimDefect(BaseModel):
    """A single defect detected during claim readiness evaluation."""

    field_name: str
    defect_type: str
    severity: ClaimDefectSeverity
    description: str
    remediation_hint: Optional[str] = None


class ClaimReadinessSummary(BaseModel):
    """Readiness evaluation result for a single claim."""

    claim_id: str
    readiness_score: int = Field(..., ge=0, le=100, description="0–100 completeness score")
    is_billable: bool
    defects: list[ClaimDefect]
    urgency: UrgencyLevel
    estimated_value_cents: Optional[int] = Field(None, ge=0)
    evaluated_at: datetime


class ClaimIntakeRecord(BaseModel):
    """A single claim in the intake queue."""

    claim_id: str
    patient_id: str
    encounter_date: Optional[str] = None
    transport_type: Optional[str] = None
    payer_name: Optional[str] = None
    readiness_score: Optional[int] = Field(None, ge=0, le=100)
    urgency: UrgencyLevel
    status: str
    created_at: datetime


class CodingSuggestion(BaseModel):
    """A single coding suggestion (CPT, ICD, modifier, or service level)."""

    suggestion_type: str = Field(..., description="cpt | icd | modifier | mileage | service_level")
    code: str
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    denial_risk: Optional[str] = Field(None, description="low | medium | high")
    source_fields: list[str] = Field(default_factory=list)


class CodingRecommendationBundle(BaseModel):
    """Complete coding recommendation set for a claim draft."""

    claim_id: str
    suggestions: list[CodingSuggestion]
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    denial_risk_summary: str
    underbilling_detected: bool
    overbilling_detected: bool
    generated_at: datetime


# ---------------------------------------------------------------------------
# Submission
# ---------------------------------------------------------------------------


class SubmissionAttempt(BaseModel):
    """Record of a single claim submission attempt."""

    attempt_id: str
    claim_id: str
    batch_id: Optional[str] = None
    clearinghouse: str
    status: str = Field(..., description="queued | submitted | accepted | rejected | error")
    error_code: Optional[str] = None
    error_description: Optional[str] = None
    submitted_at: Optional[datetime] = None
    response_received_at: Optional[datetime] = None
    retry_count: int = Field(default=0, ge=0)


class SubmissionTimelineEvent(BaseModel):
    """A single event in a claim's submission lifecycle timeline."""

    event_type: str
    description: str
    occurred_at: datetime
    actor: Optional[str] = None


# ---------------------------------------------------------------------------
# Denials
# ---------------------------------------------------------------------------


class DenialRecord(BaseModel):
    """A single denial requiring operator action."""

    denial_id: str
    claim_id: str
    patient_id: str
    payer_name: str
    denial_reason_code: str
    denial_reason_description: str
    denied_amount_cents: int = Field(..., ge=0)
    appeal_eligible: bool
    urgency: UrgencyLevel
    received_at: datetime
    follow_up_due_date: Optional[str] = None


class DenialCluster(BaseModel):
    """A cluster of denials sharing a common root cause pattern."""

    cluster_id: str
    root_cause_label: str
    denial_count: int = Field(..., ge=0)
    total_denied_cents: int = Field(..., ge=0)
    top_payers: list[str]
    recommended_action: str


class DenialRootCauseSummary(BaseModel):
    """Aggregated root-cause analysis for the denial portfolio."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    top_causes: Optional[list[DenialCluster]] = None
    as_of: Optional[datetime] = None


class DenialRecoveryForecast(BaseModel):
    """Projected recovery from the current denial portfolio."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    estimated_recoverable_cents: Optional[int] = Field(None, ge=0)
    appeal_yield_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    high_confidence_count: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


# ---------------------------------------------------------------------------
# AR and recovery
# ---------------------------------------------------------------------------


class ARAgingBucket(BaseModel):
    """A single aging bucket in the AR aging report."""

    label: str = Field(..., description="e.g. '0-30 days', '31-60 days'")
    claim_count: int = Field(..., ge=0)
    total_balance_cents: int = Field(..., ge=0)
    recoverable_estimate_cents: Optional[int] = Field(None, ge=0)


class RecoverabilityScore(BaseModel):
    """Recoverability scoring result for a single AR item."""

    claim_id: str
    score: int = Field(..., ge=0, le=100)
    estimated_recovery_cents: int = Field(..., ge=0)
    timely_filing_days_remaining: Optional[int] = None
    recommended_action: str
    confidence: str = Field(..., description="low | medium | high")


class AROpportunityRecord(BaseModel):
    """A single aged AR item with full recovery context."""

    claim_id: str
    patient_id: str
    payer_name: str
    balance_cents: int = Field(..., ge=0)
    days_outstanding: int = Field(..., ge=0)
    recoverability_score: Optional[int] = Field(None, ge=0, le=100)
    timely_filing_days_remaining: Optional[int] = None
    appeal_eligible: bool
    rebill_eligible: bool
    recommended_action: Optional[str] = None
    urgency: UrgencyLevel


class HistoricalClaimReconstructionSummary(BaseModel):
    """Summary of a historical claim reconstruction from imported data."""

    reconstruction_id: str
    source_import_id: str
    claims_reconstructed: int = Field(..., ge=0)
    claims_with_gaps: int = Field(..., ge=0)
    estimated_opportunity_cents: int = Field(..., ge=0)
    completed_at: datetime


# ---------------------------------------------------------------------------
# Patient financial
# ---------------------------------------------------------------------------


class StatementHistoryItem(BaseModel):
    """A single statement record in a patient account's statement history."""

    statement_id: str
    statement_date: str
    amount_cents: int = Field(..., ge=0)
    delivery_method: str
    delivery_status: str
    paid: bool


class PaymentHistoryItem(BaseModel):
    """A single payment record in a patient account."""

    payment_id: str
    payment_date: str
    amount_cents: int = Field(..., ge=0)
    payment_method: str
    applied_to_claim_id: Optional[str] = None


class PaymentPlanSummary(BaseModel):
    """Summary of an active patient payment plan."""

    plan_id: str
    total_balance_cents: int = Field(..., ge=0)
    monthly_payment_cents: int = Field(..., ge=0)
    payments_remaining: int = Field(..., ge=0)
    next_payment_date: Optional[str] = None
    status: str


class DisputeRecord(BaseModel):
    """A single patient balance dispute record."""

    dispute_id: str
    opened_at: datetime
    reason: str
    status: str
    resolution_notes: Optional[str] = None


class PatientCommunicationEvent(BaseModel):
    """A single communication event in a patient's financial history."""

    event_id: str
    channel: str = Field(..., description="sms | email | phone | mail | portal")
    direction: str = Field(..., description="outbound | inbound")
    summary: str
    occurred_at: datetime
    delivery_status: Optional[str] = None


class PatientBalanceExplanation(BaseModel):
    """Plain-language balance explanation for a patient account."""

    total_balance_cents: int = Field(..., ge=0)
    insurance_portion_resolved: bool
    patient_portion_cents: int = Field(..., ge=0)
    explanation_lines: list[str]
    next_recommended_action: str


class PatientFinancialAccountSummary(BaseModel):
    """Full financial summary for a single patient account."""

    patient_id: str
    total_balance_cents: int = Field(..., ge=0)
    active_payment_plan: Optional[PaymentPlanSummary] = None
    open_disputes: int = Field(..., ge=0)
    last_statement_date: Optional[str] = None
    last_payment_date: Optional[str] = None
    next_recommended_action: Optional[str] = None


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


class IntegrationStatus(str, Enum):
    """Operational status for a billing integration connector."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILING = "failing"
    UNCONFIGURED = "unconfigured"
    CREDENTIAL_EXPIRED = "credential_expired"


class CredentialHealthSummary(BaseModel):
    """Health state of stored credentials for an integration."""

    connector_id: str
    connector_name: str
    status: IntegrationStatus
    expires_at: Optional[datetime] = None
    days_until_expiry: Optional[int] = None
    last_verified_at: Optional[datetime] = None


class WebhookFailureRecord(BaseModel):
    """A single webhook delivery failure requiring inspection or replay."""

    failure_id: str
    connector_id: str
    event_type: str
    failed_at: datetime
    retry_count: int = Field(..., ge=0)
    last_error: str
    payload_available: bool
    replay_eligible: bool


class MappingDriftRecord(BaseModel):
    """A detected mapping drift in a connector's field mapping configuration."""

    drift_id: str
    connector_id: str
    field_name: str
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    detected_at: datetime
    severity: str = Field(..., description="low | medium | high | blocking")


class RetryQueueSummary(BaseModel):
    """Summary of items pending retry in the submission retry queue."""

    connector_id: str
    pending_retry_count: int = Field(..., ge=0)
    oldest_pending_at: Optional[datetime] = None
    next_retry_scheduled_at: Optional[datetime] = None


class ImportJobSummary(BaseModel):
    """Summary of a billing data import job."""

    job_id: str
    import_type: str = Field(..., description="aged_ar | denials | remits | statements | payments | workqueue")
    status: str = Field(..., description="queued | processing | completed | failed | validation_error")
    records_processed: Optional[int] = Field(None, ge=0)
    records_failed: Optional[int] = Field(None, ge=0)
    validation_warnings: list[str] = Field(default_factory=list)
    submitted_at: datetime
    completed_at: Optional[datetime] = None


class ExportJobSummary(BaseModel):
    """Summary of a billing data export job."""

    job_id: str
    export_type: str
    status: str
    records_exported: Optional[int] = Field(None, ge=0)
    destination: str
    submitted_at: datetime
    completed_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------


class RevenueCashRealizationSummary(BaseModel):
    """Revenue and cash realization analytics aggregate."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_charges_cents: Optional[int] = Field(None, ge=0)
    total_submitted_cents: Optional[int] = Field(None, ge=0)
    total_paid_cents: Optional[int] = Field(None, ge=0)
    total_outstanding_ar_cents: Optional[int] = Field(None, ge=0)
    reimbursement_lag_days_avg: Optional[float] = None
    collection_rate_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    vendor_delta_cents: Optional[int] = None
    as_of: Optional[datetime] = None


class ClaimsHealthSummary(BaseModel):
    """Claims health analytics aggregate."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    avg_readiness_score: Optional[float] = Field(None, ge=0.0, le=100.0)
    missing_field_trend: Optional[str] = None
    clean_claim_rate_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    submission_success_rate_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    as_of: Optional[datetime] = None


class DenialLeakageSummary(BaseModel):
    """Denial and revenue leakage analytics aggregate."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    denial_rate_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    total_leakage_cents: Optional[int] = Field(None, ge=0)
    appeal_yield_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    top_denial_reason: Optional[str] = None
    as_of: Optional[datetime] = None


class OperatorProductivitySummary(BaseModel):
    """Operator productivity analytics aggregate."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    claims_worked: Optional[int] = Field(None, ge=0)
    revenue_touched_cents: Optional[int] = Field(None, ge=0)
    revenue_per_hour_cents: Optional[int] = Field(None, ge=0)
    queue_pressure: Optional[str] = None
    backlog_count: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Founder Command
# ---------------------------------------------------------------------------


class FounderTenantFinancialSummary(BaseModel):
    """Financial health summary for a single tenant in founder oversight."""

    tenant_id: str
    tenant_name: str
    total_charges_cents: Optional[int] = Field(None, ge=0)
    total_paid_cents: Optional[int] = Field(None, ge=0)
    outstanding_ar_cents: Optional[int] = Field(None, ge=0)
    denial_rate_pct: Optional[float] = Field(None, ge=0.0, le=100.0)
    recovery_opportunity_cents: Optional[int] = Field(None, ge=0)
    integration_health: Optional[str] = None
    as_of: Optional[datetime] = None


class FounderBillingOverview(BaseModel):
    """Cross-tenant billing overview for the founder command surface."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_tenants: Optional[int] = Field(None, ge=0)
    tenants_with_ar_risk: Optional[int] = Field(None, ge=0)
    total_recovery_opportunity_cents: Optional[int] = Field(None, ge=0)
    total_integration_failures: Optional[int] = Field(None, ge=0)
    migrations_in_progress: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class FounderMigrationReadinessSummary(BaseModel):
    """Migration readiness board entry for a single tenant."""

    tenant_id: str
    tenant_name: str
    onboarding_status: str
    import_blockers: list[str]
    go_live_ready: bool
    go_live_risk_level: str = Field(..., description="low | medium | high | blocked")


class FounderIntegrationRiskSummary(BaseModel):
    """Integration risk summary for founder oversight."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    failing_connectors: Optional[int] = Field(None, ge=0)
    credential_expiring_soon: Optional[int] = Field(None, ge=0)
    webhook_backlog_count: Optional[int] = Field(None, ge=0)
    replay_needed_count: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None


class FounderRecoveryOpportunitySummary(BaseModel):
    """Cross-tenant recovery opportunity for founder command."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    total_dormant_ar_cents: Optional[int] = Field(None, ge=0)
    total_underpayment_candidates: Optional[int] = Field(None, ge=0)
    highest_opportunity_tenant_id: Optional[str] = None
    as_of: Optional[datetime] = None


class FounderOperationalRiskSummary(BaseModel):
    """Operator and support escalation risk for founder command."""

    availability: SurfaceAvailability
    unavailable_reason: Optional[str] = None
    overloaded_operators: Optional[int] = Field(None, ge=0)
    open_support_escalations: Optional[int] = Field(None, ge=0)
    sla_breaches: Optional[int] = Field(None, ge=0)
    as_of: Optional[datetime] = None
