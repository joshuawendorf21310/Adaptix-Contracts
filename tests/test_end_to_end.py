"""
Tests for end-to-end extraction flow.

Validates the complete contract authority pipeline:
  1. Define a typed DomainEvent
  2. Register it in EventCatalog
  3. Look it up in the ContractRegistry
  4. Wrap it in an EventEnvelope
  5. Serialize to bus dict (JSON-safe)
  6. Deserialize from bus dict
  7. Validate compatibility
  8. Validate against the catalog schema

This is the "golden path" that every downstream consumer follows.
"""

from __future__ import annotations

import json
import uuid

import pytest

from adaptix_contracts.compat import (
    DownstreamDeclaration,
    assert_compatible,
    is_version_compatible,
    validate_matrix,
)
from adaptix_contracts.envelope import EventEnvelope
from adaptix_contracts.events import EventCatalog, import_all_events
from adaptix_contracts.registry import CONTRACT_REGISTRY, all_event_types, lookup_required
from adaptix_contracts.types.enums import CadUnitStatus
from adaptix_contracts.version import CONTRACT_VERSION


TENANT = uuid.UUID("12345678-1234-5678-1234-567812345678")
ACTOR = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
ENTITY = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


def _minimal_kwargs_for(schema, event_type: str) -> dict:
    """Build minimal construction kwargs for any DomainEvent subclass.

    Supplies the DomainEvent base fields plus sensible defaults for any
    additional required fields discovered via model introspection.
    """
    kwargs: dict = {
        "event_type": event_type,
        "tenant_id": TENANT,
        "entity_type": event_type.split(".")[0],
        "entity_id": ENTITY,
    }
    base_fields = {"event_id", "event_type", "tenant_id", "actor_id", "entity_type",
                   "entity_id", "payload", "timestamp", "correlation_id", "version"}
    for name, field_info in schema.model_fields.items():
        if name in base_fields or name in kwargs:
            continue
        if not field_info.is_required():
            continue
        # Supply a sensible default based on annotation
        ann = field_info.annotation
        if ann is bool:
            kwargs[name] = True
        elif ann is int:
            kwargs[name] = 0
        elif ann is float:
            kwargs[name] = 0.0
        elif ann is uuid.UUID:
            kwargs[name] = ENTITY
        else:
            kwargs[name] = ""
    return kwargs


@pytest.fixture(autouse=True)
def _ensure_catalog():
    import_all_events()


class TestEndToEndGoldenPath:
    """Full wrap → serialize → deserialize → validate flow."""

    def test_incident_created_golden_path(self):
        # 1. Look up the contract
        contract = lookup_required("incident.created")
        assert contract.source_repo == "adaptix-cad"
        assert contract.stability == "stable"

        # 2. Build the payload from a typed event
        catalog = EventCatalog()
        schema = catalog.get_schema("incident.created")
        assert schema is not None
        event = schema(
            event_type="incident.created",
            tenant_id=TENANT,
            actor_id=ACTOR,
            entity_type="incident",
            entity_id=ENTITY,
            incident_number="INC-2026-001",
            severity="critical",
            dispatch_priority=1,
            location={"address": "123 Main St"},
        )
        assert event.event_type == "incident.created"

        # 3. Wrap in envelope
        envelope = EventEnvelope.wrap(
            event_type=event.event_type,
            source_repo=contract.source_repo,
            tenant_id=event.tenant_id,
            payload=event.payload,
            actor_id=event.actor_id,
            schema_version=contract.schema_version,
        )
        assert envelope.event_type == "incident.created"
        assert envelope.source_repo == "adaptix-cad"
        assert envelope.contract_version == CONTRACT_VERSION

        # 4. Serialize to bus dict
        bus_dict = envelope.to_bus_dict()
        serialized = json.dumps(bus_dict)
        assert "incident.created" in serialized

        # 5. Deserialize
        reconstructed = EventEnvelope.from_bus_dict(json.loads(serialized))
        assert reconstructed.envelope_id == envelope.envelope_id
        assert reconstructed.event_type == envelope.event_type
        assert reconstructed.tenant_id == envelope.tenant_id

        # 6. Validate compatibility
        assert reconstructed.is_compatible_with("0.1.0", "0.2.x")

    def test_epcr_signed_triggers_billing_flow(self):
        """epcr.signed → billing.claim.created integration point."""
        # Look up contract
        epcr_contract = lookup_required("epcr.signed")
        assert "patient_id" in epcr_contract.payload_fields
        assert "signed_at" in epcr_contract.payload_fields

        # Create envelope for epcr.signed
        epcr_envelope = EventEnvelope.wrap(
            event_type="epcr.signed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-001",
                "incident_id": "inc-001",
                "patient_id": "pat-001",
                "signed_by": str(ACTOR),
                "signed_at": "2026-04-10T12:00:00Z",
            },
            actor_id=ACTOR,
        )

        # Verify billing can consume this
        billing_contract = lookup_required("billing.claim.created")
        assert billing_contract.source_repo == "adaptix-billing"

        # Billing produces its own envelope
        billing_envelope = EventEnvelope.wrap(
            event_type="billing.claim.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-001",
                "epcr_id": epcr_envelope.payload["epcr_id"],
                "patient_id": epcr_envelope.payload["patient_id"],
                "payer": "Medicare",
            },
            causation_id=epcr_envelope.envelope_id,
            correlation_id=epcr_envelope.correlation_id,
        )

        assert billing_envelope.causation_id == epcr_envelope.envelope_id
        assert billing_envelope.event_type == "billing.claim.created"


