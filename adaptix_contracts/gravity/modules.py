"""
ADAPTIX GRAVITY MODULE CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK

Authoritative Pydantic schemas for all gravity-level modules.
These contracts are the boundary between frontend and backend.
No frontend module may invent local-only DTOs for backend-backed state.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ─── Enums ───────────────────────────────────────────────────────────────────

class GravityModuleState(str, Enum):
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"
    DEGRADED = "degraded"
    EMPTY = "empty"
    STALE = "stale"


class GravityRiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class GravityActionStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    SNOOZED = "snoozed"
    RESOLVED = "resolved"


class GravityNotificationSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class GravityNotificationState(str, Enum):
    UNREAD = "unread"
    READ = "read"
    RESOLVED = "resolved"
    SNOOZED = "snoozed"
    ESCALATED = "escalated"


# ─── AI Run Payload ───────────────────────────────────────────────────────────

class GravityAIRunPayload(BaseModel):
    """
    Authoritative AI run contract.
    Every AI output must include source, confidence, risk level, and human action boundary.
    AI may NOT finalize records, submit exports, send messages, or alter authoritative state
    without human acceptance.
    """
    ai_run_id: str
    model_or_engine_id: str
    source_record_ids: List[str] = Field(default_factory=list)
    source_evidence: List[str] = Field(default_factory=list)
    generated_at: datetime
    confidence_score: float = Field(ge=0.0, le=1.0)
    risk_level: GravityRiskLevel
    human_action_required: bool
    recommended_action: Optional[str] = None
    explanation: str
    accepted_at: Optional[datetime] = None
    accepted_by: Optional[str] = None
    rejected_at: Optional[datetime] = None
    rejected_by: Optional[str] = None
    audit_event_id: Optional[str] = None


# ─── Audit Event Payload ──────────────────────────────────────────────────────

class GravityAuditEventPayload(BaseModel):
    """
    Immutable audit event. Every mutation must write an audit event.
    No silent writes. No silent failures.
    """
    id: str
    tenant_id: str
    actor_id: str
    actor_name: Optional[str] = None
    action: str
    resource_type: str
    resource_id: str
    changes: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime
    version: int = 1


# ─── Notification Payload ─────────────────────────────────────────────────────

class GravityNotificationPayload(BaseModel):
    """
    Unified notification contract.
    All modules route user-visible action feedback through the notification system.
    """
    id: str
    tenant_id: str
    title: str
    message: Optional[str] = None
    severity: GravityNotificationSeverity
    state: GravityNotificationState = GravityNotificationState.UNREAD
    module: str
    source_record_id: Optional[str] = None
    source_record_type: Optional[str] = None
    action_url: Optional[str] = None
    created_at: datetime
    read_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    snoozed_until: Optional[datetime] = None
    escalated_at: Optional[datetime] = None
    audit_event_id: Optional[str] = None


# ─── Action Payload ───────────────────────────────────────────────────────────

class GravityActionPayload(BaseModel):
    """
    Prioritized action item requiring human decision.
    """
    id: str
    tenant_id: str
    label: str
    description: Optional[str] = None
    severity: GravityRiskLevel
    status: GravityActionStatus = GravityActionStatus.OPEN
    assignee_id: Optional[str] = None
    assignee_name: Optional[str] = None
    due_at: Optional[datetime] = None
    snoozed_until: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    source_module: str
    source_record_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    audit_event_id: Optional[str] = None


# ─── Validation Result ────────────────────────────────────────────────────────

class GravityValidationError(BaseModel):
    field: str
    message: str
    code: str
    severity: GravityRiskLevel = GravityRiskLevel.HIGH


class GravityValidationResult(BaseModel):
    """
    Structured validation result. Never suppress low-confidence errors.
    """
    valid: bool
    errors: List[GravityValidationError] = Field(default_factory=list)
    warnings: List[GravityValidationError] = Field(default_factory=list)
    validated_at: datetime
    validator_version: str = "1.0"


# ─── Error Envelope ───────────────────────────────────────────────────────────

class GravityErrorEnvelope(BaseModel):
    """
    Structured error response. Never return fake success.
    """
    error_code: str
    message: str
    detail: Optional[str] = None
    field: Optional[str] = None
    retry_allowed: bool = True
    timestamp: datetime
    request_id: Optional[str] = None


# ─── Pagination ───────────────────────────────────────────────────────────────

class GravityPaginatedResponse(BaseModel):
    """
    Standard paginated response envelope.
    """
    items: List[Any]
    total: int
    page: int = 1
    limit: int = 50
    has_more: bool = False
