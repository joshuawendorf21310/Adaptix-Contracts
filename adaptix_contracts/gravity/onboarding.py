"""
GRAVITY ONBOARDING CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class OnboardingStepState(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class OnboardingSessionState(str, Enum):
    IN_PROGRESS = "in_progress"
    READY_FOR_GO_LIVE = "ready_for_go_live"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class OnboardingStepResponse(BaseModel):
    id: str
    session_id: str
    step_key: str
    title: str
    description: Optional[str] = None
    state: OnboardingStepState
    required: bool
    order: int
    completed_at: Optional[datetime] = None
    blocker_reason: Optional[str] = None


class OnboardingBlockerResponse(BaseModel):
    id: str
    step_key: str
    message: str
    severity: str
    resolved: bool
    created_at: datetime


class OnboardingSessionResponse(BaseModel):
    id: str
    tenant_id: str
    state: OnboardingSessionState
    readiness_score: float
    steps: List[OnboardingStepResponse]
    blockers: List[OnboardingBlockerResponse]
    created_at: datetime
    updated_at: datetime


class OnboardingCompleteStepResponse(BaseModel):
    step: OnboardingStepResponse
    session_readiness_score: float
    audit_event_id: str


class OnboardingCreateBlockerRequest(BaseModel):
    step_key: str
    message: str
    severity: str = "high"