class TestEveryRegistryEventCanBeWrapped:
    """Ensure every single registry event type can be wrapped in an envelope."""

    @pytest.mark.parametrize(
        "event_type",
        all_event_types(),
        ids=lambda et: et,
    )
    def test_wrap_registry_event(self, event_type: str):
        contract = lookup_required(event_type)

        envelope = EventEnvelope.wrap(
            event_type=event_type,
            source_repo=contract.source_repo,
            tenant_id=TENANT,
            payload={field: "test" for field in contract.payload_fields},
            schema_version=contract.schema_version,
        )

        assert envelope.event_type == event_type
        assert envelope.source_repo == contract.source_repo
        assert envelope.schema_version == contract.schema_version

        # Round-trip through JSON
        raw = json.loads(json.dumps(envelope.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.event_type == event_type


class TestEveryRegistryEventHasTypedClass:
    """Ensure every registry event has a typed DomainEvent subclass in the catalog."""

    @pytest.mark.parametrize(
        "event_type",
        all_event_types(),
        ids=lambda et: et,
    )
    def test_catalog_has_schema(self, event_type: str):
        catalog = EventCatalog()
        schema = catalog.get_schema(event_type)
        assert schema is not None, (
            f"Registry event {event_type!r} has no typed event class in EventCatalog"
        )

    @pytest.mark.parametrize(
        "event_type",
        all_event_types(),
        ids=lambda et: et,
    )
    def test_typed_event_is_constructable(self, event_type: str):
        catalog = EventCatalog()
        schema = catalog.get_schema(event_type)
        assert schema is not None
        kwargs = _minimal_kwargs_for(schema, event_type)
        instance = schema(**kwargs)
        assert instance.event_type == event_type
        assert instance.tenant_id == TENANT


class TestCompatibilityEndToEnd:
    """Validate the compatibility declaration and matrix flow."""

    def test_assert_compatible_with_current_version(self):
        assert_compatible(min_version="0.1.1", max_version="0.2.x")

    def test_validate_matrix_all_compatible(self):
        result = validate_matrix()
        assert result["incompatible"] == [], (
            f"Incompatible repos: {result['incompatible']}"
        )

    def test_downstream_declaration_round_trip(self, tmp_path):
        """Test the full contracts.json → DownstreamDeclaration → assert_or_raise flow."""
        contracts_file = tmp_path / "contracts.json"
        contracts_file.write_text(json.dumps({
            "repo": "adaptix-test-e2e",
            "min_contract_version": "0.1.1",
            "max_contract_version": "0.2.x",
            "event_types": ["incident.created", "epcr.signed"],
            "notes": "End-to-end test declaration",
        }))

        dec = DownstreamDeclaration.from_json_file(str(contracts_file))
        assert dec.repo == "adaptix-test-e2e"
        assert "incident.created" in dec.event_types

        # Should not raise
        dec.assert_or_raise()

    def test_envelope_compatibility_check(self):
        envelope = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={},
        )
        # Compatible with current
        assert envelope.is_compatible_with("0.1.0", "0.2.x")
        # Not compatible with future-only
        assert not envelope.is_compatible_with("99.0.0")


class TestSubPackageImports:
    """Verify the sub-package __init__.py re-exports work correctly."""

    def test_events_package_exports(self):
        from adaptix_contracts.events import DomainEvent, EventCatalog, import_all_events

        assert DomainEvent is not None
        assert EventCatalog is not None
        assert callable(import_all_events)

    def test_types_package_exports(self):
        from adaptix_contracts.types import IncidentStatus, AlertPriority

        assert IncidentStatus is not None
        assert AlertPriority is not None

    def test_utils_package_exports(self):
        from adaptix_contracts.utils import normalize_role_claims

        assert callable(normalize_role_claims)

    def test_top_level_package_exports(self):
        from adaptix_contracts import (
            CONTRACT_VERSION,
            EventEnvelope,
            assert_compatible,
            catalog_summary,
            is_version_compatible,
            lookup,
            lookup_required,
            validate_catalog_against_registry,
        )

        assert CONTRACT_VERSION == "0.2.1"
        assert EventEnvelope is not None
        assert callable(lookup)
        assert callable(lookup_required)
        assert callable(catalog_summary)
        assert callable(assert_compatible)
        assert callable(is_version_compatible)
        assert callable(validate_catalog_against_registry)


class TestValidateCatalogAgainstRegistry:
    """Validate that the EventCatalog ↔ CONTRACT_REGISTRY bridge works."""

    def test_validate_returns_ok(self):
        from adaptix_contracts.registry import validate_catalog_against_registry

        result = validate_catalog_against_registry()
        assert result["ok"] is True
        assert result["missing"] == []

    def test_validate_counts_match(self):
        from adaptix_contracts.registry import validate_catalog_against_registry

        result = validate_catalog_against_registry()
        assert result["registry_count"] == result["catalog_count"]
        assert result["extra"] == []

    def test_every_registry_event_has_catalog_schema(self):
        """This is the authoritative assertion for the pre-1.0.0 audit item:
        'EventCatalog validates against CONTRACT_REGISTRY'."""
        from adaptix_contracts.registry import validate_catalog_against_registry

        result = validate_catalog_against_registry()
        assert result["ok"], (
            f"Missing catalog schemas for registry events: {result['missing']}"
        )


class TestNemsisExportPipelineIntegration:
    """End-to-end test for the NEMSIS auto-export pipeline.

    Simulates the full lifecycle: lock → compliance → queue → validate → submit → accept/reject.
    Each step produces an EventEnvelope that references the previous via causation_id.
    """

    def test_nemsis_pipeline_happy_path(self):
        """lock → compliance (pass) → queue → validate → submit → accept."""
        epcr_id = "epcr-nemsis-001"
        export_id = str(uuid.uuid4())

        # Step 1: Lock the ePCR
        lock_env = EventEnvelope.wrap(
            event_type="nemsis.epcr.locked",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={"epcr_id": epcr_id, "lock_reason": "qa_complete"},
        )
        assert lock_env.event_type == "nemsis.epcr.locked"

        # Step 2: Compliance check passes
        compliance_env = EventEnvelope.wrap(
            event_type="nemsis.compliance.check_completed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": epcr_id,
                "is_compliant": True,
                "blocker_count": 0,
                "readiness_state": "ready",
            },
            causation_id=lock_env.envelope_id,
        )
        assert compliance_env.payload["is_compliant"] is True

        # Step 3: Queue for export
        queue_env = EventEnvelope.wrap(
            event_type="nemsis.export.queued",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={"epcr_id": epcr_id, "export_id": export_id, "export_format": "xml"},
            causation_id=compliance_env.envelope_id,
        )

        # Step 4: Validate export
        validate_env = EventEnvelope.wrap(
            event_type="nemsis.export.validated",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "export_id": export_id,
                "validation_passed": True,
                "error_count": 0,
                "warning_count": 0,
            },
            causation_id=queue_env.envelope_id,
        )

        # Step 5: Submit to state endpoint
        submit_env = EventEnvelope.wrap(
            event_type="nemsis.export.submitted",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "export_id": export_id,
                "submission_method": "api",
                "submission_id": "STATE-RX-001",
            },
            causation_id=validate_env.envelope_id,
        )

        # Step 6: State accepts
        accept_env = EventEnvelope.wrap(
            event_type="nemsis.export.accepted",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={"export_id": export_id, "state_reference": "ST-2026-001"},
            causation_id=submit_env.envelope_id,
        )

        # Verify full chain
        assert accept_env.causation_id == submit_env.envelope_id
        assert submit_env.causation_id == validate_env.envelope_id
        assert validate_env.causation_id == queue_env.envelope_id
        assert queue_env.causation_id == compliance_env.envelope_id
        assert compliance_env.causation_id == lock_env.envelope_id

        # Verify all round-trip through JSON
        for env in [lock_env, compliance_env, queue_env, validate_env, submit_env, accept_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.envelope_id == env.envelope_id
            assert restored.event_type == env.event_type

    def test_nemsis_pipeline_rejection_path(self):
        """lock → compliance (pass) → queue → validate → submit → reject."""
        export_id = str(uuid.uuid4())

        submit_env = EventEnvelope.wrap(
            event_type="nemsis.export.submitted",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "export_id": export_id,
                "submission_method": "api",
                "submission_id": "STATE-RX-002",
            },
        )

        reject_env = EventEnvelope.wrap(
            event_type="nemsis.export.rejected",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "export_id": export_id,
                "rejection_count": 2,
                "rejection_codes": ["ERR-001", "ERR-002"],
            },
            causation_id=submit_env.envelope_id,
        )

        assert reject_env.causation_id == submit_env.envelope_id
        assert reject_env.payload["rejection_count"] == 2
        assert len(reject_env.payload["rejection_codes"]) == 2

    def test_nemsis_compliance_failure_blocks_export(self):
        """Compliance failure means the pipeline stops — no queue event follows."""
        compliance_env = EventEnvelope.wrap(
            event_type="nemsis.compliance.check_completed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-fail-001",
                "is_compliant": False,
                "blocker_count": 3,
                "readiness_state": "blocked",
            },
        )
        assert compliance_env.payload["is_compliant"] is False
        assert compliance_env.payload["blocker_count"] == 3

    def test_all_nemsis_events_in_registry(self):
        """All NEMSIS pipeline events must be in the contract registry."""
        nemsis_types = [
            "nemsis.epcr.locked",
            "nemsis.compliance.check_completed",
            "nemsis.export.queued",
            "nemsis.export.validated",
            "nemsis.export.submitted",
            "nemsis.export.accepted",
            "nemsis.export.rejected",
        ]
        for event_type in nemsis_types:
            contract = lookup_required(event_type)
            assert contract.source_repo == "adaptix-epcr"
            assert contract.stability == "stable"


