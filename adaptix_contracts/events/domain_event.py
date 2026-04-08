"""Domain Event base model for Adaptix event-driven architecture.

Provides a typed, validated event model that coexists with the legacy BaseEvent
(EventBridge-focused) system. Domain events are designed for internal pub/sub
via Redis and future EventBridge forwarding.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DomainEvent(BaseModel):
    """Base class for all typed domain events in Adaptix.

    Every domain event carries tenant isolation, actor attribution, and
    correlation metadata.  Subclasses add domain-specific fields.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_type": "IncidentCreated",
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                "entity_type": "incident",
                "entity_id": "550e8400-e29b-41d4-a716-446655440000",
                "payload": {"severity": "critical"},
            }
        }
    )

    event_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this event instance",
    )
    event_type: str = Field(
        ...,
        description="Dot-delimited or PascalCase event type identifier",
    )
    tenant_id: uuid.UUID = Field(
        ...,
        description="Tenant ID for multi-tenancy isolation",
    )
    actor_id: uuid.UUID | None = Field(
        default=None,
        description="User or system actor that triggered the event",
    )
    entity_type: str = Field(
        ...,
        description="Domain entity type (e.g. incident, epcr, claim)",
    )
    entity_id: uuid.UUID = Field(
        ...,
        description="Primary key of the affected entity",
    )
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Domain-specific event payload",
    )
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp when event was created",
    )
    correlation_id: str | None = Field(
        default=None,
        description="Correlation ID for tracing related events",
    )
    version: int = Field(
        default=1,
        description="Schema version for backward compatibility",
    )
