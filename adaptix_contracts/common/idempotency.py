"""Idempotency contracts for Adaptix services."""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel


class IdempotencyRecord(BaseModel):
    idempotency_key: str
    tenant_id: str
    service: str
    operation: str
    request_hash: str
    response_status: int
    response_body: Optional[dict] = None
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_duplicate: bool = False