class TestCrossDomainIntegrationFlows:
    """Test cross-domain event flows that span multiple services."""

    def test_epcr_signed_to_billing_to_ai(self):
        """epcr.signed → billing.claim.created → AI augmentation (billing.claim.denied review)."""
        # 1. ePCR is signed
        epcr_envelope = EventEnvelope.wrap(
            event_type="epcr.signed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            actor_id=ACTOR,
            payload={
                "epcr_id": "epcr-xd-001",
                "incident_id": "inc-xd-001",
                "patient_id": "pat-xd-001",
                "signed_by": str(ACTOR),
                "signed_at": "2026-04-11T12:00:00Z",
            },
            correlation_id="corr-flow-001",
        )

        # 2. Billing creates a claim (triggered by epcr.signed)
        claim_envelope = EventEnvelope.wrap(
            event_type="billing.claim.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-xd-001",
                "epcr_id": epcr_envelope.payload["epcr_id"],
                "patient_id": epcr_envelope.payload["patient_id"],
                "payer": "Medicare",
            },
            causation_id=epcr_envelope.envelope_id,
            correlation_id=epcr_envelope.correlation_id,
        )

        # 3. Claim gets denied
        denied_envelope = EventEnvelope.wrap(
            event_type="billing.claim.denied",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-xd-001",
                "denial_code": "CO-4",
                "denial_reason": "The procedure code is inconsistent with the modifier used",
            },
            causation_id=claim_envelope.envelope_id,
            correlation_id=epcr_envelope.correlation_id,
        )

        # 4. AI picks up the denied claim for review
        # Verify the AI repo subscribes to billing.claim.denied
        from adaptix_contracts.compat import get_declaration

        ai_dec = get_declaration("adaptix-ai")
        assert ai_dec is not None
        assert "billing.claim.denied" in ai_dec.event_types

        # Verify correlation chain is preserved
        assert claim_envelope.correlation_id == epcr_envelope.correlation_id
        assert denied_envelope.correlation_id == epcr_envelope.correlation_id

        # Verify causation chain
        assert claim_envelope.causation_id == epcr_envelope.envelope_id
        assert denied_envelope.causation_id == claim_envelope.envelope_id

    def test_incident_dispatch_to_crewlink_to_mdt(self):
        """incident.created → crewlink.alert.created → crewlink.assignment.accepted → mdt.status_changed."""
        # 1. Incident is created (CAD dispatch)
        incident_env = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "incident_id": "inc-dispatch-001",
                "incident_number": "INC-2026-001",
                "priority": "charlie",
                "location": "123 Main St",
                "call_type": "medical",
            },
            correlation_id="corr-dispatch-001",
        )

        # 2. CrewLink sends an alert
        alert_env = EventEnvelope.wrap(
            event_type="crewlink.alert.created",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-001",
                "page_type": "dispatch",
                "priority": "high",
                "recipients": ["device-token-001", "device-token-002"],
            },
            causation_id=incident_env.envelope_id,
            correlation_id=incident_env.correlation_id,
        )

        # 3. Crew accepts assignment
        accept_env = EventEnvelope.wrap(
            event_type="crewlink.assignment.accepted",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "assignment_id": "assign-001",
                "incident_id": "inc-dispatch-001",
                "user_id": str(ACTOR),
                "unit_id": "unit-m1",
            },
            causation_id=alert_env.envelope_id,
            correlation_id=incident_env.correlation_id,
        )

        # 4. MDT status changes to en_route
        mdt_env = EventEnvelope.wrap(
            event_type="mdt.status_changed",
            source_repo="adaptix-field",
            tenant_id=TENANT,
            payload={
                "unit_id": "unit-m1",
                "status_code": "en_route",
                "latitude": 37.7749,
                "longitude": -122.4194,
            },
            causation_id=accept_env.envelope_id,
            correlation_id=incident_env.correlation_id,
        )

        # Verify full correlation chain preserved
        for env in [alert_env, accept_env, mdt_env]:
            assert env.correlation_id == "corr-dispatch-001"

        # Verify causation chain
        assert alert_env.causation_id == incident_env.envelope_id
        assert accept_env.causation_id == alert_env.envelope_id
        assert mdt_env.causation_id == accept_env.envelope_id

        # Verify architecture: CrewLink recipients are device tokens, not phone numbers
        for recipient in alert_env.payload["recipients"]:
            assert "phone" not in recipient.lower()

    def test_fire_isolation_policy_in_practice(self):
        """Fire events flow independently — no CAD/MDT/CrewLink coupling."""
        fire_env = EventEnvelope.wrap(
            event_type="fire.incident.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-001",
                "incident_type": "structure_fire",
                "address": "456 Oak Ave",
            },
        )

        # Verify fire events are isolated
        from adaptix_contracts.compat import get_declaration

        fire_dec = get_declaration("adaptix-fire")
        assert fire_dec is not None

        # Fire should NOT consume MDT, CAD, or CrewLink events
        for forbidden_prefix in ("mdt.", "cad.", "crewlink."):
            for et in fire_dec.event_types:
                assert not et.startswith(forbidden_prefix), (
                    f"Fire isolation violation: {et!r}"
                )

        # But fire events flow to Command for operational awareness
        cmd_dec = get_declaration("adaptix-command")
        assert cmd_dec is not None
        assert "fire.incident.status_changed" in cmd_dec.event_types


