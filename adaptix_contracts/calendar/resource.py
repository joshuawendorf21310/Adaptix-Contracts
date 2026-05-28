"""Calendar resource contracts for TransportLink and Workforce."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from .event import AdaptixCalendarProduct


class AdaptixCalendarResourceKind(str, Enum):
    """Resource lanes supported by the reduced-scope calendar products."""

    UNIT = "unit"
    CREW = "crew"
    EQUIPMENT = "equipment"
    FACILITY = "facility"
    EMPLOYEE = "employee"
    BASE = "base"
    OPEN_SHIFT_POOL = "open_shift_pool"


class AdaptixCalendarResource(BaseModel):
    """Tenant-scoped calendar resource lane contract."""

    id: str
    tenant_id: str = Field(alias="tenantId")
    product: AdaptixCalendarProduct
    kind: AdaptixCalendarResourceKind
    label: str = Field(min_length=1)
    status: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {
        "populate_by_name": True,
        "extra": "forbid",
    }
