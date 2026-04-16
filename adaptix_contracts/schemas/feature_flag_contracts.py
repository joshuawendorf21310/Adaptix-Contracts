"""Feature flag contracts.

Defines typed contracts for feature flag resolution, evaluation,
targeting, and rollout visibility across Adaptix services.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class FeatureFlagStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    CONDITIONAL = "conditional"


class TargetType(str, Enum):
    GLOBAL = "global"
    TENANT = "tenant"
    USER = "user"
    ROLE = "role"
    SERVICE = "service"


class FeatureFlagRule(BaseModel):
    rule_id: str
    target_type: TargetType
    target_value: str
    enabled: bool
    note: Optional[str] = None


class FeatureFlagContract(BaseModel):
    flag_key: str
    description: Optional[str] = None

    status: FeatureFlagStatus
    default_enabled: bool

    rules: list[FeatureFlagRule] = Field(default_factory=list)
    evaluated_at: datetime


class FeatureFlagResolutionRequest(BaseModel):
    flag_key: str
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None
    service_name: Optional[str] = None


class FeatureFlagResolutionResponse(BaseModel):
    flag_key: str
    resolved_enabled: bool
    resolved_by_rule_id: Optional[str] = None
    evaluated_at: datetime


class FeatureFlagUpdatedEvent(BaseModel):
    event_type: str = "feature_flag.updated"

    flag_key: str
    status: FeatureFlagStatus
    updated_at: datetime
