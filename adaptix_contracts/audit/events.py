"""Audit event contracts for Adaptix services."""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class AuditEventEnvelope(BaseModel):
    event_id: str
    event_type: str
    event_version: str = "1.0"
    tenant_id: str
    actor_id: str
    source_service: str
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
    idempotency_key: Optional[str] = None
    occurred_at: datetime
    payload: dict[str, Any] = {}


class ManualOverrideRecord(BaseModel):
    override_id: str
    tenant_id: str
    actor_id: str
    resource_type: str
    resource_id: str
    reason: str
    supervisor_id: Optional[str] = None
    occurred_at: datetime
    audit_trail: list[dict] = []


class WebhookEventRecord(BaseModel):
    webhook_id: str
    provider: str
    event_type: str
    tenant_id: Optional[str] = None
    idempotency_key: str
    received_at: datetime
    processed: bool = False
    processing_result: Optional[str] = None
