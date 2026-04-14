"""
Tests for adaptix_contracts.registry

Validates:
  - All CONTRACT_REGISTRY entries are structurally valid
  - No duplicate event_type registrations
  - lookup() / lookup_required() behaviour
  - by_source_repo() and by_stability() filters
  - catalog_summary() structure
  - Architecture policies: fire isolation, crewlink device-first, etc.
"""

from __future__ import annotations

import pytest

from adaptix_contracts.registry import (
    CONTRACT_REGISTRY,
    ContractEntry,
    all_event_types,
    by_source_repo,
    by_stability,
    catalog_summary,
    lookup,
    lookup_required,
)

VALID_STABILITIES = frozenset({"stable", "beta", "experimental", "deprecated"})
VALID_REPOS = frozenset(
    {
        "adaptix-core",
        "adaptix-cad",
        "adaptix-field",
        "adaptix-epcr",
        "adaptix-medications",
        "adaptix-inventory",
        "adaptix-narcotics",
        "adaptix-billing",
        "adaptix-fire",
        "adaptix-air",
        "adaptix-crewlink",
        "adaptix-transportlink",
        "adaptix-transport",  # Added
        "adaptix-workforce",
        "adaptix-command",
        "adaptix-flow",
        "adaptix-pulse",
        "adaptix-interop",
        "adaptix-insight",
        "adaptix-ai",
        "adaptix-admin",
        "adaptix-mdt",  # Added
        "adaptix-communications",  # Added
    }
)


class TestRegistryStructure:
    def test_registry_is_non_empty(self):
        assert len(CONTRACT_REGISTRY) > 0

    def test_no_duplicate_event_types(self):
        event_types = [e.event_type for e in CONTRACT_REGISTRY]
        assert len(event_types) == len(set(event_types)), (
            f"Duplicate event types found: {[t for t in event_types if event_types.count(t) > 1]}"
        )

    def test_all_event_types_are_dot_namespaced(self):
        for entry in CONTRACT_REGISTRY:
            assert "." in entry.event_type, (
                f"Event type {entry.event_type!r} must be dot-namespaced e.g. 'incident.created'"
            )

    def test_all_source_repos_are_known(self):
        for entry in CONTRACT_REGISTRY:
            assert entry.source_repo in VALID_REPOS, (
                f"{entry.event_type!r} has unknown source_repo {entry.source_repo!r}"
            )

    def test_all_stabilities_are_valid(self):
        for entry in CONTRACT_REGISTRY:
            assert entry.stability in VALID_STABILITIES, (
                f"{entry.event_type!r} has invalid stability {entry.stability!r}"
            )

    def test_all_schema_versions_are_positive(self):
        for entry in CONTRACT_REGISTRY:
            assert entry.schema_version >= 1, (
                f"{entry.event_type!r} has invalid schema_version {entry.schema_version}"
            )

    def test_all_entries_are_contract_entry_instances(self):
        for entry in CONTRACT_REGISTRY:
            assert isinstance(entry, ContractEntry)


class TestLookup:
    def test_lookup_known_event(self):
        entry = lookup("incident.created")
        assert entry is not None
        assert entry.source_repo == "adaptix-cad"

    def test_lookup_unknown_returns_none(self):
        assert lookup("nonexistent.event.type") is None

    def test_lookup_required_known_event(self):
        entry = lookup_required("epcr.signed")
        assert entry.event_type == "epcr.signed"

    def test_lookup_required_unknown_raises_key_error(self):
        with pytest.raises(KeyError, match="not registered"):
            lookup_required("shadow.realm.event")

    def test_all_event_types_is_sorted(self):
        types = all_event_types()
        assert types == sorted(types)

    def test_all_event_types_covers_registry(self):
        assert set(all_event_types()) == {e.event_type for e in CONTRACT_REGISTRY}


