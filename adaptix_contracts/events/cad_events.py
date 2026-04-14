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
class CadCallMergedEvent(DomainEvent):
    event_type: str = "cad.call.merged"
    entity_type: str = "cad"
    master_call_id: str = ""
    merged_call_ids: str = ""
    merged_by: str = ""
    merged_at: str = ""
class CadCallSplitEvent(DomainEvent):
    event_type: str = "cad.call.split"
    entity_type: str = "cad"
    original_call_id: str = ""
    new_call_ids: str = ""
    split_by: str = ""
    split_at: str = ""
class CadCallTransferredEvent(DomainEvent):
    event_type: str = "cad.call.transferred"
    entity_type: str = "cad"
    call_id: str = ""
    from_agency: str = ""
    to_agency: str = ""
    transferred_by: str = ""
    transferred_at: str = ""
class CadCallerCallbackCompletedEvent(DomainEvent):
    event_type: str = "cad.caller.callback.completed"
    entity_type: str = "cad"
    call_id: str = ""
    completed_by: str = ""
    completed_at: str = ""
class CadCallerCallbackRequestedEvent(DomainEvent):
    event_type: str = "cad.caller.callback.requested"
    entity_type: str = "cad"
    call_id: str = ""
    callback_number: str = ""
    requested_at: str = ""
class CadUnitRecommendationGeneratedEvent(DomainEvent):
    event_type: str = "cad.unit.recommendation.generated"
    entity_type: str = "cad"
    call_id: str = ""
    recommended_units: str = ""
    recommendation_score: float = 0.0
    generated_at: str = ""
class DispatchCallReceivedEvent(DomainEvent):
    event_type: str = "dispatch.call.received"
    entity_type: str = "dispatch"
    call_id: str = ""
    caller_number: str = ""
    call_type: str = ""
    received_at: str = ""
class DispatchCallTransferredEvent(DomainEvent):
    event_type: str = "dispatch.call.transferred"
    entity_type: str = "dispatch"
    call_id: str = ""
    from_dispatcher: str = ""
    to_dispatcher: str = ""
    transferred_at: str = ""
class DispatchCallTriagedEvent(DomainEvent):
    event_type: str = "dispatch.call.triaged"
    entity_type: str = "dispatch"
    call_id: str = ""
    triage_level: int = 0
    triaged_by: str = ""
    triaged_at: str = ""
class DispatchPsapTransferReceivedEvent(DomainEvent):
    event_type: str = "dispatch.psap.transfer_received"
    entity_type: str = "dispatch"
    call_id: str = ""
    from_psap: str = ""
    to_psap: str = ""
    transferred_at: str = ""
class DispatchTimelineMilestoneEvent(DomainEvent):
    event_type: str = "dispatch.timeline.milestone"
    entity_type: str = "dispatch"
    incident_id: str = ""
    milestone_type: str = ""
    timestamp: str = ""
class DispatchUnitRecommendedEvent(DomainEvent):
    event_type: str = "dispatch.unit.recommended"
    entity_type: str = "dispatch"
    incident_id: str = ""
    unit_id: str = ""
    recommendation_score: float = 0.0
    recommended_at: str = ""
class DispatchZoneCoverageChangedEvent(DomainEvent):
    event_type: str = "dispatch.zone.coverage_changed"
    entity_type: str = "dispatch"
    zone_id: str = ""
    coverage_level: int = 0
    available_units: str = ""
    changed_at: str = ""
class UnitAvailableEvent(DomainEvent):
    event_type: str = "unit.available"
    entity_type: str = "unit"
    unit_id: str = ""
    available_at: str = ""
class UnitClearedEvent(DomainEvent):
    event_type: str = "unit.cleared"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    cleared_at: str = ""
class UnitCrewAssignedEvent(DomainEvent):
    event_type: str = "unit.crew.assigned"
    entity_type: str = "unit"
    unit_id: str = ""
    crew_member_ids: str = ""
    assigned_at: str = ""
class UnitDispatchedEvent(DomainEvent):
    event_type: str = "unit.dispatched"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    dispatched_at: str = ""
class UnitEnrouteEvent(DomainEvent):
    event_type: str = "unit.enroute"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    enroute_at: str = ""
class UnitLocationUpdatedEvent(DomainEvent):
    event_type: str = "unit.location.updated"
    entity_type: str = "unit"
    unit_id: str = ""
    latitude: str = ""
    longitude: str = ""
    speed: str = ""
    heading: str = ""
    updated_at: str = ""
class UnitOnsceneEvent(DomainEvent):
    event_type: str = "unit.onscene"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    onscene_at: str = ""
class UnitOutOfServiceEvent(DomainEvent):
    event_type: str = "unit.out_of_service"
    entity_type: str = "unit"
    unit_id: str = ""
    reason: str = ""
    oos_at: str = ""
class UnitTransportCompletedEvent(DomainEvent):
    event_type: str = "unit.transport.completed"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    transport_completed_at: str = ""
class UnitTransportStartedEvent(DomainEvent):
    event_type: str = "unit.transport.started"
    entity_type: str = "unit"
    unit_id: str = ""
    incident_id: str = ""
    destination: str = ""
    transport_started_at: str = ""
_catalog.register("cad.call.merged", CadCallMergedEvent)
_catalog.register("cad.call.split", CadCallSplitEvent)
_catalog.register("cad.call.transferred", CadCallTransferredEvent)
_catalog.register("cad.caller.callback.completed", CadCallerCallbackCompletedEvent)
_catalog.register("cad.caller.callback.requested", CadCallerCallbackRequestedEvent)
_catalog.register("cad.unit.recommendation.generated", CadUnitRecommendationGeneratedEvent)
_catalog.register("dispatch.call.received", DispatchCallReceivedEvent)
_catalog.register("dispatch.call.transferred", DispatchCallTransferredEvent)
_catalog.register("dispatch.call.triaged", DispatchCallTriagedEvent)
_catalog.register("dispatch.psap.transfer_received", DispatchPsapTransferReceivedEvent)
_catalog.register("dispatch.timeline.milestone", DispatchTimelineMilestoneEvent)
_catalog.register("dispatch.unit.recommended", DispatchUnitRecommendedEvent)
_catalog.register("dispatch.zone.coverage_changed", DispatchZoneCoverageChangedEvent)
_catalog.register("unit.available", UnitAvailableEvent)
_catalog.register("unit.cleared", UnitClearedEvent)
_catalog.register("unit.crew.assigned", UnitCrewAssignedEvent)
_catalog.register("unit.dispatched", UnitDispatchedEvent)
_catalog.register("unit.enroute", UnitEnrouteEvent)
_catalog.register("unit.location.updated", UnitLocationUpdatedEvent)
_catalog.register("unit.onscene", UnitOnsceneEvent)
_catalog.register("unit.out_of_service", UnitOutOfServiceEvent)
_catalog.register("unit.transport.completed", UnitTransportCompletedEvent)
_catalog.register("unit.transport.started", UnitTransportStartedEvent)
