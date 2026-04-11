"""CAD domain events (unit and sync lifecycle).

Incident events live in incident_events.py; this module covers the remaining
CAD-sourced event types.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class UnitStatusChangedEvent(DomainEvent):
    event_type: str = "unit.status_changed"
    entity_type: str = "unit"

    unit_id: str = ""
    unit_identifier: str = ""
    previous_status: str = ""
    new_status: str = ""


class CadSyncCompletedEvent(DomainEvent):
    event_type: str = "cad.sync.completed"
    entity_type: str = "cad_sync"

    sync_id: str = ""
    cad_system_type: str = ""
    incident_count: int = 0


class CadSyncFailedEvent(DomainEvent):
    event_type: str = "cad.sync.failed"
    entity_type: str = "cad_sync"

    sync_id: str = ""
    cad_system_type: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("unit.status_changed", UnitStatusChangedEvent)
_catalog.register("cad.sync.completed", CadSyncCompletedEvent)
_catalog.register("cad.sync.failed", CadSyncFailedEvent)
