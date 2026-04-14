"""AIr domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class AirFlightDepartedEvent(DomainEvent):
    event_type: str = "air.flight.departed"
    entity_type: str = "air"

    mission_id: str = ""
    aircraft_id: str = ""
    departure_location: str = ""
    departed_at: str = ""


class AirFlightLandedEvent(DomainEvent):
    event_type: str = "air.flight.landed"
    entity_type: str = "air"

    mission_id: str = ""
    aircraft_id: str = ""
    landing_location: str = ""
    landed_at: str = ""


class AirFuelAddedEvent(DomainEvent):
    event_type: str = "air.fuel.added"
    entity_type: str = "air"

    aircraft_id: str = ""
    fuel_quantity: str = ""
    fuel_type: str = ""
    added_at: str = ""


class AirLandingZoneEstablishedEvent(DomainEvent):
    event_type: str = "air.landing_zone.established"
    entity_type: str = "air"

    mission_id: str = ""
    lz_coordinates: str = ""
    lz_secure: str = ""
    established_by: str = ""


class AirMaintenanceRequiredEvent(DomainEvent):
    event_type: str = "air.maintenance.required"
    entity_type: str = "air"

    aircraft_id: str = ""
    maintenance_type: str = ""
    hours_remaining: str = ""
    required_by: str = ""


class AirMissionAcceptedEvent(DomainEvent):
    event_type: str = "air.mission.accepted"
    entity_type: str = "air"

    mission_id: str = ""
    aircraft_id: str = ""
    pilot_id: str = ""
    accepted_at: str = ""


class AirMissionCreatedEvent(DomainEvent):
    event_type: str = "air.mission.created"
    entity_type: str = "air"

    mission_id: str = ""
    mission_type: str = ""
    requested_at: str = ""


class AirMissionDeclinedEvent(DomainEvent):
    event_type: str = "air.mission.declined"
    entity_type: str = "air"

    mission_id: str = ""
    reason: str = ""


class AirPatientHandoffCompletedEvent(DomainEvent):
    event_type: str = "air.patient.handoff_completed"
    entity_type: str = "air"

    mission_id: str = ""
    patient_id: str = ""
    destination_facility: str = ""
    handoff_at: str = ""


class AirPatientLoadedEvent(DomainEvent):
    event_type: str = "air.patient.loaded"
    entity_type: str = "air"

    mission_id: str = ""
    patient_id: str = ""
    loaded_at: str = ""


class AirPilotDutyEndedEvent(DomainEvent):
    event_type: str = "air.pilot.duty_ended"
    entity_type: str = "air"

    pilot_id: str = ""
    aircraft_id: str = ""
    duty_end_at: str = ""
    flight_hours: str = ""


class AirPilotDutyStartedEvent(DomainEvent):
    event_type: str = "air.pilot.duty_started"
    entity_type: str = "air"

    pilot_id: str = ""
    aircraft_id: str = ""
    duty_start_at: str = ""


class AirPreflightCompletedEvent(DomainEvent):
    event_type: str = "air.preflight.completed"
    entity_type: str = "air"

    aircraft_id: str = ""
    pilot_id: str = ""
    checklist_completed: str = ""
    completed_at: str = ""


class AirReadinessCheckedEvent(DomainEvent):
    event_type: str = "air.readiness.checked"
    entity_type: str = "air"

    aircraft_id: str = ""
    is_ready: bool = False
    maintenance_status: str = ""
    fuel_level: int = 0

class AirRiskAssessedEvent(DomainEvent):
    event_type: str = "air.risk.assessed"
    entity_type: str = "air"

    mission_id: str = ""
    risk_score: float = 0.0
    risk_factors: str = ""
    assessed_by: str = ""


class AirSafetyEventReportedEvent(DomainEvent):
    event_type: str = "air.safety_event.reported"
    entity_type: str = "air"

    mission_id: str = ""
    event_type: str = ""
    severity: int = 0
    reported_by: str = ""


class AirSceneRequestReceivedEvent(DomainEvent):
    event_type: str = "air.scene_request.received"
    entity_type: str = "air"

    request_id: str = ""
    scene_location: str = ""
    patient_condition: str = ""
    requested_by: str = ""


class AirWeatherCheckedEvent(DomainEvent):
    event_type: str = "air.weather.checked"
    entity_type: str = "air"

    mission_id: str = ""
    weather_conditions: str = ""
    flight_clearance: str = ""


class AirWeightBalanceCalculatedEvent(DomainEvent):
    event_type: str = "air.weight_balance.calculated"
    entity_type: str = "air"

    mission_id: str = ""
    aircraft_id: str = ""
    total_weight: str = ""
    cg_location: str = ""
    within_limits: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("air.flight.departed", AirFlightDepartedEvent)
_catalog.register("air.flight.landed", AirFlightLandedEvent)
_catalog.register("air.fuel.added", AirFuelAddedEvent)
_catalog.register("air.landing_zone.established", AirLandingZoneEstablishedEvent)
_catalog.register("air.maintenance.required", AirMaintenanceRequiredEvent)
_catalog.register("air.mission.accepted", AirMissionAcceptedEvent)
_catalog.register("air.mission.created", AirMissionCreatedEvent)
_catalog.register("air.mission.declined", AirMissionDeclinedEvent)
_catalog.register("air.patient.handoff_completed", AirPatientHandoffCompletedEvent)
_catalog.register("air.patient.loaded", AirPatientLoadedEvent)
_catalog.register("air.pilot.duty_ended", AirPilotDutyEndedEvent)
_catalog.register("air.pilot.duty_started", AirPilotDutyStartedEvent)
_catalog.register("air.preflight.completed", AirPreflightCompletedEvent)
_catalog.register("air.readiness.checked", AirReadinessCheckedEvent)
_catalog.register("air.risk.assessed", AirRiskAssessedEvent)
_catalog.register("air.safety_event.reported", AirSafetyEventReportedEvent)
_catalog.register("air.scene_request.received", AirSceneRequestReceivedEvent)
_catalog.register("air.weather.checked", AirWeatherCheckedEvent)
_catalog.register("air.weight_balance.calculated", AirWeightBalanceCalculatedEvent)