class TestBillingDenialAndRecoveryFlows:
    """End-to-end flows for billing denial, payment failure, and dispute paths."""

    def test_billing_claim_denial_to_dispute(self):
        """billing.claim.denied → patient.financial.dispute.created flow."""
        # 1. Claim is denied
        denied_env = EventEnvelope.wrap(
            event_type="billing.claim.denied",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-deny-001",
                "denial_code": "CO-4",
                "denial_reason": "Procedure code inconsistent with modifier",
            },
            correlation_id="corr-denial-001",
        )
        assert denied_env.event_type == "billing.claim.denied"

        # 2. Patient opens a financial dispute
        dispute_env = EventEnvelope.wrap(
            event_type="patient.financial.dispute.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "dispute_id": "disp-001",
                "account_id": "acct-001",
                "amount_disputed": 2500,
            },
            causation_id=denied_env.envelope_id,
            correlation_id=denied_env.correlation_id,
        )

        assert dispute_env.causation_id == denied_env.envelope_id
        assert dispute_env.correlation_id == denied_env.correlation_id

        # AI consumes both events
        from adaptix_contracts.compat import get_declaration

        ai_dec = get_declaration("adaptix-ai")
        assert ai_dec is not None
        assert "billing.claim.denied" in ai_dec.event_types
        assert "patient.financial.dispute.created" in ai_dec.event_types

    def test_payment_posted_and_failed_lifecycle(self):
        """payment.posted and payment.failed as alternative outcomes."""
        # 1. Claim is paid
        paid_env = EventEnvelope.wrap(
            event_type="billing.claim.paid",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-pay-001",
                "amount_paid": 1500,
                "paid_at": "2026-04-11T15:00:00Z",
            },
            correlation_id="corr-pay-001",
        )

        # 2. Payment is posted
        posted_env = EventEnvelope.wrap(
            event_type="payment.posted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-001",
                "account_id": "acct-001",
                "amount": 1500,
            },
            causation_id=paid_env.envelope_id,
            correlation_id=paid_env.correlation_id,
        )
        assert posted_env.causation_id == paid_env.envelope_id

        # Alternative: payment fails
        failed_env = EventEnvelope.wrap(
            event_type="payment.failed",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-002",
                "account_id": "acct-001",
                "error_code": "insufficient_funds",
            },
            correlation_id="corr-pay-002",
        )
        assert failed_env.event_type == "payment.failed"

        # Round-trip both through JSON
        for env in [posted_env, failed_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.event_type == env.event_type

    def test_payment_refund_flow(self):
        """payment.posted → payment.refunded chain."""
        posted_env = EventEnvelope.wrap(
            event_type="payment.posted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-refund-001",
                "account_id": "acct-refund-001",
                "amount": 3000,
            },
            correlation_id="corr-refund-001",
        )

        refund_env = EventEnvelope.wrap(
            event_type="payment.refunded",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-refund-001",
                "account_id": "acct-refund-001",
                "refund_amount": 3000,
            },
            causation_id=posted_env.envelope_id,
            correlation_id=posted_env.correlation_id,
        )

        assert refund_env.causation_id == posted_env.envelope_id
        assert refund_env.payload["refund_amount"] == 3000

    def test_full_billing_lifecycle_claim_to_payment(self):
        """epcr.signed → billing.claim.created → submitted → paid → payment.posted."""
        correlation = "corr-full-billing-001"

        # 1. ePCR signed
        epcr_env = EventEnvelope.wrap(
            event_type="epcr.signed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-bl-001",
                "incident_id": "inc-bl-001",
                "patient_id": "pat-bl-001",
                "signed_by": str(ACTOR),
                "signed_at": "2026-04-10T08:00:00Z",
            },
            correlation_id=correlation,
        )

        # 2. Claim created
        claim_env = EventEnvelope.wrap(
            event_type="billing.claim.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-bl-001",
                "epcr_id": "epcr-bl-001",
                "patient_id": "pat-bl-001",
                "payer": "Medicare",
            },
            causation_id=epcr_env.envelope_id,
            correlation_id=correlation,
        )

        # 3. Claim submitted
        submitted_env = EventEnvelope.wrap(
            event_type="billing.claim.submitted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-bl-001",
                "payer": "Medicare",
                "submitted_at": "2026-04-10T09:00:00Z",
            },
            causation_id=claim_env.envelope_id,
            correlation_id=correlation,
        )

        # 4. Claim paid
        paid_env = EventEnvelope.wrap(
            event_type="billing.claim.paid",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-bl-001",
                "amount_paid": 4200,
                "paid_at": "2026-04-12T10:00:00Z",
            },
            causation_id=submitted_env.envelope_id,
            correlation_id=correlation,
        )

        # 5. Payment posted
        payment_env = EventEnvelope.wrap(
            event_type="payment.posted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-bl-001",
                "account_id": "acct-bl-001",
                "amount": 4200,
            },
            causation_id=paid_env.envelope_id,
            correlation_id=correlation,
        )

        # Verify full causal chain
        assert claim_env.causation_id == epcr_env.envelope_id
        assert submitted_env.causation_id == claim_env.envelope_id
        assert paid_env.causation_id == submitted_env.envelope_id
        assert payment_env.causation_id == paid_env.envelope_id

        # Correlation preserved throughout
        for env in [epcr_env, claim_env, submitted_env, paid_env, payment_env]:
            assert env.correlation_id == correlation


