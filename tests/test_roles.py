"""
Tests for adaptix_contracts.utils.roles — normalize_role_claims.

Validates:
  - Deduplication of role claims
  - Ordering with primary_role first
  - Handling of None, empty string, whitespace
  - Mixed input types (list, tuple, set)
"""

from __future__ import annotations

from adaptix_contracts.utils.roles import normalize_role_claims


class TestNormalizeRoleClaims:
    def test_single_primary_role(self):
        result = normalize_role_claims(primary_role="admin")
        assert result == ["admin"]

    def test_single_role(self):
        result = normalize_role_claims(role="paramedic")
        assert result == ["paramedic"]

    def test_roles_list(self):
        result = normalize_role_claims(roles=["admin", "paramedic"])
        assert result == ["admin", "paramedic"]

    def test_primary_role_comes_first(self):
        result = normalize_role_claims(
            primary_role="admin",
            roles=["paramedic", "dispatcher"],
        )
        assert result[0] == "admin"
        assert "paramedic" in result
        assert "dispatcher" in result

    def test_deduplication(self):
        result = normalize_role_claims(
            primary_role="admin",
            role="admin",
            roles=["admin", "paramedic"],
        )
        assert result.count("admin") == 1

    def test_none_values_ignored(self):
        result = normalize_role_claims(primary_role=None, role=None, roles=None)
        assert result == []

    def test_empty_string_ignored(self):
        result = normalize_role_claims(primary_role="", role="", roles=[""])
        assert result == []

    def test_whitespace_only_ignored(self):
        result = normalize_role_claims(primary_role="  ", role="  ")
        assert result == []

    def test_tuple_input(self):
        result = normalize_role_claims(roles=("admin", "medic"))
        assert "admin" in result
        assert "medic" in result

    def test_set_input(self):
        result = normalize_role_claims(roles={"admin", "medic"})
        assert "admin" in result
        assert "medic" in result

    def test_role_and_primary_role_both_inserted_front(self):
        result = normalize_role_claims(
            primary_role="captain",
            role="lieutenant",
            roles=["firefighter"],
        )
        # Both primary_role and role should be at front, with primary_role first
        assert result.index("captain") < result.index("firefighter")
        assert result.index("lieutenant") < result.index("firefighter")

    def test_non_string_values_converted(self):
        result = normalize_role_claims(primary_role=42, roles=[True])
        assert "42" in result
        assert "True" in result
