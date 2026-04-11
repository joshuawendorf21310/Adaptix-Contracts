"""Audit domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class AuditEntryCreatedEvent(DomainEvent):
    event_type: str = "audit.entry.created"
    entity_type: str = "audit_entry"

    entry_id: str = ""
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("audit.entry.created", AuditEntryCreatedEvent)