class TestCrewLinkAlertLifecycle:
    """End-to-end flows for CrewLink alert expiration and escalation."""

    def test_alert_expiration_flow(self):
        """crewlink.alert.created → crewlink.alert.expired (no ack)."""
        alert_env = EventEnvelope.wrap(
            event_type="crewlink.alert.created",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-exp-001",
                "page_type": "dispatch",
                "priority": "high",
                "recipients": ["device-token-001"],
            },
            correlation_id="corr-exp-001",
        )

        # Alert expires (no acknowledgment received)
        expired_env = EventEnvelope.wrap(
            event_type="crewlink.alert.expired",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={"alert_id": "alert-exp-001"},
            causation_id=alert_env.envelope_id,
            correlation_id=alert_env.correlation_id,
        )

        assert expired_env.causation_id == alert_env.envelope_id
        assert expired_env.payload["alert_id"] == alert_env.payload["alert_id"]

    def test_alert_acknowledged_then_assignment_declined(self):
        """crewlink.alert.created → acknowledged → assignment.declined."""
        alert_env = EventEnvelope.wrap(
            event_type="crewlink.alert.created",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-dec-001",
                "page_type": "dispatch",
                "priority": "high",
                "recipients": ["device-token-002"],
            },
            correlation_id="corr-dec-001",
        )

        ack_env = EventEnvelope.wrap(
            event_type="crewlink.alert.acknowledged",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-dec-001",
                "user_id": str(ACTOR),
                "device_id": "device-token-002",
                "acknowledged_at": "2026-04-11T12:30:00Z",
            },
            causation_id=alert_env.envelope_id,
            correlation_id=alert_env.correlation_id,
        )

        declined_env = EventEnvelope.wrap(
            event_type="crewlink.assignment.declined",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "assignment_id": "assign-dec-001",
                "user_id": str(ACTOR),
                "reason": "off_duty",
            },
            causation_id=ack_env.envelope_id,
            correlation_id=alert_env.correlation_id,
        )

        assert ack_env.causation_id == alert_env.envelope_id
        assert declined_env.causation_id == ack_env.envelope_id

        # All share the same correlation
        for env in [alert_env, ack_env, declined_env]:
            assert env.correlation_id == "corr-dec-001"


