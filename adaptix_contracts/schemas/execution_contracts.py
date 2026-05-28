"""Execution engine contracts for the Adaptix platform.

These schemas preserve the historical contract surface used by Core's
execution-engine integration tests and any older internal tooling that still
imports ``adaptix_contracts.schemas.execution_contracts``.

The canonical HTTP route layer in Core now uses inline request/response
schemas, but the domain model remains useful for compatibility, testability,
and future shared execution workflows.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Lifecycle states for an execution run."""

    PENDING = "pending"
    QUEUED = "queued"
    APPROVED = "approved"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    CANCELLED = "cancelled"


class ApprovalStatus(str, Enum):
    """Approval-decision states recorded for a pending execution."""

    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class RiskLevel(str, Enum):
    """Execution risk classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExecutionTarget(BaseModel):
    """Concrete target for a DAG node."""

    domain: str = Field(min_length=1, max_length=100)
    repo_id: str = Field(min_length=1, max_length=255)
    service: str = Field(min_length=1, max_length=255)
    endpoint: str = Field(min_length=1, max_length=500)


class DAGNode(BaseModel):
    """Single executable node in an execution DAG."""

    node_id: str = Field(min_length=1, max_length=255)
    target: ExecutionTarget
    payload: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)
    timeout_ms: int = Field(default=5000, ge=1000)
    critical_path: bool = Field(default=False)


class ExecutionDAG(BaseModel):
    """Complete directed acyclic graph for an execution request."""

    dag_id: str = Field(min_length=1, max_length=255)
    nodes: list[DAGNode] = Field(default_factory=list)
    entry_nodes: list[str] = Field(default_factory=list)


class ExecutionCreateRequest(BaseModel):
    """Historical contract for creating an execution run."""

    dag: ExecutionDAG
    description: str = Field(min_length=1, max_length=1000)
    requires_approval: bool = Field(default=True)
    environment: str = Field(default="staging", pattern="^(staging|production|sandbox)$")
    tags: list[str] = Field(default_factory=list)
    idempotency_key: str | None = Field(default=None, max_length=255)


class NodeExecutionResult(BaseModel):
    """Normalized per-node execution result payload."""

    node_id: str = Field(min_length=1, max_length=255)
    status: str = Field(min_length=1, max_length=50)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = Field(default=None, ge=0)
    output: dict[str, Any] | None = None
    error: str | None = None


class ApprovalRequest(BaseModel):
    """Approve/reject decision payload for a pending execution."""

    execution_id: UUID
    approved: bool
    comments: str | None = Field(default=None, max_length=2000)


class ExecutionAuditEntry(BaseModel):
    """Immutable execution-audit projection."""

    audit_id: UUID
    execution_id: UUID
    timestamp: datetime
    user_id: str
    action: str
    details: dict[str, Any] = Field(default_factory=dict)


class ExecutionRunResponse(BaseModel):
    """Compatibility response model for execution-run reads."""

    execution_id: UUID
    dag_id: str
    status: ExecutionStatus
    description: str
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_duration_ms: int | None = Field(default=None, ge=0)
    node_results: list[NodeExecutionResult] = Field(default_factory=list)
    approval_required: bool
    approval_status: ApprovalStatus | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None
    risk_level: RiskLevel | None = None
    environment: str
    tags: list[str] = Field(default_factory=list)