"""Adaptix Contracts — Event types and catalog.

Public API:
    DomainEvent         — base class for all typed domain events
    EventCatalog        — singleton registry for event type → schema mappings
    import_all_events() — force-import every event module so the catalog is fully populated
"""

from adaptix_contracts.events.domain_event import DomainEvent as DomainEvent  # noqa: F401
from adaptix_contracts.events.event_catalog import EventCatalog as EventCatalog  # noqa: F401


def import_all_events() -> None:
    """Import every event module to ensure all events are registered in the catalog.

    Call this once at application startup if you need catalog completeness.
    """
    from adaptix_contracts.events import (  # noqa: F401
        audit_events,
        auth_events,
        billing_events,
        cad_events,
        crewlink_events,
        epcr_events,
        fire_events,
        incident_events,
        mdt_events,
        nemsis_events,
        webhook_events,
        workforce_events,
    )