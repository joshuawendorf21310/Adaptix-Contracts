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
class IncidentAssignedEvent(DomainEvent):
    event_type: str = "incident.assigned"
    entity_type: str = "incident"
    incident_id: str = ""
    unit_id: str = ""
    assigned_at: str = ""
class IncidentCallerCallbackEvent(DomainEvent):
    event_type: str = "incident.caller.callback"
    entity_type: str = "incident"
    incident_id: str = ""
    callback_number: str = ""
    callback_requested_at: str = ""
class IncidentDispatchedEvent(DomainEvent):
    event_type: str = "incident.dispatched"
    entity_type: str = "incident"
    incident_id: str = ""
    unit_id: str = ""
    dispatched_at: str = ""
class IncidentLocationUpdatedEvent(DomainEvent):
    event_type: str = "incident.location_updated"
    entity_type: str = "incident"
    incident_id: str = ""
    previous_location: str = ""
    new_location: str = ""
class IncidentMutualAidAcceptedEvent(DomainEvent):
    event_type: str = "incident.mutual_aid_accepted"
    entity_type: str = "incident"
    incident_id: str = ""
    providing_tenant_id: str = ""
    units_assigned: str = ""
class IncidentMutualAidDeclinedEvent(DomainEvent):
    event_type: str = "incident.mutual_aid_declined"
    entity_type: str = "incident"
    incident_id: str = ""
    declining_tenant_id: str = ""
    reason: str = ""
class IncidentMutualAidRequestedEvent(DomainEvent):
    event_type: str = "incident.mutual_aid_requested"
    entity_type: str = "incident"
    incident_id: str = ""
    requesting_tenant_id: str = ""
    requested_resources: str = ""
class IncidentNotesAddedEvent(DomainEvent):
    event_type: str = "incident.notes.added"
    entity_type: str = "incident"
    incident_id: str = ""
    note_text: str = ""
    added_by: str = ""
    added_at: str = ""
class IncidentPriorityChangedEvent(DomainEvent):
    event_type: str = "incident.priority_changed"
    entity_type: str = "incident"
    incident_id: str = ""
    previous_priority: str = ""
    new_priority: str = ""
class IncidentResourceRequestedEvent(DomainEvent):
    event_type: str = "incident.resource.requested"
    entity_type: str = "incident"
    incident_id: str = ""
    resource_type: str = ""
    quantity: str = ""
    requested_by: str = ""
_catalog.register("incident.assigned", IncidentAssignedEvent)
_catalog.register("incident.caller.callback", IncidentCallerCallbackEvent)
_catalog.register("incident.dispatched", IncidentDispatchedEvent)
_catalog.register("incident.location_updated", IncidentLocationUpdatedEvent)
_catalog.register("incident.mutual_aid_accepted", IncidentMutualAidAcceptedEvent)
_catalog.register("incident.mutual_aid_declined", IncidentMutualAidDeclinedEvent)
_catalog.register("incident.mutual_aid_requested", IncidentMutualAidRequestedEvent)
_catalog.register("incident.notes.added", IncidentNotesAddedEvent)
_catalog.register("incident.priority_changed", IncidentPriorityChangedEvent)
_catalog.register("incident.resource.requested", IncidentResourceRequestedEvent)
