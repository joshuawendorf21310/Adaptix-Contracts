"""Scheduling response schemas (Phase 2, T218).

Pydantic v2 response models for scheduling domain endpoints.
"""
from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ShiftResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    crew_id: str | None = None
    start_time: str
    end_time: str
    status: str = "scheduled"
    unit_id: str | None = None
    personnel: list[dict[str, Any]] = []
    created_at: str | None = None


class ShiftListResponse(BaseModel):
    shifts: list[ShiftResponse]
    total: int


class ScheduleOverviewResponse(BaseModel):
    date_range_start: str
    date_range_end: str
    total_shifts: int
    open_shifts: int
    filled_shifts: int
    overtime_hours: float = 0.0
