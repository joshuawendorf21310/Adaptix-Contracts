from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    id: UUID
    audit_event_id: UUID | None = None
    tenant_id: UUID
    actor_user_id: UUID | None
    action: str
    entity_name: str
    entity_id: UUID | None = None
    field_changes: dict | None = None
    correlation_id: str | None
    request_id: str | None = None
    outcome_code: str | None = None
    structured_outcome: dict | None = None
    evidence_pack_id: str | None = None
    proof_refs: list[str] | None = None
    legal_hold: bool = False
    legal_hold_id: UUID | None = None
    retention_expires_at: datetime | None = None
    event_type: str | None = None
    event_id: UUID | None = None
    checksum: str | None = None
    created_at: datetime


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    skip: int
    limit: int


class AuditMutationRequest(BaseModel):
    action: str
    entity_name: str
    entity_id: UUID
    field_changes: dict


class AuditChainResponse(BaseModel):
    request_id: str | None = None
    resource: str | None = None
    resource_id: str | None = None
    operations: list[AuditLogResponse]
    total: int


class AuditRetentionSummary(BaseModel):
    tables: dict
    legal_hold_count: int


class LegalHoldCreateRequest(BaseModel):
    reason: str = Field(..., min_length=3, max_length=500)
    resource: str | None = None
    resource_id: str | None = None


class LegalHoldResponse(BaseModel):
    id: UUID
    audit_event_id: UUID | None = None
    tenant_id: UUID
    action: str
    resource: str | None = None
    resource_id: str | None = None
    legal_hold: bool
    legal_hold_id: UUID | None = None
    notes: str | None = None
    created_at: datetime


class WebhookReplayStatusResponse(BaseModel):
    id: str
    provider: str | None = None
    status: str
    replay_state: str | None = None
    replay_count: int = 0
    replay_requested_at: str | None = None
    last_replayed_at: str | None = None
    replay_reason: str | None = None
    idempotency_key: str | None = None
    external_event_id: str | None = None
    evidence_pack_id: str | None = None
    proof_refs: list[str] = []
