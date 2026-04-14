"""Fire and NERIS domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class FireIncidentCreatedEvent(DomainEvent):
    event_type: str = "fire.incident.created"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    incident_type: str = ""
    address: str = ""

class FireIncidentStatusChangedEvent(DomainEvent):
    event_type: str = "fire.incident.status_changed"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    previous_status: str = ""
    new_status: str = ""

class FireIncidentClosedEvent(DomainEvent):
    event_type: str = "fire.incident.closed"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    disposition: str = ""

class NerisSubmissionCreatedEvent(DomainEvent):
    event_type: str = "neris.submission.created"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    fire_incident_id: str = ""
    state_code: str = ""

class NerisSubmissionAcknowledgedEvent(DomainEvent):
    event_type: str = "neris.submission.acknowledged"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    acknowledged_at: str = ""

class NerisSubmissionRejectedEvent(DomainEvent):
    event_type: str = "neris.submission.rejected"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    rejection_reason: str = ""

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("fire.incident.created", FireIncidentCreatedEvent)
_catalog.register("fire.incident.status_changed", FireIncidentStatusChangedEvent)
_catalog.register("fire.incident.closed", FireIncidentClosedEvent)
_catalog.register("neris.submission.created", NerisSubmissionCreatedEvent)
_catalog.register("neris.submission.acknowledged", NerisSubmissionAcknowledgedEvent)
_catalog.register("neris.submission.rejected", NerisSubmissionRejectedEvent)
class FireAccountabilityCheckedEvent(DomainEvent):
    event_type: str = "fire.accountability.checked"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    check_type: str = ""
    personnel_accounted: str = ""
    checked_at: str = ""
class FireAlarmDispatchedEvent(DomainEvent):
    event_type: str = "fire.alarm.dispatched"
    entity_type: str = "fire"
    alarm_id: str = ""
    fire_incident_id: str = ""
    dispatched_at: str = ""
class FireAlarmReceivedEvent(DomainEvent):
    event_type: str = "fire.alarm.received"
    entity_type: str = "fire"
    alarm_id: str = ""
    alarm_type: str = ""
    location: str = ""
    received_at: str = ""
class FireApparatusAssignedEvent(DomainEvent):
    event_type: str = "fire.apparatus.assigned"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    apparatus_id: str = ""
    assigned_at: str = ""
class FireApparatusEnrouteEvent(DomainEvent):
    event_type: str = "fire.apparatus.enroute"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    apparatus_id: str = ""
    enroute_at: str = ""
class FireApparatusOnsceneEvent(DomainEvent):
    event_type: str = "fire.apparatus.onscene"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    apparatus_id: str = ""
    onscene_at: str = ""
class FireCauseDeterminedEvent(DomainEvent):
    event_type: str = "fire.cause.determined"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    cause_type: str = ""
    investigator_id: str = ""
    determined_at: str = ""
class FireCommandTransferredEvent(DomainEvent):
    event_type: str = "fire.command.transferred"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    from_commander: str = ""
    to_commander: str = ""
    transferred_at: str = ""
class FireExposureCreatedEvent(DomainEvent):
    event_type: str = "fire.exposure.created"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    exposure_id: str = ""
    exposure_type: str = ""
    address: str = ""
class FireHydrantLocatedEvent(DomainEvent):
    event_type: str = "fire.hydrant.located"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    hydrant_id: str = ""
    flow_rate: str = ""
    located_at: str = ""
class FireIncidentAccountabilityParCompletedEvent(DomainEvent):
    event_type: str = "fire.incident.accountability.par_completed"
    entity_type: str = "fire"
    incident_id: str = ""
    completed_by: str = ""
    all_accounted: str = ""
    completed_at: str = ""
class FireIncidentAccountabilityTagAssignedEvent(DomainEvent):
    event_type: str = "fire.incident.accountability.tag_assigned"
    entity_type: str = "fire"
    incident_id: str = ""
    tag_id: str = ""
    assigned_to: str = ""
    assigned_at: str = ""
class FireIncidentCommandEstablishedEvent(DomainEvent):
    event_type: str = "fire.incident.command_established"
    entity_type: str = "fire"
    incident_id: str = ""
    incident_commander: str = ""
    command_location: str = ""
    established_at: str = ""
class FireIncidentCommandTransferredEvent(DomainEvent):
    event_type: str = "fire.incident.command_transferred"
    entity_type: str = "fire"
    incident_id: str = ""
    from_ic: str = ""
    to_ic: str = ""
    transferred_at: str = ""
class FireIncidentMaydayDeclaredEvent(DomainEvent):
    event_type: str = "fire.incident.mayday.declared"
    entity_type: str = "fire"
    incident_id: str = ""
    declared_by: str = ""
    location: str = ""
    declared_at: str = ""
class FireIncidentSizeUpRecordedEvent(DomainEvent):
    event_type: str = "fire.incident.size_up.recorded"
    entity_type: str = "fire"
    incident_id: str = ""
    building_type: str = ""
    fire_extent: str = ""
    exposures: str = ""
    recorded_by: str = ""
class FireIncidentStrategyDeclaredEvent(DomainEvent):
    event_type: str = "fire.incident.strategy_declared"
    entity_type: str = "fire"
    incident_id: str = ""
    strategy: str = ""
    declared_by: str = ""
    declared_at: str = ""
class FireLossEstimatedEvent(DomainEvent):
    event_type: str = "fire.loss.estimated"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    property_loss: str = ""
    contents_loss: str = ""
    estimated_by: str = ""
class FireMaydayDeclaredEvent(DomainEvent):
    event_type: str = "fire.mayday.declared"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    personnel_id: str = ""
    location: str = ""
    declared_at: str = ""
class FireMaydayResolvedEvent(DomainEvent):
    event_type: str = "fire.mayday.resolved"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    personnel_id: str = ""
    resolution: str = ""
    resolved_at: str = ""
class FireOverhaulCompletedEvent(DomainEvent):
    event_type: str = "fire.overhaul.completed"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    completed_by: str = ""
    completed_at: str = ""
class FirePersonnelAssignedEvent(DomainEvent):
    event_type: str = "fire.personnel.assigned"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    personnel_id: str = ""
    role: str = ""
    assigned_at: str = ""
class FireSafetyEventReportedEvent(DomainEvent):
    event_type: str = "fire.safety_event.reported"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    event_type: str = ""
    reported_by: str = ""
    severity: int = 0
class FireSearchCompletedEvent(DomainEvent):
    event_type: str = "fire.search.completed"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    search_area: str = ""
    all_clear: str = ""
    completed_by: str = ""
class FireSizeUpCompletedEvent(DomainEvent):
    event_type: str = "fire.size_up.completed"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    building_type: str = ""
    occupancy: str = ""
    hazards: str = ""
    completed_by: str = ""
class FireStagingEstablishedEvent(DomainEvent):
    event_type: str = "fire.staging.established"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    staging_location: str = ""
    established_by: str = ""
    established_at: str = ""
class FireVentilationInitiatedEvent(DomainEvent):
    event_type: str = "fire.ventilation.initiated"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    ventilation_type: str = ""
    location: str = ""
    initiated_at: str = ""
class FireWaterSupplyEstablishedEvent(DomainEvent):
    event_type: str = "fire.water_supply.established"
    entity_type: str = "fire"
    fire_incident_id: str = ""
    supply_type: str = ""
    flow_gpm: str = ""
    established_at: str = ""
_catalog.register("fire.accountability.checked", FireAccountabilityCheckedEvent)
_catalog.register("fire.alarm.dispatched", FireAlarmDispatchedEvent)
_catalog.register("fire.alarm.received", FireAlarmReceivedEvent)
_catalog.register("fire.apparatus.assigned", FireApparatusAssignedEvent)
_catalog.register("fire.apparatus.enroute", FireApparatusEnrouteEvent)
_catalog.register("fire.apparatus.onscene", FireApparatusOnsceneEvent)
_catalog.register("fire.cause.determined", FireCauseDeterminedEvent)
_catalog.register("fire.command.transferred", FireCommandTransferredEvent)
_catalog.register("fire.exposure.created", FireExposureCreatedEvent)
_catalog.register("fire.hydrant.located", FireHydrantLocatedEvent)
_catalog.register("fire.incident.accountability.par_completed", FireIncidentAccountabilityParCompletedEvent)
_catalog.register("fire.incident.accountability.tag_assigned", FireIncidentAccountabilityTagAssignedEvent)
_catalog.register("fire.incident.command_established", FireIncidentCommandEstablishedEvent)
_catalog.register("fire.incident.command_transferred", FireIncidentCommandTransferredEvent)
_catalog.register("fire.incident.mayday.declared", FireIncidentMaydayDeclaredEvent)
_catalog.register("fire.incident.size_up.recorded", FireIncidentSizeUpRecordedEvent)
_catalog.register("fire.incident.strategy_declared", FireIncidentStrategyDeclaredEvent)
_catalog.register("fire.loss.estimated", FireLossEstimatedEvent)
_catalog.register("fire.mayday.declared", FireMaydayDeclaredEvent)
_catalog.register("fire.mayday.resolved", FireMaydayResolvedEvent)
_catalog.register("fire.overhaul.completed", FireOverhaulCompletedEvent)
_catalog.register("fire.personnel.assigned", FirePersonnelAssignedEvent)
_catalog.register("fire.safety_event.reported", FireSafetyEventReportedEvent)
_catalog.register("fire.search.completed", FireSearchCompletedEvent)
_catalog.register("fire.size_up.completed", FireSizeUpCompletedEvent)
_catalog.register("fire.staging.established", FireStagingEstablishedEvent)
_catalog.register("fire.ventilation.initiated", FireVentilationInitiatedEvent)
_catalog.register("fire.water_supply.established", FireWaterSupplyEstablishedEvent)
