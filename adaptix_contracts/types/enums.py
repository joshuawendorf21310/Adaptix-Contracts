"""Compatibility aliases for narcotics enum imports.

These names preserve the historic `adaptix_contracts.types.enums` import path
used by consumer services while delegating to the canonical schema module.
"""

from adaptix_contracts.schemas.narcotic import (
    ActionStatus,
    ComplianceType,
    ControlledSubstanceSchedule,
    CountType,
    KitStatus,
    NarcoticAccessType,
    NarcoticInvestigationStatus,
    NarcoticMedicationStatus,
    NarcoticTransactionType,
    NarcoticVaultStatus,
    NarcoticVaultType,
    RecallStatus,
    ShiftPhase,
    WitnessEventType,
)

VaultType = NarcoticVaultType
VaultStatus = NarcoticVaultStatus
DEASchedule = ControlledSubstanceSchedule
MedicationStatus = NarcoticMedicationStatus
AccessType = NarcoticAccessType
InvestigationStatus = NarcoticInvestigationStatus

__all__ = [
    "AccessType",
    "ActionStatus",
    "ComplianceType",
    "CountType",
    "DEASchedule",
    "InvestigationStatus",
    "KitStatus",
    "MedicationStatus",
    "NarcoticTransactionType",
    "RecallStatus",
    "ShiftPhase",
    "VaultStatus",
    "VaultType",
    "WitnessEventType",
]
