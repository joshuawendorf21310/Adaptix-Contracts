"""Auth context contracts for Adaptix services."""
from typing import Optional
from pydantic import BaseModel


class TenantAuthContext(BaseModel):
    tenant_id: str
    user_id: str
    roles: list[str]
    permissions: list[str]
    session_id: str
    issued_at: str
    expires_at: str
    source_service: Optional[str] = None


class RolePermissionDecision(BaseModel):
    allowed: bool
    role: str
    permission: str
    reason: Optional[str] = None
    tenant_id: str
    user_id: str
