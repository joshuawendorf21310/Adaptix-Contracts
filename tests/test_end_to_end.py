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
        instance = schema(
            event_type=event_type,
            tenant_id=TENANT,
            entity_type=event_type.split(".")[0],
            entity_id=ENTITY,
        )
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
        )

        assert CONTRACT_VERSION == "0.2.0"
        assert EventEnvelope is not None
        assert callable(lookup)
        assert callable(lookup_required)
        assert callable(catalog_summary)
        assert callable(assert_compatible)
        assert callable(is_version_compatible)
