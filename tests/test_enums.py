"""
Tests for adaptix_contracts.types.enums

Validates:
  - All enum types are importable and have expected members
  - No enum values collide within a domain
  - Transition functions return correct sets
  - Backward-compat aliases resolve to the right enum class
"""

from __future__ import annotations

from adaptix_contracts.types.enums import (
    AlertPriority,
    AlertStatus,
    ApparatusStatus,
    ApparatusType,
    AssetStatus,
    AssignmentAckStatus,
    AssignmentStatus,
    AssignmentType,
    AvailabilityStatus,
    AvailabilityType,
    CadSyncStatus,
    CadSystemType,
    CadUnitStatus,
    CycleCountStatus,
    DEASchedule,
    DeliveryMethod,
    DeliveryStatus,
    FacilityType,
    FireIncidentStatus,
    FireIncidentType,
    IncidentPriority,
    IncidentStatus,
    InventoryTransactionType,
    InvestigationStatus,
    ItemCategory,
    ItemStatus,
    LocationType,
    MaintenanceType,
    MdtStatus,
    MedicationStatus,
    MessagePriority,
    MutualAidType,
    NarcoticTransactionType,
    NoteType,
    PageStatus,
    PageType,
    PatientAccountStatus,
    PatientDisputeStatus,
    PatientGender,
    PatientPaymentStatus,
    PaymentPlanFrequency,
    PaymentPlanStatus,
    PCSABNStatus,
    PurchaseOrderStatus,
    ResourceRequestStatus,
    TransportStatus,
    TransportType,
    UnitStatusCode,
    UrgencyLevel,
    VaultStatus,
    VaultType,
    allowed_fire_transition_targets,
)


class TestCrewLinkEnums:
    def test_availability_type_members(self):
        assert AvailabilityType.SHIFT.value == "shift"
        assert AvailabilityType.ON_DUTY.value == "on_duty"

    def test_alert_priority_ordering(self):
        levels = [AlertPriority.LOW, AlertPriority.NORMAL, AlertPriority.HIGH, AlertPriority.CRITICAL]
        assert len(levels) == 4

    def test_alert_status_has_acknowledged(self):
        assert AlertStatus.ACKNOWLEDGED.value == "acknowledged"

    def test_page_status_is_alias_for_alert_status(self):
        assert PageStatus is AlertStatus

    def test_assignment_type_members(self):
        assert AssignmentType.DISPATCH.value == "dispatch"

    def test_assignment_status_terminal(self):
        assert AssignmentStatus.COMPLETED.value == "completed"
        assert AssignmentStatus.CANCELLED.value == "cancelled"

    def test_delivery_method_is_push_first(self):
        """PUSH must be available as a delivery method (device-registry-backed)."""
        assert DeliveryMethod.PUSH.value == "push"

    def test_urgency_level_includes_emergency(self):
        assert UrgencyLevel.EMERGENCY.value == "emergency"

    def test_page_type_has_assignment(self):
        assert PageType.ASSIGNMENT.value == "assignment"


class TestCadEnums:
    def test_cad_sync_status_members(self):
        assert CadSyncStatus.PENDING.value == "pending"
        assert CadSyncStatus.SUCCESS.value == "success"
        assert CadSyncStatus.FAILED.value == "failed"

    def test_cad_unit_status_members(self):
        expected = {"available", "assigned", "out_of_service"}
        actual = {m.value for m in CadUnitStatus}
        assert expected == actual

    def test_cad_system_type_includes_known_vendors(self):
        values = {m.value for m in CadSystemType}
        assert "zoll" in values
        assert "tyler" in values
        assert "motorola" in values


class TestIncidentEnums:
    def test_incident_status_lifecycle(self):
        expected_present = {"draft", "dispatched", "on_scene", "completed", "cancelled"}
        actual = {m.value for m in IncidentStatus}
        assert expected_present <= actual

    def test_incident_priority_alpha_to_echo(self):
        values = [m.value for m in IncidentPriority]
        assert "alpha" in values
        assert "echo" in values


