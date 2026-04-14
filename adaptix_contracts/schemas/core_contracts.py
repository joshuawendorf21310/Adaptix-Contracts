"""Core domain cross-domain contracts."""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class DomainEvent(BaseModel):
    """Base contract for all cross-domain events."""
    event_id: UUID
    tenant_id: UUID
    event_type: str
    source_domain: str
    payload: dict
    published_at: datetime
    correlation_id: Optional[str] = None

class UserAuthContext(BaseModel):
    """Auth context passed across domain boundaries."""
    user_id: UUID
    tenant_id: UUID
    role: str
    email: str
