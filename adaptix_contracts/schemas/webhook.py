"""Webhook domain response schemas.

Pydantic v2 request/response models for webhook registration, delivery,
and retry endpoints.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ── Webhook Registration ──────────────────────────────────────────────────────


class WebhookCreateRequest(BaseModel):
    """Request to register a new webhook endpoint."""

    endpoint_url: str = Field(min_length=1, max_length=2048)
    event_types: list[str] = Field(min_length=1)
    secret: str | None = Field(default=None, max_length=255)
    active: bool = True
    description: str | None = Field(default=None, max_length=500)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WebhookUpdateRequest(BaseModel):
    """Request to update a webhook registration."""

    endpoint_url: str | None = Field(default=None, min_length=1, max_length=2048)
    event_types: list[str] | None = None
    secret: str | None = Field(default=None, max_length=255)
    active: bool | None = None
    description: str | None = Field(default=None, max_length=500)


class WebhookResponse(BaseModel):
    """Webhook registration response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    endpoint_url: str
    event_types: list[str]
    active: bool
    description: str | None
    metadata: dict[str, Any]
    created_at: datetime
    updated_at: datetime


class WebhookListResponse(BaseModel):
    """Paginated webhook list."""

    items: list[WebhookResponse]
    total: int


# ── Delivery Log ──────────────────────────────────────────────────────────────


class WebhookDeliveryResponse(BaseModel):
    """A single webhook delivery attempt record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    webhook_id: UUID
    event_type: str
    endpoint_url: str
    http_status: int | None
    success: bool
    error: str | None
    attempt: int
    delivered_at: datetime | None
    created_at: datetime


class WebhookDeliveryListResponse(BaseModel):
    """Paginated webhook delivery history."""

    items: list[WebhookDeliveryResponse]
    total: int
