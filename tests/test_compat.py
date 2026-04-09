"""
Tests for adaptix_contracts.compat

Validates:
  - _parse() and _compare() helpers
  - is_version_compatible() range logic including wildcard patterns
  - assert_compatible() raises correctly
  - DownstreamDeclaration model construction and assert_or_raise()
  - COMPATIBILITY_MATRIX entries are all structurally valid
  - validate_matrix() returns correct result for current version
"""

from __future__ import annotations

import pytest

from adaptix_contracts.compat import (
    COMPATIBILITY_MATRIX,
    DownstreamDeclaration,
    _compare,
    _parse,
    assert_compatible,
    get_declaration,
    is_version_compatible,
    validate_matrix,
)
from adaptix_contracts.version import CONTRACT_VERSION


class TestParse:
    def test_major_minor_patch(self):
        assert _parse("1.2.3") == (1, 2, 3)

    def test_major_minor_only(self):
        assert _parse("0.1") == (0, 1, 0)

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            _parse("not.a.version.at.all")

    def test_leading_spaces_stripped(self):
        assert _parse("  1.0.0  ") == (1, 0, 0)


class TestCompare:
    def test_equal(self):
        assert _compare("1.0.0", "1.0.0") == 0

    def test_less_than_patch(self):
        assert _compare("1.0.0", "1.0.1") == -1

    def test_greater_than_minor(self):
        assert _compare("1.1.0", "1.0.9") == 1

    def test_major_dominates(self):
        assert _compare("2.0.0", "1.99.99") == 1


class TestIsVersionCompatible:
    def test_in_range(self):
        assert is_version_compatible("0.2.0", "0.1.0", "0.3.0")

    def test_at_minimum(self):
        assert is_version_compatible("0.1.1", "0.1.1")

    def test_below_minimum(self):
        assert not is_version_compatible("0.1.0", "0.1.1")

    def test_above_maximum(self):
        assert not is_version_compatible("1.0.0", "0.1.0", "0.9.9")

    def test_at_maximum(self):
        assert is_version_compatible("0.2.0", "0.1.0", "0.2.0")

    def test_no_maximum(self):
        assert is_version_compatible("99.0.0", "0.1.0")

    def test_wildcard_patch(self):
        assert is_version_compatible("0.2.5", "0.1.0", "0.2.x")
        assert not is_version_compatible("0.3.0", "0.1.0", "0.2.x")

    def test_current_contract_version_is_compatible_with_self(self):
        assert is_version_compatible(CONTRACT_VERSION, CONTRACT_VERSION)


class TestAssertCompatible:
    def test_compatible_does_not_raise(self):
        assert_compatible(min_version="0.1.0", current_version="0.2.0")

    def test_compatible_with_max(self):
        assert_compatible(min_version="0.1.0", max_version="0.2.x", current_version="0.2.0")

    def test_incompatible_raises(self):
        with pytest.raises(RuntimeError, match="version mismatch"):
            assert_compatible(min_version="99.0.0", current_version="0.2.0")

    def test_uses_installed_version_when_none_given(self):
        # Should not raise — installed version is compatible with itself
        assert_compatible(min_version="0.1.0")


class TestDownstreamDeclaration:
    def test_model_construction(self):
        dec = DownstreamDeclaration(
            repo="adaptix-test",
            min_contract_version="0.1.0",
            max_contract_version="0.2.x",
            event_types=["incident.created"],
            notes="Test declaration",
        )
        assert dec.repo == "adaptix-test"
        assert dec.event_types == ["incident.created"]

    def test_assert_or_raise_passes(self):
        dec = DownstreamDeclaration(
            repo="adaptix-test",
            min_contract_version="0.1.0",
            max_contract_version="0.2.x",
        )
        # Should not raise
        dec.assert_or_raise(current_version="0.2.0")

    def test_assert_or_raise_fails(self):
        dec = DownstreamDeclaration(
            repo="adaptix-test",
            min_contract_version="99.0.0",
        )
        with pytest.raises(RuntimeError):
            dec.assert_or_raise(current_version="0.2.0")

    def test_event_types_defaults_to_empty_list(self):
        dec = DownstreamDeclaration(
            repo="adaptix-test",
            min_contract_version="0.1.0",
        )
        assert dec.event_types == []


class TestCompatibilityMatrix:
    def test_matrix_is_non_empty(self):
        assert len(COMPATIBILITY_MATRIX) > 0

    def test_all_entries_have_valid_repo_slugs(self):
        for dec in COMPATIBILITY_MATRIX:
            assert dec.repo.startswith("adaptix-"), f"Bad repo: {dec.repo}"

    def test_all_min_versions_are_parseable(self):
        for dec in COMPATIBILITY_MATRIX:
            _parse(dec.min_contract_version)  # Must not raise

    def test_all_max_versions_are_parseable_or_none(self):
        for dec in COMPATIBILITY_MATRIX:
            if dec.max_contract_version is not None:
                _parse(dec.max_contract_version.replace(".x", ".0"))

    def test_all_entries_compatible_with_current(self):
        result = validate_matrix()
        assert result["incompatible"] == [], (
            f"Some repos are not compatible with {result['current_version']}: "
            f"{result['incompatible']}"
        )

    def test_validate_matrix_structure(self):
        result = validate_matrix()
        assert "current_version" in result
        assert "compatible" in result
        assert "incompatible" in result
        assert result["current_version"] == CONTRACT_VERSION

    def test_no_duplicate_repos(self):
        repos = [dec.repo for dec in COMPATIBILITY_MATRIX]
        assert len(repos) == len(set(repos)), f"Duplicate repo entries: {repos}"

    def test_get_declaration(self):
        dec = get_declaration("adaptix-core")
        assert dec is not None
        assert dec.repo == "adaptix-core"

    def test_get_declaration_unknown(self):
        assert get_declaration("adaptix-nonexistent") is None

    def test_adaptix_core_covers_audit_events(self):
        dec = get_declaration("adaptix-core")
        assert dec is not None
        assert "audit.entry.created" in dec.event_types

    def test_fire_does_not_consume_mdt_events(self):
        """Fire standalone should not subscribe to MDT/CAD/CrewLink events by policy."""
        dec = get_declaration("adaptix-fire")
        assert dec is not None
        for forbidden in ("mdt.login", "mdt.status_changed", "crewlink.alert.created"):
            assert forbidden not in dec.event_types, (
                f"Fire should not subscribe to {forbidden!r} by architecture policy"
            )
