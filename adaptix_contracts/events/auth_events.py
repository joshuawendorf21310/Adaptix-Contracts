"""Auth and tenancy domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from pydantic import Field

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class TenantCreatedEvent(DomainEvent):
    event_type: str = "tenant.created"
    entity_type: str = "tenant"

    name: str = ""
    service_lines: list[str] = Field(default_factory=list)


class TenantSuspendedEvent(DomainEvent):
    event_type: str = "tenant.suspended"
    entity_type: str = "tenant"

    reason: str = ""


class UserCreatedEvent(DomainEvent):
    event_type: str = "user.created"
    entity_type: str = "user"

    user_id: str = ""
    email: str = ""
    roles: list[str] = Field(default_factory=list)


class UserDeactivatedEvent(DomainEvent):
    event_type: str = "user.deactivated"
    entity_type: str = "user"

    user_id: str = ""


class FeatureFlagToggledEvent(DomainEvent):
    event_type: str = "feature_flag.toggled"
    entity_type: str = "feature_flag"

    flag_name: str = ""
    enabled: bool = False


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("tenant.created", TenantCreatedEvent)
_catalog.register("tenant.suspended", TenantSuspendedEvent)
_catalog.register("user.created", UserCreatedEvent)
_catalog.register("user.deactivated", UserDeactivatedEvent)
_catalog.register("feature_flag.toggled", FeatureFlagToggledEvent)
