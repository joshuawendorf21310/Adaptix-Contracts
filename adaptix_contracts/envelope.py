"""
Adaptix Contracts — Versioned Event Envelope  v0.2.0

Every cross-repo event MUST be wrapped in an EventEnvelope before publication.
The envelope is the *only* surface downstream repos depend on for routing,
correlation, and compatibility checking.

Field contract:
  envelope_version  — semver of the envelope shape itself (NEVER changes without
                      a major version bump of adaptix-contracts)
  schema_version    — integer version of the *payload* schema carried inside
  contract_version  — the adaptix-contracts package semver that produced this event
  event_type        — dot-namespaced string  e.g. "incident.created"
  source_repo       — the publishing GitHub repository  e.g. "adaptix-core"
  tenant_id         — required for all multi-tenant events
  correlation_id    — optional; used for distributed tracing
  causation_id      — optional; id of the event that caused this one
  emitted_at        — UTC ISO-8601 timestamp
  payload           — the actual domain event data (validated separately)
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

# Bump ENVELOPE_VERSION only when the envelope shape itself is modified in a
# backward-incompatible way (new required field, renamed field, removed field).
ENVELOPE_VERSION = "1.0"

# Injected by the build system — do not edit directly.
from adaptix_contracts.version import CONTRACT_VERSION  # noqa: E402


class EventEnvelope(BaseModel):
    """Canonical cross-repo event transport wrapper.

    All events flowing between Adaptix repositories MUST be serialised as an
    EventEnvelope.  Consumers validate the envelope before inspecting payload.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "envelope_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "envelope_version": "1.0",
                "contract_version": "0.2.0",
                "event_type": "incident.created",
                "schema_version": 1,
                "source_repo": "adaptix-cad",
                "tenant_id": "123e4567-e89b-12d3-a456-426614174000",
                "actor_id": None,
                "correlation_id": "c0rr-0001",
                "causation_id": None,
                "emitted_at": "2026-04-09T00:00:00Z",
                "payload": {"incident_id": "...", "status": "dispatched"},
            }
        }
    )

    # ── Identity ────────────────────────────────────────────────────────────
    envelope_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this envelope instance.",
    )

    # ── Versioning ──────────────────────────────────────────────────────────
    envelope_version: str = Field(
        default=ENVELOPE_VERSION,
        description="Semver of the envelope shape. Consumers MUST reject unknown major versions.",
    )
    contract_version: str = Field(
        default=CONTRACT_VERSION,
        description="The adaptix-contracts package version that produced this envelope.",
    )
    schema_version: int = Field(
        default=1,
        ge=1,
        description="Integer version of the payload schema. Starts at 1, increments on breaking changes.",
    )

    # ── Routing ─────────────────────────────────────────────────────────────
    event_type: str = Field(
        ...,
        description=(
            "Dot-namespaced event type identifier.  Format: <domain>.<verb> "
            "e.g. 'incident.created', 'epcr.signed', 'billing.claim.submitted'."
        ),
    )
    source_repo: str = Field(
        ...,
        description="GitHub repository slug that emitted this event e.g. 'adaptix-cad'.",
    )

    # ── Tenancy ─────────────────────────────────────────────────────────────
    tenant_id: uuid.UUID = Field(
        ...,
        description="Tenant isolation key. MUST match the tenant context of all payload entities.",
    )
    actor_id: uuid.UUID | None = Field(
        default=None,
        description="User or service account that triggered the event.",
    )

    # ── Tracing ─────────────────────────────────────────────────────────────
    correlation_id: str | None = Field(
        default=None,
        description="Opaque tracing token that groups a chain of related events.",
    )
    causation_id: str | None = Field(
        default=None,
        description="envelope_id of the event that directly caused this event.",
    )

    # ── Timing ──────────────────────────────────────────────────────────────
    emitted_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp when this envelope was created.",
    )

    # ── Payload ─────────────────────────────────────────────────────────────
    payload: dict[str, Any] = Field(
        default_factory=dict,
        description="Domain-specific event data. Validated against the schema registered for event_type.",
    )

    # ── Helpers ─────────────────────────────────────────────────────────────

    def is_compatible_with(self, min_version: str, max_version: str | None = None) -> bool:
        """Return True if this envelope's contract_version is within [min, max]."""
        from adaptix_contracts.compat import is_version_compatible

        return is_version_compatible(self.contract_version, min_version, max_version)

    def to_bus_dict(self) -> dict[str, Any]:
        """Serialise to a dict suitable for Redis / SQS / EventBridge publication."""
        return self.model_dump(mode="json")

    @classmethod
    def from_bus_dict(cls, data: dict[str, Any]) -> EventEnvelope:
        """Deserialise from a raw bus message dict."""
        return cls.model_validate(data)

    @classmethod
    def wrap(
        cls,
        *,
        event_type: str,
        source_repo: str,
        tenant_id: uuid.UUID,
        payload: dict[str, Any],
        schema_version: int = 1,
        actor_id: uuid.UUID | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> EventEnvelope:
        """Convenience constructor — preferred over direct instantiation."""
        return cls(
            event_type=event_type,
            source_repo=source_repo,
            tenant_id=tenant_id,
            payload=payload,
            schema_version=schema_version,
            actor_id=actor_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
        )