class TestWorkforceSchedulingFlows:
    """End-to-end flows for workforce scheduling lifecycle."""

    def test_shift_created_filled_missed(self):
        """scheduling.shift.created → filled → missed lifecycle."""
        correlation = "corr-shift-001"

        # 1. Shift created
        created_env = EventEnvelope.wrap(
            event_type="scheduling.shift.created",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "shift_id": "shift-001",
                "unit_id": "unit-m1",
                "start_time": "2026-04-12T06:00:00Z",
                "end_time": "2026-04-12T18:00:00Z",
            },
            correlation_id=correlation,
        )

        # 2. Shift filled
        filled_env = EventEnvelope.wrap(
            event_type="scheduling.shift.filled",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "shift_id": "shift-001",
                "user_id": str(ACTOR),
            },
            causation_id=created_env.envelope_id,
            correlation_id=correlation,
        )

        assert filled_env.causation_id == created_env.envelope_id

        # 3. Another shift is missed (no fill)
        missed_env = EventEnvelope.wrap(
            event_type="scheduling.shift.missed",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={"shift_id": "shift-002"},
            correlation_id="corr-shift-002",
        )

        assert missed_env.event_type == "scheduling.shift.missed"

    def test_personnel_create_to_deactivate(self):
        """personnel.created → personnel.deactivated lifecycle."""
        created_env = EventEnvelope.wrap(
            event_type="personnel.created",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "first_name": "Jane",
                "last_name": "Doe",
                "role": "paramedic",
            },
            correlation_id="corr-personnel-001",
        )

        deactivated_env = EventEnvelope.wrap(
            event_type="personnel.deactivated",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "reason": "voluntary_resignation",
            },
            causation_id=created_env.envelope_id,
            correlation_id=created_env.correlation_id,
        )

        assert deactivated_env.causation_id == created_env.envelope_id

    def test_training_completed_round_trip(self):
        """training.completed event with full serialize/deserialize."""
        env = EventEnvelope.wrap(
            event_type="training.completed",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "training_id": "trn-001",
                "user_id": str(ACTOR),
                "course_name": "ACLS Recertification",
                "completed_at": "2026-04-10T16:00:00Z",
            },
        )

        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.event_type == "training.completed"
        assert restored.payload["course_name"] == "ACLS Recertification"


