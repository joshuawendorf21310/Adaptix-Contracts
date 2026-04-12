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

        assert CONTRACT_VERSION == "0.2.0"
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


class TestAuthTenancyLifecycle:
    """End-to-end test for auth/tenancy lifecycle events.

    Simulates: tenant.created → user.created → user.deactivated → tenant.suspended.
    Core owns all auth/tenancy events.
    """

    def test_tenant_user_lifecycle(self):
        """Full tenant provisioning → user lifecycle → tenant suspension."""
        # 1. Tenant is created
        tenant_env = EventEnvelope.wrap(
            event_type="tenant.created",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "tenant_id": str(TENANT),
                "name": "Acme EMS",
                "service_lines": ["ems", "fire"],
            },
            correlation_id="corr-tenant-001",
        )
        assert tenant_env.event_type == "tenant.created"

        # 2. User is created under the tenant
        user_env = EventEnvelope.wrap(
            event_type="user.created",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "tenant_id": str(TENANT),
                "email": "medic@acme-ems.com",
                "roles": ["paramedic", "field_user"],
            },
            causation_id=tenant_env.envelope_id,
            correlation_id=tenant_env.correlation_id,
        )
        assert user_env.causation_id == tenant_env.envelope_id

        # 3. User is deactivated
        deactivate_env = EventEnvelope.wrap(
            event_type="user.deactivated",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "tenant_id": str(TENANT),
                "reason": "termination",
            },
            actor_id=ACTOR,
            causation_id=user_env.envelope_id,
            correlation_id=tenant_env.correlation_id,
        )
        assert deactivate_env.payload["reason"] == "termination"

        # 4. Tenant is suspended
        suspend_env = EventEnvelope.wrap(
            event_type="tenant.suspended",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "tenant_id": str(TENANT),
                "reason": "non_payment",
            },
            correlation_id=tenant_env.correlation_id,
        )
        assert suspend_env.payload["reason"] == "non_payment"

        # Verify correlation chain
        for env in [user_env, deactivate_env, suspend_env]:
            assert env.correlation_id == tenant_env.correlation_id

        # Verify all round-trip through JSON
        for env in [tenant_env, user_env, deactivate_env, suspend_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.envelope_id == env.envelope_id
            assert restored.event_type == env.event_type

    def test_core_owns_all_auth_events(self):
        """All auth/tenancy events must be owned by adaptix-core."""
        auth_types = [
            "tenant.created", "tenant.suspended",
            "user.created", "user.deactivated",
            "feature_flag.toggled",
            "audit.entry.created",
        ]
        for event_type in auth_types:
            contract = lookup_required(event_type)
            assert contract.source_repo == "adaptix-core", (
                f"{event_type!r} should be owned by adaptix-core, got {contract.source_repo!r}"
            )


class TestBillingPaymentLifecycle:
    """End-to-end test for the billing claim and payment lifecycle.

    Simulates: epcr.signed → billing.claim.created → submitted → paid,
    and the denial → refund path.
    """

    def test_claim_happy_path(self):
        """epcr.signed → claim.created → claim.submitted → claim.paid → payment.posted."""
        # 1. ePCR triggers claim creation
        claim_env = EventEnvelope.wrap(
            event_type="billing.claim.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-pay-001",
                "epcr_id": "epcr-pay-001",
                "patient_id": "pat-pay-001",
                "payer": "BlueCross",
            },
            correlation_id="corr-billing-001",
        )

        # 2. Claim is submitted
        submit_env = EventEnvelope.wrap(
            event_type="billing.claim.submitted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-pay-001",
                "payer": "BlueCross",
                "submitted_at": "2026-04-11T14:00:00Z",
            },
            causation_id=claim_env.envelope_id,
            correlation_id=claim_env.correlation_id,
        )

        # 3. Claim is paid
        paid_env = EventEnvelope.wrap(
            event_type="billing.claim.paid",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-pay-001",
                "amount_cents": 125000,
                "paid_at": "2026-04-15T09:00:00Z",
            },
            causation_id=submit_env.envelope_id,
            correlation_id=claim_env.correlation_id,
        )

        # 4. Payment is posted
        payment_env = EventEnvelope.wrap(
            event_type="payment.posted",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-001",
                "claim_id": "clm-pay-001",
                "amount_cents": 125000,
            },
            causation_id=paid_env.envelope_id,
            correlation_id=claim_env.correlation_id,
        )

        # Verify causation chain
        assert submit_env.causation_id == claim_env.envelope_id
        assert paid_env.causation_id == submit_env.envelope_id
        assert payment_env.causation_id == paid_env.envelope_id

        # Verify all share correlation
        for env in [submit_env, paid_env, payment_env]:
            assert env.correlation_id == claim_env.correlation_id

    def test_claim_denial_and_refund_path(self):
        """claim.created → submitted → denied → payment.refunded."""
        claim_env = EventEnvelope.wrap(
            event_type="billing.claim.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-deny-001",
                "epcr_id": "epcr-deny-001",
                "patient_id": "pat-deny-001",
                "payer": "Aetna",
            },
            correlation_id="corr-billing-deny",
        )

        denied_env = EventEnvelope.wrap(
            event_type="billing.claim.denied",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "claim_id": "clm-deny-001",
                "denial_code": "CO-16",
                "denial_reason": "Claim lacks information",
            },
            causation_id=claim_env.envelope_id,
            correlation_id=claim_env.correlation_id,
        )

        # A prior payment gets refunded
        refund_env = EventEnvelope.wrap(
            event_type="payment.refunded",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-refund-001",
                "claim_id": "clm-deny-001",
                "refund_amount_cents": 50000,
            },
            causation_id=denied_env.envelope_id,
            correlation_id=claim_env.correlation_id,
        )

        assert denied_env.causation_id == claim_env.envelope_id
        assert refund_env.causation_id == denied_env.envelope_id
        assert refund_env.correlation_id == claim_env.correlation_id

    def test_payment_failure(self):
        """payment.posted failure emits payment.failed."""
        failed_env = EventEnvelope.wrap(
            event_type="payment.failed",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "payment_id": "pay-fail-001",
                "claim_id": "clm-fail-001",
                "error_code": "INSUFFICIENT_FUNDS",
            },
        )
        assert failed_env.event_type == "payment.failed"
        raw = json.loads(json.dumps(failed_env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["error_code"] == "INSUFFICIENT_FUNDS"


class TestWebhookDeliveryLifecycle:
    """End-to-end test for webhook delivery and failure events."""

    def test_webhook_delivered(self):
        """webhook.delivered event round-trips correctly."""
        env = EventEnvelope.wrap(
            event_type="webhook.delivered",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "webhook_id": "wh-001",
                "endpoint": "https://partner.example.com/hook",
                "status_code": 200,
                "response_ms": 142,
            },
        )
        assert env.event_type == "webhook.delivered"
        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["status_code"] == 200

    def test_webhook_failed(self):
        """webhook.failed captures failure details."""
        env = EventEnvelope.wrap(
            event_type="webhook.failed",
            source_repo="adaptix-core",
            tenant_id=TENANT,
            payload={
                "webhook_id": "wh-002",
                "endpoint": "https://partner.example.com/hook",
                "status_code": 500,
                "error": "Internal Server Error",
                "retry_count": 3,
            },
        )
        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["retry_count"] == 3
        assert restored.payload["status_code"] == 500

    def test_webhook_events_owned_by_core(self):
        """Core owns all webhook events."""
        for event_type in ("webhook.delivered", "webhook.failed"):
            contract = lookup_required(event_type)
            assert contract.source_repo == "adaptix-core"


class TestWorkforceSchedulingLifecycle:
    """End-to-end test for workforce scheduling and personnel lifecycle.

    Simulates: scheduling.shift.created → shift.filled → personnel events → training.
    """

    def test_shift_lifecycle(self):
        """shift.created → shift.filled → shift.missed chain."""
        shift_env = EventEnvelope.wrap(
            event_type="scheduling.shift.created",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "shift_id": "shift-001",
                "start_time": "2026-04-12T06:00:00Z",
                "end_time": "2026-04-12T18:00:00Z",
                "unit_id": "unit-m2",
            },
            correlation_id="corr-shift-001",
        )

        filled_env = EventEnvelope.wrap(
            event_type="scheduling.shift.filled",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "shift_id": "shift-001",
                "assigned_user_id": str(ACTOR),
                "filled_at": "2026-04-11T20:00:00Z",
            },
            causation_id=shift_env.envelope_id,
            correlation_id=shift_env.correlation_id,
        )

        assert filled_env.causation_id == shift_env.envelope_id
        assert filled_env.correlation_id == shift_env.correlation_id

        # Verify JSON round-trip
        for env in [shift_env, filled_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.event_type == env.event_type

    def test_shift_missed(self):
        """A shift that isn't filled produces scheduling.shift.missed."""
        missed_env = EventEnvelope.wrap(
            event_type="scheduling.shift.missed",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "shift_id": "shift-miss-001",
                "reason": "no_available_personnel",
            },
        )
        raw = json.loads(json.dumps(missed_env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["reason"] == "no_available_personnel"

    def test_personnel_lifecycle(self):
        """personnel.created → training.completed → personnel.deactivated."""
        create_env = EventEnvelope.wrap(
            event_type="personnel.created",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "personnel_id": str(ACTOR),
                "role": "paramedic",
                "hire_date": "2026-01-15",
            },
            correlation_id="corr-personnel-001",
        )

        training_env = EventEnvelope.wrap(
            event_type="training.completed",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "personnel_id": str(ACTOR),
                "training_type": "ACLS",
                "completed_at": "2026-03-01T10:00:00Z",
            },
            causation_id=create_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        deactivate_env = EventEnvelope.wrap(
            event_type="personnel.deactivated",
            source_repo="adaptix-workforce",
            tenant_id=TENANT,
            payload={
                "personnel_id": str(ACTOR),
                "reason": "resignation",
            },
            causation_id=training_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # Verify causation chain
        assert training_env.causation_id == create_env.envelope_id
        assert deactivate_env.causation_id == training_env.envelope_id

        # All share the same correlation
        for env in [training_env, deactivate_env]:
            assert env.correlation_id == create_env.correlation_id

    def test_workforce_events_owned_by_workforce(self):
        """Workforce owns all scheduling and personnel events."""
        workforce_types = [
            "scheduling.shift.created", "scheduling.shift.filled",
            "scheduling.shift.missed", "personnel.created",
            "personnel.deactivated", "training.completed",
        ]
        for event_type in workforce_types:
            contract = lookup_required(event_type)
            assert contract.source_repo == "adaptix-workforce"


class TestCADSyncLifecycle:
    """End-to-end test for CAD sync events."""

    def test_cad_sync_completed(self):
        """cad.sync.completed event round-trips correctly."""
        env = EventEnvelope.wrap(
            event_type="cad.sync.completed",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "sync_id": "sync-001",
                "record_count": 42,
                "sync_type": "full",
            },
        )
        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["record_count"] == 42
        assert restored.event_type == "cad.sync.completed"

    def test_cad_sync_failed(self):
        """cad.sync.failed captures error details."""
        env = EventEnvelope.wrap(
            event_type="cad.sync.failed",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "sync_id": "sync-fail-001",
                "error": "Connection timeout",
                "retry_count": 3,
            },
        )
        raw = json.loads(json.dumps(env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["error"] == "Connection timeout"


class TestEpcrFullLifecycle:
    """End-to-end test for the complete ePCR lifecycle.

    epcr.created → epcr.signed → epcr.locked → epcr.nemsis.exported.
    """

    def test_epcr_full_pipeline(self):
        """Full ePCR lifecycle through NEMSIS export."""
        # 1. ePCR created
        create_env = EventEnvelope.wrap(
            event_type="epcr.created",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-lc-001",
                "incident_id": "inc-lc-001",
                "patient_id": "pat-lc-001",
            },
            correlation_id="corr-epcr-lc-001",
        )

        # 2. ePCR signed
        sign_env = EventEnvelope.wrap(
            event_type="epcr.signed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-lc-001",
                "incident_id": "inc-lc-001",
                "patient_id": "pat-lc-001",
                "signed_by": str(ACTOR),
                "signed_at": "2026-04-12T10:00:00Z",
            },
            actor_id=ACTOR,
            causation_id=create_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # 3. ePCR locked for QA
        lock_env = EventEnvelope.wrap(
            event_type="epcr.locked",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-lc-001",
                "lock_reason": "signed",
            },
            causation_id=sign_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # 4. NEMSIS exported
        export_env = EventEnvelope.wrap(
            event_type="epcr.nemsis.exported",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={
                "epcr_id": "epcr-lc-001",
                "export_format": "xml",
                "export_id": "exp-001",
            },
            causation_id=lock_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # Verify causation chain
        assert sign_env.causation_id == create_env.envelope_id
        assert lock_env.causation_id == sign_env.envelope_id
        assert export_env.causation_id == lock_env.envelope_id

        # Verify correlation preserved
        for env in [sign_env, lock_env, export_env]:
            assert env.correlation_id == create_env.correlation_id

        # Verify all round-trip through JSON
        for env in [create_env, sign_env, lock_env, export_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.envelope_id == env.envelope_id


class TestIncidentFullLifecycle:
    """End-to-end test for the full incident lifecycle.

    incident.created → status_changed → unit.status_changed → incident.closed.
    """

    def test_incident_lifecycle(self):
        """Full incident from creation to closure."""
        # 1. Incident dispatched
        create_env = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "incident_id": "inc-full-001",
                "incident_number": "INC-2026-100",
                "priority": "bravo",
                "location": "789 Elm St",
            },
            correlation_id="corr-inc-full-001",
        )

        # 2. Status changes to dispatched
        status_env = EventEnvelope.wrap(
            event_type="incident.status_changed",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "incident_id": "inc-full-001",
                "old_status": "pending",
                "new_status": "dispatched",
            },
            causation_id=create_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # 3. Unit status changes to en_route
        unit_env = EventEnvelope.wrap(
            event_type="unit.status_changed",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "unit_id": "unit-m3",
                "old_status": "available",
                "new_status": "en_route",
                "incident_id": "inc-full-001",
            },
            causation_id=status_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # 4. Incident closed
        close_env = EventEnvelope.wrap(
            event_type="incident.closed",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={
                "incident_id": "inc-full-001",
                "close_reason": "patient_transported",
                "closed_at": "2026-04-12T11:00:00Z",
            },
            causation_id=unit_env.envelope_id,
            correlation_id=create_env.correlation_id,
        )

        # Verify causation chain
        assert status_env.causation_id == create_env.envelope_id
        assert unit_env.causation_id == status_env.envelope_id
        assert close_env.causation_id == unit_env.envelope_id

        # Verify all round-trip
        for env in [create_env, status_env, unit_env, close_env]:
            raw = json.loads(json.dumps(env.to_bus_dict()))
            restored = EventEnvelope.from_bus_dict(raw)
            assert restored.event_type == env.event_type


class TestMDTSessionLifecycle:
    """End-to-end test for MDT session lifecycle.

    mdt.login → mdt.status_changed → mdt.message.sent → mdt.logout.
    """

    def test_mdt_session(self):
        """Full MDT session from login to logout."""
        login_env = EventEnvelope.wrap(
            event_type="mdt.login",
            source_repo="adaptix-field",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "device_id": "mdt-tablet-001",
                "unit_id": "unit-m1",
            },
            correlation_id="corr-mdt-session",
        )

        status_env = EventEnvelope.wrap(
            event_type="mdt.status_changed",
            source_repo="adaptix-field",
            tenant_id=TENANT,
            payload={
                "unit_id": "unit-m1",
                "status_code": "available",
                "latitude": 37.7749,
                "longitude": -122.4194,
            },
            causation_id=login_env.envelope_id,
            correlation_id=login_env.correlation_id,
        )

        message_env = EventEnvelope.wrap(
            event_type="mdt.message.sent",
            source_repo="adaptix-field",
            tenant_id=TENANT,
            payload={
                "message_id": "msg-001",
                "from_unit": "unit-m1",
                "to_unit": "unit-m2",
                "body": "en route to scene",
            },
            causation_id=status_env.envelope_id,
            correlation_id=login_env.correlation_id,
        )

        logout_env = EventEnvelope.wrap(
            event_type="mdt.logout",
            source_repo="adaptix-field",
            tenant_id=TENANT,
            payload={
                "user_id": str(ACTOR),
                "device_id": "mdt-tablet-001",
                "unit_id": "unit-m1",
            },
            causation_id=message_env.envelope_id,
            correlation_id=login_env.correlation_id,
        )

        # Verify causation chain
        assert status_env.causation_id == login_env.envelope_id
        assert message_env.causation_id == status_env.envelope_id
        assert logout_env.causation_id == message_env.envelope_id

        # All share correlation
        for env in [status_env, message_env, logout_env]:
            assert env.correlation_id == login_env.correlation_id


