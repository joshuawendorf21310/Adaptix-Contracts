"""Representative validation and round-trip tests for key Adaptix contracts."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from adaptix_contracts.schemas import (
    AuditActionType,
    AuditActorType,
    AuditContext,
    AuditRecord,
    AuditSeverity,
    ClaimContract,
    ClaimCreatedEvent,
    ClaimLineItem,
    ClaimStatus,
    ClearinghouseProvider,
    DomainEvent,
    UserAuthContext,
    WorkflowContext,
    WorkflowExecution,
    WorkflowStatus,
)


def _timestamp() -> datetime:
    """Return a deterministic UTC timestamp for regression tests."""

    return datetime(2026, 4, 21, 12, 0, tzinfo=UTC)


def _build_domain_event() -> DomainEvent:
    """Create a representative cross-domain event payload."""

    return DomainEvent(
        event_id=uuid4(),
        tenant_id=uuid4(),
        event_type="billing.claim.created",
        source_domain="billing",
        payload={"claim_id": "claim-001"},
        published_at=_timestamp(),
        correlation_id="corr-001",
    )


def _build_user_auth_context() -> UserAuthContext:
    """Create a representative cross-service auth context."""

    return UserAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        role="admin",
        email="ops@adaptix.test",
    )


def _build_audit_record() -> AuditRecord:
    """Create a representative immutable audit record."""

    return AuditRecord(
        audit_id="audit-001",
        actor_type=AuditActorType.SYSTEM,
        action_type=AuditActionType.CREATE,
        resource_type="claim",
        success=True,
        severity=AuditSeverity.LOW,
        context=AuditContext(
            tenant_id="tenant-001",
            correlation_id="corr-001",
            service_name="contracts-test",
        ),
        changed_fields=["status"],
        occurred_at=_timestamp(),
    )


def _build_claim_contract() -> ClaimContract:
    """Create a representative billing claim contract."""

    return ClaimContract(
        claim_id="claim-001",
        tenant_id="tenant-001",
        patient_id="patient-001",
        status=ClaimStatus.READY,
        total_charge_cents=120000,
        total_paid_cents=10000,
        total_adjustment_cents=5000,
        balance_cents=105000,
        line_items=[
            ClaimLineItem(
                line_id="line-001",
                procedure_code="A0429",
                modifier_codes=["GM"],
                diagnosis_codes=["R07.9"],
                units=1,
                charge_cents=120000,
                description="ALS transport",
            )
        ],
        created_at=_timestamp(),
        updated_at=_timestamp(),
        submitted_at=_timestamp(),
    )


def _build_claim_created_event() -> ClaimCreatedEvent:
    """Create a representative billing claim created event."""

    return ClaimCreatedEvent(
        claim_id="claim-001",
        tenant_id="tenant-001",
        patient_id="patient-001",
        created_at=_timestamp(),
    )


def _build_workflow_execution() -> WorkflowExecution:
    """Create a representative workflow execution contract."""

    return WorkflowExecution(
        workflow_id="wf-001",
        workflow_type="claim_submission",
        context=WorkflowContext(
            workflow_id="wf-001",
            tenant_id="tenant-001",
            correlation_id="corr-001",
            initiator_user_id="user-001",
        ),
        status=WorkflowStatus.RUNNING,
        started_at=_timestamp(),
    )


@pytest.mark.parametrize(
    ("factory", "expected_type"),
    [
        (_build_domain_event, DomainEvent),
        (_build_user_auth_context, UserAuthContext),
        (_build_audit_record, AuditRecord),
        (_build_claim_contract, ClaimContract),
        (_build_claim_created_event, ClaimCreatedEvent),
        (_build_workflow_execution, WorkflowExecution),
    ],
)
def test_representative_contracts_round_trip(factory, expected_type) -> None:
    """Ensure representative contracts serialize and deserialize without drift."""

    contract = factory()
    restored = expected_type.model_validate_json(contract.model_dump_json())
    assert restored == contract


def test_claim_line_item_rejects_non_positive_units() -> None:
    """Protect billing consumers from invalid service-line unit counts."""

    with pytest.raises(ValidationError):
        ClaimLineItem(
            line_id="line-001",
            procedure_code="A0429",
            units=0,
            charge_cents=100,
        )


def test_claim_contract_rejects_negative_balances() -> None:
    """Reject financially impossible negative balances at the contract boundary."""

    with pytest.raises(ValidationError):
        ClaimContract(
            claim_id="claim-001",
            tenant_id="tenant-001",
            patient_id="patient-001",
            status=ClaimStatus.DRAFT,
            total_charge_cents=100,
            balance_cents=-1,
            created_at=_timestamp(),
            updated_at=_timestamp(),
        )


def test_claim_created_event_accepts_supported_clearinghouse_enum_values() -> None:
    """Keep enum serialization stable for downstream event consumers."""

    assert ClearinghouseProvider.OFFICE_ALLY.value == "office_ally"