class TestMultiTenantIsolation:
    """Verify envelope tenant isolation semantics."""

    TENANT_A = uuid.UUID("aaaa1111-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
    TENANT_B = uuid.UUID("bbbb2222-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

    def test_envelopes_carry_distinct_tenant_ids(self):
        """Two envelopes for the same event type on different tenants stay separate."""
        env_a = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=self.TENANT_A,
            payload={"incident_id": "inc-a-001", "incident_number": "A-001",
                      "priority": "alpha", "location": "1 A St", "call_type": "medical"},
        )
        env_b = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=self.TENANT_B,
            payload={"incident_id": "inc-b-001", "incident_number": "B-001",
                      "priority": "bravo", "location": "2 B St", "call_type": "trauma"},
        )

        assert env_a.tenant_id != env_b.tenant_id
        assert env_a.envelope_id != env_b.envelope_id

        # Round-trip preserves tenant isolation
        restored_a = EventEnvelope.from_bus_dict(json.loads(json.dumps(env_a.to_bus_dict())))
        restored_b = EventEnvelope.from_bus_dict(json.loads(json.dumps(env_b.to_bus_dict())))
        assert restored_a.tenant_id == self.TENANT_A
        assert restored_b.tenant_id == self.TENANT_B

    @pytest.mark.parametrize("event_type", all_event_types(), ids=lambda et: et)
    def test_every_event_preserves_tenant_through_roundtrip(self, event_type: str):
        """Parametrized: every event type preserves tenant_id through JSON round-trip."""
        contract = lookup_required(event_type)
        env = EventEnvelope.wrap(
            event_type=event_type,
            source_repo=contract.source_repo,
            tenant_id=self.TENANT_A,
            payload={field: "test" for field in contract.payload_fields},
        )

        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.tenant_id == self.TENANT_A


class TestCoreAuthWebhookFlows:
    """End-to-end flows for core auth, audit, and webhook lifecycle."""

    def test_tenant_created_to_user_lifecycle(self):
        """tenant.created → user.created → user.deactivated."""
        correlation = "corr-tenant-001"

        tenant_env = EventEnvelope.wrap(
            event_type="tenant.created",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "tenant_id": str(TENANT),
                "name": "Acme EMS",
                "service_lines": ["ems", "fire"],
            },
            correlation_id=correlation,
        )

        user_env = EventEnvelope.wrap(
            event_type="user.created",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "tenant_id": str(TENANT),
                "email": "admin@acme-ems.com",
                "roles": ["admin", "dispatcher"],
            },
            causation_id=tenant_env.envelope_id,
            correlation_id=correlation,
        )

        deactivated_env = EventEnvelope.wrap(
            event_type="user.deactivated",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "tenant_id": str(TENANT),
            },
            causation_id=user_env.envelope_id,
            correlation_id=correlation,
        )

        assert user_env.causation_id == tenant_env.envelope_id
        assert deactivated_env.causation_id == user_env.envelope_id

    def test_webhook_delivered_and_failed_paths(self):
        """webhook.delivered vs webhook.failed as alternative outcomes."""
        delivered_env = EventEnvelope.wrap(
            event_type="webhook.delivered",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "webhook_id": "wh-001",
                "endpoint_url": "https://example.com/hook",
                "http_status": 200,
            },
        )
        assert delivered_env.payload["http_status"] == 200

        failed_env = EventEnvelope.wrap(
            event_type="webhook.failed",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "webhook_id": "wh-002",
                "endpoint_url": "https://example.com/hook",
                "error": "connection_timeout",
                "attempt": 3,
            },
        )
        assert failed_env.payload["attempt"] == 3

        # Both round-trip
        for env in [delivered_env, failed_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.event_type == env.event_type

    def test_audit_entry_created_round_trip(self):
        """audit.entry.created envelope round-trip."""
        env = EventEnvelope.wrap(
            event_type="audit.entry.created",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            actor_id=ACTOR,
            payload={
                "entry_id": "aud-001",
                "action": "user.create",
                "resource_type": "user",
                "resource_id": str(ACTOR),
                "actor_id": str(ACTOR),
            },
        )

        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.actor_id == ACTOR
        assert restored.payload["action"] == "user.create"

    def test_feature_flag_toggled(self):
        """feature_flag.toggled event."""
        env = EventEnvelope.wrap(
            event_type="feature_flag.toggled",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "flag_name": "new_billing_ui",
                "enabled": True,
                "tenant_id": str(TENANT),
            },
        )
        assert env.payload["enabled"] is True


