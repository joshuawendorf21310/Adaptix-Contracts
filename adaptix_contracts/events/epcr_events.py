"""ePCR domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class EpcrCreatedEvent(DomainEvent):
    event_type: str = "epcr.created"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""
    patient_id: str = ""


class EpcrSignedEvent(DomainEvent):
    event_type: str = "epcr.signed"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""
    patient_id: str = ""
    signed_by: str = ""
    signed_at: str = ""


class EpcrLockedEvent(DomainEvent):
    event_type: str = "epcr.locked"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""


class EpcrNemsisExportedEvent(DomainEvent):
    event_type: str = "epcr.nemsis.exported"
    entity_type: str = "epcr"

    export_id: str = ""
    epcr_id: str = ""
    state_code: str = ""
    export_status: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("epcr.created", EpcrCreatedEvent)
_catalog.register("epcr.signed", EpcrSignedEvent)
_catalog.register("epcr.locked", EpcrLockedEvent)
_catalog.register("epcr.nemsis.exported", EpcrNemsisExportedEvent)