class TestFireNerisLifecycle:
    """End-to-end test for fire incident and NERIS submission lifecycle.

    fire.incident.created → status_changed → closed → neris submission lifecycle.
    """

    def test_fire_to_neris_pipeline(self):
        """Fire incident lifecycle through NERIS submission."""
        # 1. Fire incident created
        fire_env = EventEnvelope.wrap(
            event_type="fire.incident.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-lc-001",
                "incident_type": "structure_fire",
                "address": "456 Oak Ave",
            },
            correlation_id="corr-fire-lc-001",
        )

        # 2. Status updated
        status_env = EventEnvelope.wrap(
            event_type="fire.incident.status_changed",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-lc-001",
                "old_status": "dispatched",
                "new_status": "on_scene",
            },
            causation_id=fire_env.envelope_id,
            correlation_id=fire_env.correlation_id,
        )

        # 3. Fire incident closed
        close_env = EventEnvelope.wrap(
            event_type="fire.incident.closed",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "fire_incident_id": "fire-lc-001",
                "close_reason": "fire_extinguished",
            },
            causation_id=status_env.envelope_id,
            correlation_id=fire_env.correlation_id,
        )

        # 4. NERIS submission created
        neris_env = EventEnvelope.wrap(
            event_type="neris.submission.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-001",
                "fire_incident_id": "fire-lc-001",
            },
            causation_id=close_env.envelope_id,
            correlation_id=fire_env.correlation_id,
        )

        # 5. NERIS acknowledged
        ack_env = EventEnvelope.wrap(
            event_type="neris.submission.acknowledged",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-001",
                "state_reference": "NERIS-2026-001",
            },
            causation_id=neris_env.envelope_id,
            correlation_id=fire_env.correlation_id,
        )

        # Verify full chain
        assert status_env.causation_id == fire_env.envelope_id
        assert close_env.causation_id == status_env.envelope_id
        assert neris_env.causation_id == close_env.envelope_id
        assert ack_env.causation_id == neris_env.envelope_id

        # All share correlation
        for env in [status_env, close_env, neris_env, ack_env]:
            assert env.correlation_id == fire_env.correlation_id

    def test_neris_rejection(self):
        """NERIS submission rejection path."""
        submit_env = EventEnvelope.wrap(
            event_type="neris.submission.created",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-rej-001",
                "fire_incident_id": "fire-rej-001",
            },
        )

        reject_env = EventEnvelope.wrap(
            event_type="neris.submission.rejected",
            source_repo="adaptix-fire",
            tenant_id=TENANT,
            payload={
                "submission_id": "neris-rej-001",
                "rejection_reason": "Missing required fields",
            },
            causation_id=submit_env.envelope_id,
        )

        assert reject_env.causation_id == submit_env.envelope_id
        raw = json.loads(json.dumps(reject_env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["rejection_reason"] == "Missing required fields"


class TestCrewLinkFullLifecycle:
    """End-to-end test for the full CrewLink alert → assignment lifecycle."""

    def test_alert_acknowledged_and_expired(self):
        """alert.created → acknowledged, and alert.created → expired paths."""
        alert_env = EventEnvelope.wrap(
            event_type="crewlink.alert.created",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-lc-001",
                "page_type": "dispatch",
                "priority": "high",
                "recipients": ["device-token-001"],
            },
            correlation_id="corr-crew-lc-001",
        )

        ack_env = EventEnvelope.wrap(
            event_type="crewlink.alert.acknowledged",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-lc-001",
                "acknowledged_by": str(ACTOR),
            },
            causation_id=alert_env.envelope_id,
            correlation_id=alert_env.correlation_id,
        )

        assert ack_env.causation_id == alert_env.envelope_id

        # Expiry path
        expire_env = EventEnvelope.wrap(
            event_type="crewlink.alert.expired",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "alert_id": "alert-lc-002",
                "expired_at": "2026-04-12T12:00:00Z",
            },
        )
        raw = json.loads(json.dumps(expire_env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.event_type == "crewlink.alert.expired"

    def test_assignment_declined(self):
        """Assignment can be declined."""
        declined_env = EventEnvelope.wrap(
            event_type="crewlink.assignment.declined",
            source_repo="adaptix-crewlink",
            tenant_id=TENANT,
            payload={
                "assignment_id": "assign-dec-001",
                "declined_by": str(ACTOR),
                "reason": "off_duty",
            },
        )
        raw = json.loads(json.dumps(declined_env.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)
        assert restored.payload["reason"] == "off_duty"


class TestPatientEventLifecycle:
    """End-to-end test for patient events."""

    def test_patient_account_and_dispute(self):
        """patient.account.updated → patient.financial.dispute.created."""
        account_env = EventEnvelope.wrap(
            event_type="patient.account.updated",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "patient_id": "pat-acct-001",
                "update_type": "insurance_change",
            },
            correlation_id="corr-patient-001",
        )

        dispute_env = EventEnvelope.wrap(
            event_type="patient.financial.dispute.created",
            source_repo="adaptix-billing",
            tenant_id=TENANT,
            payload={
                "dispute_id": "disp-001",
                "patient_id": "pat-acct-001",
                "claim_id": "clm-disp-001",
                "reason": "incorrect_charge",
            },
            causation_id=account_env.envelope_id,
            correlation_id=account_env.correlation_id,
        )

        assert dispute_env.causation_id == account_env.envelope_id
        # Verify AI repo subscribes to this for review
        from adaptix_contracts.compat import get_declaration
        ai_dec = get_declaration("adaptix-ai")
        assert ai_dec is not None
        assert "patient.financial.dispute.created" in ai_dec.event_types


class TestTypedEventEnvelopeRoundTrip:
    """Full typed-event → envelope → JSON → deserialize → validate round-trip for every event.

    This goes beyond the parametrized wrap test by constructing typed DomainEvent
    instances, extracting their payload, wrapping in an envelope, and round-tripping.
    """

    @pytest.mark.parametrize(
        "event_type",
        all_event_types(),
        ids=lambda et: et,
    )
    def test_typed_event_through_envelope(self, event_type: str):
        """Construct typed event → extract payload → wrap in envelope → JSON round-trip."""
        catalog = EventCatalog()
        schema = catalog.get_schema(event_type)
        assert schema is not None

        # Build typed event instance
        kwargs = _minimal_kwargs_for(schema, event_type)
        instance = schema(**kwargs)

        # Look up contract
        contract = lookup_required(event_type)

        # Wrap payload in envelope
        envelope = EventEnvelope.wrap(
            event_type=event_type,
            source_repo=contract.source_repo,
            tenant_id=instance.tenant_id,
            payload=instance.payload,
            schema_version=contract.schema_version,
        )
        assert envelope.event_type == event_type
        assert envelope.schema_version == contract.schema_version

        # Serialize and deserialize
        raw = json.loads(json.dumps(envelope.to_bus_dict()))
        restored = EventEnvelope.from_bus_dict(raw)

        assert restored.event_type == event_type
        assert restored.source_repo == contract.source_repo
        assert restored.schema_version == contract.schema_version
        assert restored.envelope_id == envelope.envelope_id
        assert restored.tenant_id == envelope.tenant_id

        # Validate compatibility
        assert restored.is_compatible_with("0.1.0", "0.2.x")
