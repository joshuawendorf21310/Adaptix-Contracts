from adaptix_contracts.events.registry import ALL_EVENTS, FIRE_INCIDENT_STATUS_UPDATED, NERIS_VALIDATION_COMPLETED
from adaptix_contracts.fire import FIRE_EVENTS, FireIncidentType, FireUnitStatus, NerisReadinessContract
from adaptix_contracts.neris import NERIS_EVENTS, NerisValidationStatus


def test_fire_contract_package_exports_expected_symbols() -> None:
    readiness = NerisReadinessContract(
        incident_id="incident-1",
        ready=False,
        missing_fields=["incident_type"],
        filled_fields=["incident_number"],
        total_required=2,
        total_filled=1,
    )

    assert readiness.incident_id == "incident-1"
    assert FireIncidentType.STRUCTURE_FIRE.value == "STRUCTURE_FIRE"
    assert FireUnitStatus.AVAILABLE.value == "AVAILABLE"
    assert NerisValidationStatus.VALIDATION_PASSED.value == "VALIDATION_PASSED"


def test_fire_and_neris_events_are_registered() -> None:
    assert "fire.incident.status.updated" in FIRE_EVENTS
    assert FIRE_INCIDENT_STATUS_UPDATED in ALL_EVENTS
    assert NERIS_VALIDATION_COMPLETED in ALL_EVENTS
    assert "neris.validation.completed" in NERIS_EVENTS