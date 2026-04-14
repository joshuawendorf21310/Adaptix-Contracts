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
class MdtFormSubmittedEvent(DomainEvent):
    event_type: str = "mdt.form.submitted"
    entity_type: str = "mdt"
    form_id: str = ""
    form_type: str = ""
    unit_id: str = ""
    submitted_by: str = ""
    submitted_at: str = ""
class MdtGeofenceEnteredEvent(DomainEvent):
    event_type: str = "mdt.geofence.entered"
    entity_type: str = "mdt"
    device_id: str = ""
    geofence_id: str = ""
    geofence_name: str = ""
    entered_at: str = ""
class MdtGeofenceExitedEvent(DomainEvent):
    event_type: str = "mdt.geofence.exited"
    entity_type: str = "mdt"
    device_id: str = ""
    geofence_id: str = ""
    geofence_name: str = ""
    exited_at: str = ""
    duration: str = ""
class MdtLocationUpdatedEvent(DomainEvent):
    event_type: str = "mdt.location.updated"
    entity_type: str = "mdt"
    device_id: str = ""
    latitude: str = ""
    longitude: str = ""
    heading: str = ""
    speed: str = ""
    updated_at: str = ""
class MdtNavigationArrivedEvent(DomainEvent):
    event_type: str = "mdt.navigation.arrived"
    entity_type: str = "mdt"
    unit_id: str = ""
    destination: str = ""
    arrived_at: str = ""
class MdtNavigationEtaUpdatedEvent(DomainEvent):
    event_type: str = "mdt.navigation.eta_updated"
    entity_type: str = "mdt"
    device_id: str = ""
    destination: str = ""
    eta: str = ""
    distance_remaining: str = ""
class MdtNavigationRouteRequestedEvent(DomainEvent):
    event_type: str = "mdt.navigation.route_requested"
    entity_type: str = "mdt"
    device_id: str = ""
    destination: str = ""
    route_options: str = ""
class MdtNavigationStartedEvent(DomainEvent):
    event_type: str = "mdt.navigation.started"
    entity_type: str = "mdt"
    unit_id: str = ""
    destination: str = ""
    started_at: str = ""
class MdtPhotoCapturedEvent(DomainEvent):
    event_type: str = "mdt.photo.captured"
    entity_type: str = "mdt"
    photo_id: str = ""
    incident_id: str = ""
    captured_by: str = ""
    captured_at: str = ""
class MdtShiftEndedEvent(DomainEvent):
    event_type: str = "mdt.shift.ended"
    entity_type: str = "mdt"
    shift_id: str = ""
    user_id: str = ""
    ended_at: str = ""
    total_calls: str = ""
class MdtShiftStartedEvent(DomainEvent):
    event_type: str = "mdt.shift.started"
    entity_type: str = "mdt"
    shift_id: str = ""
    user_id: str = ""
    vehicle_id: str = ""
    started_at: str = ""
class MdtSignatureCapturedEvent(DomainEvent):
    event_type: str = "mdt.signature.captured"
    entity_type: str = "mdt"
    signature_id: str = ""
    incident_id: str = ""
    signature_type: str = ""
    captured_at: str = ""
_catalog.register("mdt.form.submitted", MdtFormSubmittedEvent)
_catalog.register("mdt.geofence.entered", MdtGeofenceEnteredEvent)
_catalog.register("mdt.geofence.exited", MdtGeofenceExitedEvent)
_catalog.register("mdt.location.updated", MdtLocationUpdatedEvent)
_catalog.register("mdt.navigation.arrived", MdtNavigationArrivedEvent)
_catalog.register("mdt.navigation.eta_updated", MdtNavigationEtaUpdatedEvent)
_catalog.register("mdt.navigation.route_requested", MdtNavigationRouteRequestedEvent)
_catalog.register("mdt.navigation.started", MdtNavigationStartedEvent)
_catalog.register("mdt.photo.captured", MdtPhotoCapturedEvent)
_catalog.register("mdt.shift.ended", MdtShiftEndedEvent)
_catalog.register("mdt.shift.started", MdtShiftStartedEvent)
_catalog.register("mdt.signature.captured", MdtSignatureCapturedEvent)
