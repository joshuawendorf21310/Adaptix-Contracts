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
        admin_events,
        ai_events,
        air_events,
        audit_events,
        auth_events,
        billing_events,
        cad_events,
        command_events,
        communications_events,
        core_events,
        crewlink_events,
        epcr_events,
        fire_events,
        incident_events,
        interop_events,
        inventory_events,
        mdt_events,
        nemsis_events,
        transport_events,
        webhook_events,
        workforce_events,
    )