class TestFireNerisSubmissionPipeline:
    """End-to-end fire incident → NERIS submission pipeline."""

    def test_fire_incident_to_neris_submission(self):
        """fire.incident.created → status_changed → closed → neris.submission.created → ack/reject."""
        correlation = "corr-fire-001"

        # 1. Fire incident created
        created_env = EventEnvelope.wrap(
            event_type="fire.incident.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-neris-001",
                "incident_type": "structure_fire",
                "address": "789 Elm St",
            },
            correlation_id=correlation,
        )

        # 2. Status change
        status_env = EventEnvelope.wrap(
            event_type="fire.incident.status_changed",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-neris-001",
                "previous_status": "dispatched",
                "new_status": "on_scene",
            },
            causation_id=created_env.envelope_id,
            correlation_id=correlation,
        )

        # 3. Incident closed
        closed_env = EventEnvelope.wrap(
            event_type="fire.incident.closed",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-neris-001",
                "disposition": "extinguished",
            },
            causation_id=status_env.envelope_id,
            correlation_id=correlation,
        )

        # 4. NERIS submission
        submission_env = EventEnvelope.wrap(
            event_type="neris.submission.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-sub-001",
                "fire_incident_id": "fire-neris-001",
                "state_code": "TX",
            },
            causation_id=closed_env.envelope_id,
            correlation_id=correlation,
        )

        # 5a. Acknowledged
        ack_env = EventEnvelope.wrap(
            event_type="neris.submission.acknowledged",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-sub-001",
                "acknowledged_at": "2026-04-12T10:00:00Z",
            },
            causation_id=submission_env.envelope_id,
            correlation_id=correlation,
        )

        # Verify chain
        assert status_env.causation_id == created_env.envelope_id
        assert closed_env.causation_id == status_env.envelope_id
        assert submission_env.causation_id == closed_env.envelope_id
        assert ack_env.causation_id == submission_env.envelope_id

    def test_neris_submission_rejection(self):
        """neris.submission.created → neris.submission.rejected."""
        submission_env = EventEnvelope.wrap(
            event_type="neris.submission.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-rej-001",
                "fire_incident_id": "fire-rej-001",
                "state_code": "CA",
            },
        )

        rejected_env = EventEnvelope.wrap(
            event_type="neris.submission.rejected",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-rej-001",
                "rejection_reason": "Missing incident type field",
            },
            causation_id=submission_env.envelope_id,
        )

        assert rejected_env.causation_id == submission_env.envelope_id


class TestNewSchemaImports:
    """Verify the four new schema modules import and validate correctly."""

    def test_personnel_schema(self):
        from adaptix_contracts.schemas.personnel import (
            PersonnelCreateRequest,
            PersonnelDeactivateRequest,
            PersonnelListResponse,
            PersonnelResponse,
        )

        req = PersonnelCreateRequest(
            first_name="Jane", last_name="Doe", role="paramedic"
        )
        assert req.first_name == "Jane"
        assert req.role == "paramedic"

        deact = PersonnelDeactivateRequest(reason="voluntary_resignation")
        assert deact.reason == "voluntary_resignation"

    def test_webhook_schema(self):
        from adaptix_contracts.schemas.webhook import (
            WebhookCreateRequest,
            WebhookDeliveryResponse,
            WebhookResponse,
        )

        req = WebhookCreateRequest(
            endpoint_url="https://example.com/hook",
            event_types=["incident.created", "epcr.signed"],
        )
        assert len(req.event_types) == 2

    def test_training_schema(self):
        from adaptix_contracts.schemas.training import (
            TrainingCompletionCreateRequest,
            TrainingCourseCreateRequest,
            TrainingComplianceSummary,
        )

        req = TrainingCourseCreateRequest(
            course_name="ACLS Recertification",
            training_type="certification",
        )
        assert req.course_name == "ACLS Recertification"

    def test_unit_schema(self):
        from adaptix_contracts.schemas.unit import (
            UnitCreateRequest,
            UnitResponse,
            UnitStatusChangeRequest,
        )

        req = UnitCreateRequest(unit_identifier="M-1", unit_type="ambulance")
        assert req.unit_identifier == "M-1"

        status_req = UnitStatusChangeRequest(new_status="assigned")
        assert status_req.new_status == CadUnitStatus.ASSIGNED
