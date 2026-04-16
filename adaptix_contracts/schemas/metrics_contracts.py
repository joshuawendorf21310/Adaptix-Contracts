"""Metrics and observability contracts.

Defines typed contracts for service health, queue depth, latency,
throughput, and error-rate reporting across Adaptix services.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MetricSeverity(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"


class ServiceHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class QueueMetric(BaseModel):
    queue_name: str
    depth: int = Field(..., ge=0)
    oldest_age_seconds: Optional[int] = Field(None, ge=0)
    measured_at: datetime


class LatencyMetric(BaseModel):
    operation_name: str
    p50_ms: float = Field(..., ge=0.0)
    p95_ms: float = Field(..., ge=0.0)
    p99_ms: float = Field(..., ge=0.0)
    measured_at: datetime


class ErrorRateMetric(BaseModel):
    operation_name: str
    error_rate_pct: float = Field(..., ge=0.0, le=100.0)
    sample_size: int = Field(..., ge=0)
    measured_at: datetime


class ThroughputMetric(BaseModel):
    operation_name: str
    requests_per_minute: float = Field(..., ge=0.0)
    measured_at: datetime


class ServiceHealthSummary(BaseModel):
    service_name: str
    tenant_id: Optional[str] = None

    status: ServiceHealthStatus
    severity: MetricSeverity = MetricSeverity.NORMAL

    uptime_seconds: Optional[int] = Field(None, ge=0)
    version: Optional[str] = None
    message: Optional[str] = None

    queue_metrics: list[QueueMetric] = Field(default_factory=list)
    latency_metrics: list[LatencyMetric] = Field(default_factory=list)
    error_rate_metrics: list[ErrorRateMetric] = Field(default_factory=list)
    throughput_metrics: list[ThroughputMetric] = Field(default_factory=list)

    measured_at: datetime


class ServiceHealthReportedEvent(BaseModel):
    event_type: str = "metrics.service_health.reported"

    service_name: str
    tenant_id: Optional[str] = None
    status: ServiceHealthStatus
    severity: MetricSeverity = MetricSeverity.NORMAL

    measured_at: datetime
