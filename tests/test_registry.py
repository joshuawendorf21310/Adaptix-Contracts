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
