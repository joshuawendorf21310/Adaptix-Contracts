"""Pydantic schemas for the feature flag API."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class FeatureFlagConfig(BaseModel):
    """Nested config object for role overrides and percentage rollout."""

    role_overrides: dict[str, bool] = Field(default_factory=dict)
    percentage_rollout: int = Field(default=100, ge=0, le=100)


class FeatureFlagCreate(BaseModel):
    flag_key: str = Field(..., min_length=1, max_length=100)
    enabled: bool = False
    tenant_id: UUID | None = None
    config: FeatureFlagConfig = Field(default_factory=FeatureFlagConfig)
    description: str = ""


class FeatureFlagUpdate(BaseModel):
    enabled: bool | None = None
    config: FeatureFlagConfig | None = None
    description: str | None = None


class FeatureFlagResponse(BaseModel):
    id: UUID
    flag_key: str
    enabled: bool
    tenant_id: UUID | None = None
    config: dict | None = None
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class FeatureFlagEvaluateResponse(BaseModel):
    flags: dict[str, bool]
