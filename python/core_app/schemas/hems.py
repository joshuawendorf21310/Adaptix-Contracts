"""HEMS response schemas (Phase 2, T218).

Pydantic v2 response models for HEMS (helicopter EMS) mission endpoints.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class HemsMissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    incident_id: str | None = None
    aircraft_id: str | None = None
    status: str
    mission_type: str | None = None
    launch_time: str | None = None
    eta_minutes: int | None = None
    data: dict[str, Any] = {}
    created_at: str | None = None
    updated_at: str | None = None


class HemsMissionListResponse(BaseModel):
    missions: list[HemsMissionResponse]
    total: int


class HemsAircraftResponse(BaseModel):
    id: str
    tail_number: str
    model: str | None = None
    status: str = "available"
    base_location: str | None = None


class HemsWeatherResponse(BaseModel):
    flyable: bool
    conditions: str | None = None
    ceiling_ft: int | None = None
    visibility_sm: float | None = None
    wind_kts: int | None = None
    updated_at: str | None = None
