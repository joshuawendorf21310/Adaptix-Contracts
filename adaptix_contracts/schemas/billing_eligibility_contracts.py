"""Billing eligibility and insurance verification contracts."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EligibilityStatus(str, Enum):
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not_eligible"
    UNKNOWN = "unknown"
    ERROR = "error"


class CoverageLevel(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"


class EligibilityRequest(BaseModel):
    patient_id: str
    tenant_id: str
    payer_id: str
    service_date: datetime


class EligibilityResponse(BaseModel):
    request_id: str
    patient_id: str
    tenant_id: str

    status: EligibilityStatus
    coverage_level: Optional[CoverageLevel] = None

    plan_name: Optional[str] = None
    member_id: Optional[str] = None

    copay_cents: Optional[int] = Field(None, ge=0)
    deductible_remaining_cents: Optional[int] = Field(None, ge=0)

    verified_at: datetime


class EligibilityCheckedEvent(BaseModel):
    event_type: str = "billing.eligibility.checked"

    request_id: str
    patient_id: str
    tenant_id: str

    status: EligibilityStatus
    checked_at: datetime