class TestFilters:
    def test_by_source_repo_returns_only_matching(self):
        fire_events = by_source_repo("adaptix-fire")
        assert len(fire_events) > 0
        assert all(e.source_repo == "adaptix-fire" for e in fire_events)

    def test_by_source_repo_unknown_returns_empty(self):
        assert by_source_repo("adaptix-nonexistent") == []

    def test_by_stability_stable(self):
        stable = by_stability("stable")
        assert len(stable) > 0
        assert all(e.stability == "stable" for e in stable)

    def test_by_stability_beta(self):
        beta = by_stability("beta")
        assert all(e.stability == "beta" for e in beta)


class TestCatalogSummary:
    def test_summary_has_required_keys(self):
        summary = catalog_summary()
        assert "total_event_types" in summary
        assert "by_stability" in summary
        assert "by_source_repo" in summary

    def test_total_matches_registry(self):
        summary = catalog_summary()
        assert summary["total_event_types"] == len(CONTRACT_REGISTRY)

    def test_by_stability_sums_to_total(self):
        summary = catalog_summary()
        assert sum(summary["by_stability"].values()) == summary["total_event_types"]

    def test_by_source_repo_sums_to_total(self):
        summary = catalog_summary()
        assert sum(summary["by_source_repo"].values()) == summary["total_event_types"]


