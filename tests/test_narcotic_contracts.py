"""Regression tests for shared narcotics contracts."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from adaptix_contracts.schemas import (
    AccessLogListResponse,
    AccessLogResponse,
    ControlledSubstanceSchedule,
    DEAReportRequest,
    DiscrepancyResponse,
    ExpiringMedicationsRequest,
    MedicationCreateRequest,
    NarcoticAccessType,
    NarcoticDiscrepancyRecordedEvent,
    NarcoticInvestigationStatus,
    NarcoticMedicationAddedEvent,
    NarcoticMedicationStatus,
    NarcoticTransactionRecordedEvent,
    NarcoticTransactionType,
    NarcoticVaultCreatedEvent,
    NarcoticVaultStatus,
    NarcoticVaultType,
    VaultCreateRequest,
    VaultResponse,
)


def _ts() -> datetime:
    return datetime(2026, 4, 21, 12, 0, tzinfo=UTC)


def test_vault_response_round_trip() -> None:
    vault = VaultResponse(
        id=uuid4(),
        tenant_id=uuid4(),
        vault_name="Station 1 Main Vault",
        location="Station 1 / Med Room",
        vault_type=NarcoticVaultType.STATION,
        status=NarcoticVaultStatus.ACTIVE,
        last_audit_date=None,
        next_audit_date=_ts(),
        created_at=_ts(),
        updated_at=_ts(),
        deleted_at=None,
        version=3,
    )

    restored = VaultResponse.model_validate_json(vault.model_dump_json())
    assert restored == vault


def test_medication_create_request_rejects_negative_quantity() -> None:
    with pytest.raises(ValidationError):
        MedicationCreateRequest(
            drug_name="Midazolam",
            dea_schedule=ControlledSubstanceSchedule.SCHEDULE_IV,
            strength="5mg/ml",
            form="injection",
            vault_id=uuid4(),
            quantity=-1,
            lot_number="LOT-123",
            expiration_date=_ts(),
        )


def test_expiring_medications_request_bounds_days_ahead() -> None:
    with pytest.raises(ValidationError):
        ExpiringMedicationsRequest(days_ahead=0)


def test_dea_report_request_round_trip() -> None:
    report = DEAReportRequest(start_date=_ts(), end_date=_ts())
    assert DEAReportRequest.model_validate_json(report.model_dump_json()) == report


def test_transaction_event_keeps_event_type_stable() -> None:
    event = NarcoticTransactionRecordedEvent(
        transaction_id=uuid4(),
        tenant_id=uuid4(),
        medication_id=uuid4(),
        transaction_type=NarcoticTransactionType.WASTE,
        quantity=2.5,
        occurred_at=_ts(),
    )
    assert event.event_type == "narcotic.transaction.recorded"


def test_access_log_list_response_supports_nested_round_trip() -> None:
    item = AccessLogResponse(
        id=uuid4(),
        tenant_id=uuid4(),
        vault_id=uuid4(),
        user_id=uuid4(),
        access_time=_ts(),
        access_type=NarcoticAccessType.AUDIT,
        authorized_by=None,
        notes="scheduled audit",
        created_at=_ts(),
        updated_at=_ts(),
        deleted_at=None,
        version=1,
    )
    payload = AccessLogListResponse(items=[item], total=1)
    assert AccessLogListResponse.model_validate_json(payload.model_dump_json()) == payload


def test_discrepancy_response_accepts_investigation_status() -> None:
    discrepancy = DiscrepancyResponse(
        id=uuid4(),
        tenant_id=uuid4(),
        audit_id=uuid4(),
        medication_id=uuid4(),
        expected_count=10,
        actual_count=8,
        variance=-2,
        investigation_status=NarcoticInvestigationStatus.IN_PROGRESS,
        resolved_by=None,
        resolution_date=None,
        created_at=_ts(),
        updated_at=_ts(),
        deleted_at=None,
        version=1,
    )
    assert discrepancy.investigation_status == NarcoticInvestigationStatus.IN_PROGRESS


def test_representative_event_contracts_instantiate() -> None:
    vault_event = NarcoticVaultCreatedEvent(
        vault_id=uuid4(),
        tenant_id=uuid4(),
        vault_name="Supervisor Safe",
        created_at=_ts(),
    )
    medication_event = NarcoticMedicationAddedEvent(
        medication_id=uuid4(),
        tenant_id=uuid4(),
        vault_id=uuid4(),
        drug_name="Fentanyl",
        quantity=5,
        occurred_at=_ts(),
    )
    discrepancy_event = NarcoticDiscrepancyRecordedEvent(
        discrepancy_id=uuid4(),
        tenant_id=uuid4(),
        audit_id=uuid4(),
        medication_id=uuid4(),
        variance=1,
        occurred_at=_ts(),
    )

    assert vault_event.event_type == "narcotic.vault.created"
    assert medication_event.event_type == "narcotic.medication.added"
    assert discrepancy_event.event_type == "narcotic.discrepancy.recorded"


def test_vault_create_request_requires_name() -> None:
    with pytest.raises(ValidationError):
        VaultCreateRequest(vault_name="", location="Station 1", vault_type=NarcoticVaultType.STATION)
