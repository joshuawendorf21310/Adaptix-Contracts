"""CrewLink domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class CrewlinkAlertCreatedEvent(DomainEvent):
    event_type: str = "crewlink.alert.created"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""
    page_type: str = ""
    priority: str = ""
    recipients: list[str] = []


class CrewlinkAlertAcknowledgedEvent(DomainEvent):
    event_type: str = "crewlink.alert.acknowledged"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""
    user_id: str = ""
    device_id: str = ""
    acknowledged_at: str = ""


class CrewlinkAlertExpiredEvent(DomainEvent):
    event_type: str = "crewlink.alert.expired"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""


class CrewlinkAssignmentAcceptedEvent(DomainEvent):
    event_type: str = "crewlink.assignment.accepted"
    entity_type: str = "crewlink_assignment"

    assignment_id: str = ""
    incident_id: str = ""
    user_id: str = ""
    unit_id: str = ""


class CrewlinkAssignmentDeclinedEvent(DomainEvent):
    event_type: str = "crewlink.assignment.declined"
    entity_type: str = "crewlink_assignment"

    assignment_id: str = ""
    user_id: str = ""
    reason: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("crewlink.alert.created", CrewlinkAlertCreatedEvent)
_catalog.register("crewlink.alert.acknowledged", CrewlinkAlertAcknowledgedEvent)
_catalog.register("crewlink.alert.expired", CrewlinkAlertExpiredEvent)
_catalog.register("crewlink.assignment.accepted", CrewlinkAssignmentAcceptedEvent)
_catalog.register("crewlink.assignment.declined", CrewlinkAssignmentDeclinedEvent)
