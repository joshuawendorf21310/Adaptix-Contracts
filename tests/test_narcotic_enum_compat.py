from adaptix_contracts.schemas.narcotic import KitStatus as CanonicalKitStatus
from adaptix_contracts.types.enums import (
    ActionStatus,
    ComplianceType,
    CountType,
    DEASchedule,
    InvestigationStatus,
    KitStatus,
    MedicationStatus,
    RecallStatus,
    ShiftPhase,
    VaultStatus,
    VaultType,
    WitnessEventType,
)


def test_legacy_narcotics_enum_imports_resolve_from_canonical_package() -> None:
    assert VaultType.STATION.value == "station"
    assert VaultStatus.ACTIVE.value == "active"
    assert DEASchedule.SCHEDULE_II.value == "II"
    assert MedicationStatus.AVAILABLE.value == "available"
    assert CountType.START_SHIFT.value == "start_shift"
    assert ShiftPhase.END.value == "end"
    assert RecallStatus.OPEN.value == "open"
    assert WitnessEventType.WASTE.value == "waste"
    assert ComplianceType.DEA_106.value == "dea_106"
    assert ActionStatus.OVERDUE.value == "overdue"
    assert InvestigationStatus.IN_PROGRESS.value == "in_progress"
    assert KitStatus.RESTOCKING is CanonicalKitStatus.RESTOCKING