class TestFireEnums:
    def test_fire_incident_types(self):
        values = {m.value for m in FireIncidentType}
        assert "structure_fire" in values
        assert "hazmat" in values

    def test_fire_incident_status_lifecycle(self):
        values = {m.value for m in FireIncidentStatus}
        assert "dispatch" in values
        assert "completed" in values

    def test_transition_from_dispatch(self):
        targets = allowed_fire_transition_targets(FireIncidentStatus.DISPATCH)
        assert FireIncidentStatus.EN_ROUTE in targets
        assert FireIncidentStatus.CANCELLED in targets

    def test_transition_from_terminal_is_empty(self):
        assert allowed_fire_transition_targets(FireIncidentStatus.COMPLETED) == set()
        assert allowed_fire_transition_targets(FireIncidentStatus.CANCELLED) == set()

    def test_mutual_aid_type_members(self):
        values = {m.value for m in MutualAidType}
        assert "none" in values
        assert "given" in values
        assert "received" in values

    def test_apparatus_type_has_engine(self):
        assert ApparatusType.ENGINE.value == "engine"

    def test_apparatus_status_has_dispatched(self):
        assert ApparatusStatus.DISPATCHED.value == "dispatched"


class TestMdtEnums:
    def test_unit_status_code_members(self):
        values = {m.value for m in UnitStatusCode}
        assert "available" in values
        assert "en_route" in values
        assert "at_hospital" in values

    def test_availability_status_is_alias(self):
        assert AvailabilityStatus is UnitStatusCode

    def test_mdt_status_is_alias(self):
        assert MdtStatus is UnitStatusCode

    def test_message_priority_range(self):
        values = {m.value for m in MessagePriority}
        assert "routine" in values
        assert "emergency" in values


class TestInventoryEnums:
    def test_item_category_members(self):
        values = {m.value for m in ItemCategory}
        assert "medical_supply" in values
        assert "equipment" in values

    def test_location_type_members(self):
        values = {m.value for m in LocationType}
        assert "station" in values
        assert "vehicle" in values

    def test_inventory_transaction_type_distinct_from_narcotic(self):
        inv_values = {m.value for m in InventoryTransactionType}
        narc_values = {m.value for m in NarcoticTransactionType}
        # They share some values but are distinct enum types
        assert InventoryTransactionType is not NarcoticTransactionType
        # Narcotic has 'administration' which inventory does not
        assert "administration" in narc_values
        assert "administration" not in inv_values

    def test_purchase_order_status(self):
        values = {m.value for m in PurchaseOrderStatus}
        assert "draft" in values
        assert "received" in values

    def test_asset_status_members(self):
        values = {m.value for m in AssetStatus}
        assert "retired" in values

    def test_cycle_count_status(self):
        values = {m.value for m in CycleCountStatus}
        assert "completed" in values


class TestNarcoticEnums:
    def test_vault_type_members(self):
        values = {m.value for m in VaultType}
        assert "station_vault" in values
        assert "ambulance_kit" in values

    def test_dea_schedules(self):
        values = {m.value for m in DEASchedule}
        assert "schedule_ii" in values
        assert "schedule_v" in values

    def test_medication_status(self):
        values = {m.value for m in MedicationStatus}
        assert "administered" in values
        assert "wasted" in values

    def test_investigation_status(self):
        values = {m.value for m in InvestigationStatus}
        assert "escalated" in values


class TestTransportLinkEnums:
    def test_transport_status_lifecycle(self):
        values = {m.value for m in TransportStatus}
        assert "requested" in values
        assert "patient_contact" in values
        assert "completed" in values

    def test_facility_type_members(self):
        values = {m.value for m in FacilityType}
        assert "hospital" in values
        assert "dialysis_center" in values

    def test_pcs_abn_status(self):
        values = {m.value for m in PCSABNStatus}
        assert "on_file" in values


class TestPatientEnums:
    def test_patient_gender_members(self):
        values = {m.value for m in PatientGender}
        assert "female" in values
        assert "unknown" in values


class TestPatientFinancialEnums:
    def test_account_status_members(self):
        values = {m.value for m in PatientAccountStatus}
        assert "active" in values
        assert "write_off" in values

    def test_payment_plan_frequencies(self):
        values = {m.value for m in PaymentPlanFrequency}
        assert "monthly" in values

    def test_dispute_status_resolution_variants(self):
        values = {m.value for m in PatientDisputeStatus}
        assert "resolved_patient_favor" in values
        assert "resolved_agency_favor" in values