class TestArchitecturePolicies:
    """Encode the governing architecture policies as executable tests.

    These tests serve as a machine-readable contract for the service-line policy
    defined in architecture_service_line_policy.md.
    """

    def test_fire_events_owned_by_adaptix_fire(self):
        fire_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("fire.")]
        assert len(fire_events) > 0
        assert all(e.source_repo == "adaptix-fire" for e in fire_events)

    def test_neris_events_owned_by_adaptix_fire(self):
        neris_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("neris.")]
        assert len(neris_events) > 0
        assert all(e.source_repo == "adaptix-fire" for e in neris_events)

    def test_crewlink_events_owned_by_adaptix_crewlink(self):
        cl_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("crewlink.")]
        assert len(cl_events) > 0
        assert all(e.source_repo == "adaptix-crewlink" for e in cl_events)

    def test_crewlink_alert_has_device_recipient_field(self):
        """Push-first delivery requires recipients identified by device registry."""
        entry = lookup_required("crewlink.alert.created")
        assert "recipients" in entry.payload_fields

    def test_billing_events_owned_by_adaptix_billing(self):
        billing_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("billing.")]
        assert all(e.source_repo == "adaptix-billing" for e in billing_events)

    def test_mdt_events_owned_by_adaptix_field_or_mdt(self):
        """MDT events can be owned by adaptix-field (device-level) or adaptix-mdt (MDT-specific)."""
        mdt_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("mdt.")]
        assert len(mdt_events) > 0
        allowed_repos = {"adaptix-field", "adaptix-mdt"}
        assert all(e.source_repo in allowed_repos for e in mdt_events), (
            f"MDT events must be in adaptix-field or adaptix-mdt repos"
        )

    def test_no_telnyx_billing_sms_event_in_operational_domain(self):
        """Telnyx is billing-only. No SMS/voice events should be in operational domains."""
        for entry in CONTRACT_REGISTRY:
            if entry.source_repo in {"adaptix-cad", "adaptix-crewlink", "adaptix-field"}:
                assert "telnyx" not in entry.event_type.lower(), (
                    f"Event {entry.event_type!r} in operational repo {entry.source_repo!r} "
                    f"must not reference Telnyx (billing-only provider)"
                )

    def test_epcr_signed_triggers_billing_and_ai(self):
        """epcr.signed is the integration point for billing claim creation and AI review."""
        entry = lookup_required("epcr.signed")
        assert "signed_at" in entry.payload_fields
        assert "patient_id" in entry.payload_fields

    def test_core_owns_audit_and_tenancy(self):
        core_types = {e.event_type for e in by_source_repo("adaptix-core")}
        assert "audit.entry.created" in core_types
        assert "tenant.created" in core_types
        assert "user.created" in core_types

    def test_ai_events_owned_by_adaptix_ai(self):
        """AI/ML events must be owned by adaptix-ai."""
        ai_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("ai.")]
        assert len(ai_events) > 0, "AI events should exist"
        assert all(e.source_repo == "adaptix-ai" for e in ai_events)

    def test_air_events_owned_by_adaptix_air(self):
        """Air medical/HEMS events must be owned by adaptix-air."""
        air_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("air.")]
        assert len(air_events) > 0, "Air medical events should exist"
        assert all(e.source_repo == "adaptix-air" for e in air_events)

    def test_inventory_events_owned_by_adaptix_inventory(self):
        """Inventory/supply chain events must be owned by adaptix-inventory."""
        inv_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("inventory.")]
        assert len(inv_events) > 0, "Inventory events should exist"
        assert all(e.source_repo == "adaptix-inventory" for e in inv_events)

    def test_communications_events_owned_by_adaptix_communications(self):
        """Communications events must be owned by adaptix-communications."""
        comm_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("communication.")]
        assert len(comm_events) > 0, "Communication events should exist"
        assert all(e.source_repo == "adaptix-communications" for e in comm_events)

    def test_interop_events_owned_by_adaptix_interop(self):
        """HL7 and FHIR interop events must be owned by adaptix-interop."""
        hl7_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("hl7.")]
        fhir_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("fhir.")]
        assert len(hl7_events) > 0, "HL7 events should exist"
        assert len(fhir_events) > 0, "FHIR events should exist"
        assert all(e.source_repo == "adaptix-interop" for e in hl7_events)
        assert all(e.source_repo == "adaptix-interop" for e in fhir_events)

    def test_integration_events_owned_by_adaptix_core(self):
        """Generic integration events are owned by core platform."""
        integration_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("integration.")]
        assert len(integration_events) > 0, "Integration events should exist"
        assert all(e.source_repo == "adaptix-core" for e in integration_events)

    def test_transport_events_owned_by_adaptix_transport(self):
        """Transport/TransportLink events must be owned by adaptix-transport."""
        transport_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("transport.")]
        assert len(transport_events) > 0, "Transport events should exist"
        assert all(e.source_repo == "adaptix-transport" for e in transport_events)

    def test_command_dashboard_events_owned_by_adaptix_command(self):
        """Command dashboard events must be owned by adaptix-command."""
        dashboard_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("dashboard.")]
        assert len(dashboard_events) > 0, "Dashboard events should exist"
        assert all(e.source_repo == "adaptix-command" for e in dashboard_events)

    def test_admin_investor_events_owned_by_adaptix_admin(self):
        """Admin/investor events must be owned by adaptix-admin."""
        admin_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("investor.")]
        assert len(admin_events) > 0, "Investor events should exist"
        assert all(e.source_repo == "adaptix-admin" for e in admin_events)

    def test_api_events_owned_by_adaptix_core(self):
        """API key management events are core platform concerns."""
        api_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("api.")]
        assert len(api_events) > 0, "API events should exist"
        assert all(e.source_repo == "adaptix-core" for e in api_events)

    def test_compliance_events_properly_distributed(self):
        """Compliance events should be owned by appropriate domain repos."""
        compliance_events = [e for e in CONTRACT_REGISTRY if e.event_type.startswith("compliance.")]
        assert len(compliance_events) > 0, "Compliance events should exist"
        # compliance.hipaa.* → core platform
        # compliance.nemsis.* → epcr
        # compliance.attestation/policy/violation → core
        for event in compliance_events:
            if "nemsis" in event.event_type:
                assert event.source_repo == "adaptix-epcr", f"{event.event_type} should be in adaptix-epcr"
            elif "hipaa" in event.event_type or "attestation" in event.event_type or "policy" in event.event_type or "violation" in event.event_type:
                assert event.source_repo == "adaptix-core", f"{event.event_type} should be in adaptix-core"
