"""Tenant management contracts shared across Adaptix services."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TenantStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEACTIVATED = "deactivated"
    PENDING_SETUP = "pending_setup"


class TenantScopedModel(BaseModel):
    """Base contract for any tenant-scoped entity."""
    tenant_id: UUID


class TenantContract(BaseModel):
    id: UUID
    name: str
    slug: str
    status: TenantStatus = TenantStatus.ACTIVE
    plan_tier: Optional[str] = None
    metadata_json: Optional[dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class TenantCreateRequest(BaseModel):
    name: str
    slug: str
    plan_tier: Optional[str] = None
    metadata_json: Optional[dict[str, Any]] = None


class TenantUpdateRequest(BaseModel):
    name: Optional[str] = None
    plan_tier: Optional[str] = None
    status: Optional[TenantStatus] = None
    metadata_json: Optional[dict[str, Any]] = None


class TenantResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    status: TenantStatus
    plan_tier: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class TenantCreatedEvent(BaseModel):
    tenant_id: UUID
    name: str
    slug: str
    created_at: datetime


class TenantSuspendedEvent(BaseModel):
    tenant_id: UUID
    reason: Optional[str] = None
    suspended_at: datetime
