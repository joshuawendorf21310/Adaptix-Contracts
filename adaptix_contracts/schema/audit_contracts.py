"""Audit and compliance contracts.

Defines typed contracts for immutable audit logging, access tracing,
PHI-sensitive actions, security events, and compliance review workflows.

These contracts provide the canonical cross-domain audit surface for Adaptix.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AuditActorType(str, Enum):
    """Actor classification for an audited action."""

    USER = "user"
    SYSTEM = "system"
    SERVICE = "service"
    PATIENT = "patient"
    UNKNOWN = "unknown"


class AuditActionType(str, Enum):
    """Canonical action categories for audit events."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXPORT = "export"
    SIGN = "sign"
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"


class AuditSeverity(str, Enum):
    """Severity classification for audit and security events."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ComplianceReviewStatus(str, Enum):
    """Status of a compliance review item."""

    OPEN = "open"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class AuditContext(BaseModel):
    """Context surrounding an audited operation."""

    tenant_id: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    source_ip: Optional[str] = None
    user_agent: Optional[str] = None
    service_name: Optional[str] = None


class AuditRecord(BaseModel):
    """Canonical immutable audit record."""

    audit_id: str

    actor_type: AuditActorType
    actor_id: Optional[str] = None
    actor_name: Optional[str] = None

    action_type: AuditActionType
    resource_type: str
    resource_id: Optional[str] = None

    success: bool
    severity: AuditSeverity = AuditSeverity.LOW

    context: AuditContext

    changed_fields: list[str] = Field(default_factory=list)
    reason: Optional[str] = None
    occurred_at: datetime


class PhiAccessRecord(BaseModel):
    """PHI-specific access trace for compliance review."""

    access_id: str
    tenant_id: str

    actor_id: str
    patient_id: str

    resource_type: str
    resource_id: Optional[str] = None

    access_purpose: str
    minimum_necessary_asserted: bool

    occurred_at: datetime


class SecurityEventRecord(BaseModel):
    """Security-significant system event."""

    event_id: str
    tenant_id: Optional[str] = None

    event_type: str
    severity: AuditSeverity

    actor_id: Optional[str] = None
    source_ip: Optional[str] = None

    description: str
    detected_at: datetime


class ComplianceReviewItem(BaseModel):
    """Manual or automated compliance review work item."""

    review_id: str
    tenant_id: str

    related_audit_id: Optional[str] = None
    related_security_event_id: Optional[str] = None

    title: str
    description: str

    status: ComplianceReviewStatus
    severity: AuditSeverity

    assigned_to_user_id: Optional[str] = None
    opened_at: datetime
    resolved_at: Optional[datetime] = None


class AuditRecordCreatedEvent(BaseModel):
    """Published when an audit record is created."""

    event_type: str = "audit.record.created"

    audit_id: str
    tenant_id: str
    resource_type: str
    resource_id: Optional[str] = None

    occurred_at: datetime


class PhiAccessLoggedEvent(BaseModel):
    """Published when PHI access is logged."""

    event_type: str = "audit.phi_access.logged"

    access_id: str
    tenant_id: str
    patient_id: str
    actor_id: str

    occurred_at: datetime


class SecurityEventDetectedEvent(BaseModel):
    """Published when a security-significant event is detected."""

    event_type: str = "audit.security_event.detected"

    event_id: str
    tenant_id: Optional[str] = None
    severity: AuditSeverity

    detected_at: datetime


class ComplianceReviewOpenedEvent(BaseModel):
    """Published when a compliance review item is opened."""

    event_type: str = "audit.compliance_review.opened"

    review_id: str
    tenant_id: str
    severity: AuditSeverity

    opened_at: datetime
