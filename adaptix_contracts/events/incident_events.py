"""Incident domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from typing import Any

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class IncidentCreatedEvent(DomainEvent):
    event_type: str = "incident.created"
    entity_type: str = "incident"

    incident_number: str = ""
    severity: str = ""
    dispatch_priority: int = 0
    location: dict[str, Any] = {}


class IncidentStatusChangedEvent(DomainEvent):
    event_type: str = "incident.status_changed"
    entity_type: str = "incident"

    old_status: str = ""
    new_status: str = ""


class IncidentClosedEvent(DomainEvent):
    event_type: str = "incident.closed"
    entity_type: str = "incident"

    disposition: str = ""
    close_reason: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("incident.created", IncidentCreatedEvent)
_catalog.register("incident.status_changed", IncidentStatusChangedEvent)
_catalog.register("incident.closed", IncidentClosedEvent)
