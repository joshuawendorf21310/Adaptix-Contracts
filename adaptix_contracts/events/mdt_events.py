"""MDT (Mobile Data Terminal) domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class MdtLoginEvent(DomainEvent):
    event_type: str = "mdt.login"
    entity_type: str = "mdt"

    unit_id: str = ""
    user_id: str = ""
    device_id: str = ""


class MdtLogoutEvent(DomainEvent):
    event_type: str = "mdt.logout"
    entity_type: str = "mdt"

    unit_id: str = ""
    user_id: str = ""
    device_id: str = ""


class MdtStatusChangedEvent(DomainEvent):
    event_type: str = "mdt.status_changed"
    entity_type: str = "mdt"

    unit_id: str = ""
    status_code: str = ""
    latitude: float = 0.0
    longitude: float = 0.0


class MdtMessageSentEvent(DomainEvent):
    event_type: str = "mdt.message.sent"
    entity_type: str = "mdt_message"

    message_id: str = ""
    unit_id: str = ""
    body: str = ""
    priority: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("mdt.login", MdtLoginEvent)
_catalog.register("mdt.logout", MdtLogoutEvent)
_catalog.register("mdt.status_changed", MdtStatusChangedEvent)
_catalog.register("mdt.message.sent", MdtMessageSentEvent)
