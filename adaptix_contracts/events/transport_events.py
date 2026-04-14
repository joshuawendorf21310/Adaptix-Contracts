"""Transport domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class TransportAssignedEvent(DomainEvent):
    event_type: str = "transport.assigned"
    entity_type: str = "transport"

    transport_id: str = ""
    unit_id: str = ""
    crew_ids: str = ""
    assigned_at: str = ""


class TransportCompletedEvent(DomainEvent):
    event_type: str = "transport.completed"
    entity_type: str = "transport"

    transport_id: str = ""
    completed_at: str = ""
    actual_destination: str = ""


class TransportEtaUpdatedEvent(DomainEvent):
    event_type: str = "transport.eta.updated"
    entity_type: str = "transport"

    transport_id: str = ""
    previous_eta: str = ""
    new_eta: str = ""


class TransportRequestedEvent(DomainEvent):
    event_type: str = "transport.requested"
    entity_type: str = "transport"

    transport_id: str = ""
    patient_id: str = ""
    origin: str = ""
    destination: str = ""
    requested_at: str = ""


class TransportlinkPatientDeliveredEvent(DomainEvent):
    event_type: str = "transportlink.patient.delivered"
    entity_type: str = "transportlink"

    request_id: str = ""
    destination_facility: str = ""
    delivered_at: str = ""


class TransportlinkPatientLoadedEvent(DomainEvent):
    event_type: str = "transportlink.patient.loaded"
    entity_type: str = "transportlink"

    request_id: str = ""
    vehicle_id: str = ""
    loaded_at: str = ""


class TransportlinkRequestAcceptedEvent(DomainEvent):
    event_type: str = "transportlink.request.accepted"
    entity_type: str = "transportlink"

    request_id: str = ""
    provider_id: str = ""
    accepted_at: str = ""


class TransportlinkRequestCreatedEvent(DomainEvent):
    event_type: str = "transportlink.request.created"
    entity_type: str = "transportlink"

    request_id: str = ""
    origin_facility: str = ""
    destination_facility: str = ""
    patient_acuity: str = ""
    created_at: str = ""


class TransportlinkRequestDeclinedEvent(DomainEvent):
    event_type: str = "transportlink.request.declined"
    entity_type: str = "transportlink"

    request_id: str = ""
    provider_id: str = ""
    decline_reason: str = ""


class TransportlinkVehicleEnrouteToPickupEvent(DomainEvent):
    event_type: str = "transportlink.vehicle.enroute_to_pickup"
    entity_type: str = "transportlink"

    request_id: str = ""
    vehicle_id: str = ""
    eta: str = ""
    enroute_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("transport.assigned", TransportAssignedEvent)
_catalog.register("transport.completed", TransportCompletedEvent)
_catalog.register("transport.eta.updated", TransportEtaUpdatedEvent)
_catalog.register("transport.requested", TransportRequestedEvent)
_catalog.register("transportlink.patient.delivered", TransportlinkPatientDeliveredEvent)
_catalog.register("transportlink.patient.loaded", TransportlinkPatientLoadedEvent)
_catalog.register("transportlink.request.accepted", TransportlinkRequestAcceptedEvent)
_catalog.register("transportlink.request.created", TransportlinkRequestCreatedEvent)
_catalog.register("transportlink.request.declined", TransportlinkRequestDeclinedEvent)
_catalog.register("transportlink.vehicle.enroute_to_pickup", TransportlinkVehicleEnrouteToPickupEvent)
