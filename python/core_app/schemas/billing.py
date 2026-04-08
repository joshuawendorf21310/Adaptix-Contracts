"""Billing domain response schemas (Phase 2, T216).

Pydantic v2 response models for billing command center, statements, and mail endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ── Billing Command Center ────────────────────────────────────────────────────


class RevenueDashboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_claims: int
    paid_claims: int
    denied_claims: int
    pending_claims: int
    revenue_cents: int
    clean_claim_rate_pct: float
    denial_rate_pct: float
    as_of: str


class DenialHeatmapEntry(BaseModel):
    reason_code: str | None
    count: int


class DenialHeatmapResponse(BaseModel):
    heatmap: list[DenialHeatmapEntry]
    total_denials: int
    top_reason: str | None


class PayerPerformanceEntry(BaseModel):
    payer: str
    total_claims: int
    paid: int
    denied: int
    revenue_cents: int
    clean_claim_rate_pct: float
    avg_days_to_payment: float | None


class PayerPerformanceResponse(BaseModel):
    payers: list[PayerPerformanceEntry]


class LeakageItem(BaseModel):
    claim_id: str | None = None
    payer: str | None = None
    amount_cents: int
    denial_reason: str | None = None
    leakage_type: str


class RevenueLeakageResponse(BaseModel):
    total_leakage_cents: int
    leakage_items: list[LeakageItem]
    item_count: int


class ModifierEntry(BaseModel):
    modifier: str
    total: int
    paid: int
    denied: int
    revenue_cents: int


class ModifierImpactResponse(BaseModel):
    modifiers: list[ModifierEntry]


class ClaimLifecycleResponse(BaseModel):
    claim: dict[str, Any]
    lifecycle_events: list[dict[str, Any]]


class AppealSuccessResponse(BaseModel):
    total_appeals: int
    successful: int
    success_rate_pct: float


class BillingKpisResponse(BaseModel):
    total_claims: int
    clean_claim_rate: float
    denial_rate: float
    total_revenue_cents: int
    avg_days_to_payment: float | None
    as_of: str


class ClaimThroughputDayResponse(BaseModel):
    date: str
    count: int


class ClaimThroughputResponse(BaseModel):
    throughput_by_day: list[ClaimThroughputDayResponse]
    avg_daily: float


class RevenueForecastEntryResponse(BaseModel):
    month: str
    projected_cents: int
    confidence: str


class RevenueTrendResponse(BaseModel):
    historical_monthly: dict[str, int]
    avg_monthly_cents: int
    forecast: list[RevenueForecastEntryResponse]
    months_of_data: int


class BillingHealthResponse(BaseModel):
    health_score: float
    status: str
    clean_claim_rate_pct: float
    total_claims: int
    as_of: str


class AgingBucketResponse(BaseModel):
    label: str
    count: int
    total_amount: float
    claim_ids: list[str] = []


class AgingPayerBucketResponse(BaseModel):
    label: str
    count: int
    total_amount: float


class AgingReportResponse(BaseModel):
    as_of_date: str
    total_ar: float
    avg_days: float
    buckets: list[AgingBucketResponse]
    payer_breakdown: dict[str, list[AgingPayerBucketResponse]]


class AgingTrendEntryResponse(BaseModel):
    month: str
    total_ar: float
    avg_days: float
    buckets: dict[str, float]
    mom_change: float | int = 0
    mom_change_pct: float | int = 0


class AgingTrendResponse(BaseModel):
    months: int
    trend: list[AgingTrendEntryResponse]


class BatchResubmitResult(BaseModel):
    claim_id: str
    status: str


class BatchResubmitResponse(BaseModel):
    results: list[BatchResubmitResult]
    total: int


class FraudAnomaly(BaseModel):
    type: str
    patient_id: str
    claim_count: int


class FraudAnomalyResponse(BaseModel):
    anomalies: list[FraudAnomaly]
    total_anomalies: int


# ── Statements ────────────────────────────────────────────────────────────────


class StatementMailResponse(BaseModel):
    lob_letter_id: str
    statement_id: str
    status: str


class StatementPayResponse(BaseModel):
    checkout_url: str
    session_id: str


class StatementSmsResponse(BaseModel):
    status: str
    phone_number: str


class StatementPaymentLinkResponse(BaseModel):
    pay_url: str
    statement_id: str
