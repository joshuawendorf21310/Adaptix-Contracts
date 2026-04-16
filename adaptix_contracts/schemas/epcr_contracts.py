File: contracts/epcr_contracts.py

"""ePCR domain contract schemas for cross-domain communication."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EpcrChartCreatedEvent(BaseModel):
    """Published when an ePCR chart is created."""

    event_type: str = "epcr.chart.created"

    chart_id: str
    tenant_id: str
    call_number: str
    incident_type: str

    created_at: datetime


class EpcrChartFinalizedEvent(BaseModel):
    """Published when an ePCR chart is finalized."""

    event_type: str = "epcr.chart.finalized"

    chart_id: str
    tenant_id: str
    call_number: str

    finalized_at: datetime
    is_nemsis_compliant: bool

    missing_fields: list[str] = Field(default_factory=list)


class EpcrChartContract(BaseModel):
    """Read-only ePCR chart contract for cross-domain consumption."""

    id: str
    tenant_id: str

    call_number: str
    status: str
    incident_type: str

    created_at: datetime
    updated_at: Optional[datetime] = None
    finalized_at: Optional[datetime] = None


class EpcrNemsissComplianceContract(BaseModel):
    """NEMSIS 3.5.1 compliance status for a chart."""

    chart_id: str

    is_fully_compliant: bool
    compliance_percentage: float

    missing_mandatory_fields: list[str] = Field(default_factory=list)
