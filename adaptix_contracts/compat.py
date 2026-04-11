"""
Adaptix Contracts — Compatibility Layer  v0.2.0

Provides:
  - Version comparison helpers (semver subset: MAJOR.MINOR.PATCH)
  - DownstreamDeclaration: typed model for downstream repos to declare contract support
  - COMPATIBILITY_MATRIX: the machine-readable matrix of all known consumer declarations
  - is_version_compatible(): range check used by EventEnvelope
  - assert_compatible(): hard gate for consumer startup checks

Policy:
  - MAJOR bump → breaking; downstream MUST update before consuming new events
  - MINOR bump → additive; downstream MAY consume without changes (will ignore new fields)
  - PATCH bump → bug-fix; downstream is unaffected

Usage (in a downstream repo's startup):
    from adaptix_contracts.compat import assert_compatible
    assert_compatible(min_version="0.1.1", max_version="0.2.x")
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

# ─── Semver helpers ───────────────────────────────────────────────────────────

_SEMVER_RE = re.compile(r"^(\d+)\.(\d+)(?:\.(\d+))?$")


def _parse(version: str) -> tuple[int, int, int]:
    """Parse a semver string into (major, minor, patch).  Patch defaults to 0."""
    m = _SEMVER_RE.match(version.strip())
    if not m:
        raise ValueError(f"Invalid semver: {version!r}")
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    return major, minor, patch


def _compare(a: str, b: str) -> int:
    """Return -1 / 0 / 1 like cmp(a, b)."""
    ta, tb = _parse(a), _parse(b)
    if ta < tb:
        return -1
    if ta > tb:
        return 1
    return 0


def is_version_compatible(version: str, min_version: str, max_version: str | None = None) -> bool:
    """Return True if *version* is within [min_version, max_version].

    max_version may use 'x' as a wildcard for minor/patch:
      "0.2.x"  → any 0.2.*
      "1.x"    → any 1.*.*
    """
    # Normalise wildcard patterns
    if max_version is not None:
        max_version = re.sub(r"\.x$", ".999999", max_version)
        max_version = re.sub(r"^(\d+)\.x$", r"\1.999999.999999", max_version)

    if _compare(version, min_version) < 0:
        return False
    if max_version is not None and _compare(version, max_version) > 0:
        return False
    return True


def assert_compatible(
    min_version: str,
    max_version: str | None = None,
    current_version: str | None = None,
) -> None:
    """Raise RuntimeError at startup if the installed contracts version is outside the declared range.

    Intended for downstream repo startup guards:

        from adaptix_contracts.compat import assert_compatible
        assert_compatible(min_version="0.1.1", max_version="0.2.x")
    """
    if current_version is None:
        from adaptix_contracts.version import CONTRACT_VERSION

        current_version = CONTRACT_VERSION

    if not is_version_compatible(current_version, min_version, max_version):
        max_str = f" and <= {max_version}" if max_version else ""
        raise RuntimeError(
            f"adaptix-contracts version mismatch: installed={current_version!r} "
            f"but consumer requires >= {min_version!r}{max_str}.  "
            f"Update adaptix-contracts or adjust your compatibility declaration."
        )


# ─── Downstream declaration model ────────────────────────────────────────────


class DownstreamDeclaration(BaseModel):
    """A typed declaration that a downstream repo makes about which contract versions it supports.

    Place this in your repo as ``contracts.json`` at the root, or call
    ``DownstreamDeclaration.assert_or_raise()`` at application startup.
    """

    repo: str = Field(..., description="GitHub repository slug e.g. 'adaptix-cad'")
    min_contract_version: str = Field(
        ...,
        description="Minimum adaptix-contracts version this consumer can handle.",
    )
    max_contract_version: str | None = Field(
        default=None,
        description="Maximum adaptix-contracts version (inclusive). None = unbounded.",
    )
    event_types: list[str] = Field(
        default_factory=list,
        description="Explicit event_type strings this consumer subscribes to.",
    )
    notes: str = Field(
        default="",
        description="Human-readable notes about upgrade blockers or planned migrations.",
    )

    def assert_or_raise(self, current_version: str | None = None) -> None:
        """Hard gate — call at consumer startup to abort if contracts are incompatible."""
        assert_compatible(
            min_version=self.min_contract_version,
            max_version=self.max_contract_version,
            current_version=current_version,
        )

    @classmethod
    def from_json_file(cls, path: str | Path) -> DownstreamDeclaration:
        """Load a downstream declaration from a JSON file."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.model_validate(data)


# ─── Known compatibility matrix ───────────────────────────────────────────────
# Each entry is the DECLARED support level from each product repo.
# Repos are responsible for keeping this up-to-date via PR.

COMPATIBILITY_MATRIX: list[DownstreamDeclaration] = [
    DownstreamDeclaration(
        repo="adaptix-core",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "audit.entry.created",
            "tenant.created",
            "tenant.suspended",
            "user.created",
            "user.deactivated",
            "feature_flag.toggled",
            "webhook.delivered",
            "webhook.failed",
        ],
        notes="Core owns auth/tenancy/governance events. Consumes all structural events for audit.",
    ),
    DownstreamDeclaration(
        repo="adaptix-cad",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "incident.created",
            "incident.status_changed",
            "incident.closed",
            "unit.status_changed",
            "cad.sync.completed",
            "cad.sync.failed",
        ],
        notes="CAD dispatches incidents and unit assignments.",
    ),
    DownstreamDeclaration(
        repo="adaptix-field",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "incident.created",
            "incident.status_changed",
            "mdt.login",
            "mdt.logout",
            "mdt.status_changed",
            "mdt.message.sent",
        ],
        notes="Field/MDT consumes CAD dispatch and emits unit status events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-epcr",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "incident.created",
            "epcr.created",
            "epcr.signed",
            "epcr.locked",
            "epcr.nemsis.exported",
            "nemsis.epcr.locked",
            "nemsis.compliance.check_completed",
            "nemsis.export.queued",
            "nemsis.export.validated",
            "nemsis.export.submitted",
            "nemsis.export.accepted",
            "nemsis.export.rejected",
        ],
        notes="ePCR consumes incident events; emits NEMSIS export lifecycle events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-billing",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "epcr.signed",
            "epcr.locked",
            "billing.claim.created",
            "billing.claim.submitted",
            "billing.claim.paid",
            "billing.claim.denied",
            "patient.account.updated",
            "payment.posted",
            "payment.failed",
            "payment.refunded",
        ],
        notes="Billing consumes signed/locked ePCRs; emits claim lifecycle events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-fire",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "fire.incident.created",
            "fire.incident.status_changed",
            "fire.incident.closed",
            "neris.submission.created",
            "neris.submission.acknowledged",
            "neris.submission.rejected",
        ],
        notes="Fire standalone — does not consume MDT/CAD/CrewLink events by policy.",
    ),
    DownstreamDeclaration(
        repo="adaptix-crewlink",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "incident.created",
            "incident.status_changed",
            "crewlink.alert.created",
            "crewlink.alert.acknowledged",
            "crewlink.alert.expired",
            "crewlink.assignment.accepted",
            "crewlink.assignment.declined",
        ],
        notes="CrewLink is push-first/device-registry-based. Does NOT consume Telnyx SMS events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-workforce",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "scheduling.shift.created",
            "scheduling.shift.filled",
            "scheduling.shift.missed",
            "personnel.created",
            "personnel.deactivated",
            "training.completed",
        ],
        notes="Workforce owns scheduling and personnel lifecycle events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-interop",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=["*"],
        notes="Interop translates all domain events for external integrations (FHIR, HL7, CAD feeds).",
    ),
    DownstreamDeclaration(
        repo="adaptix-ai",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "epcr.signed",
            "billing.claim.denied",
            "patient.financial.dispute.created",
        ],
        notes="AI augments ePCR and billing events. No direct write access to production entities.",
    ),
    DownstreamDeclaration(
        repo="adaptix-admin",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "audit.entry.created",
            "feature_flag.toggled",
            "tenant.suspended",
        ],
        notes="Admin governance surface — read-only consumer of audit and governance events.",
    ),
    DownstreamDeclaration(
        repo="adaptix-command",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=[
            "incident.created",
            "incident.status_changed",
            "unit.status_changed",
            "mdt.status_changed",
            "fire.incident.status_changed",
        ],
        notes="Command dashboard — read-only consumer for operational awareness.",
    ),
    DownstreamDeclaration(
        repo="adaptix-insight",
        min_contract_version="0.1.1",
        max_contract_version="0.2.x",
        event_types=["*"],
        notes="Insight aggregates all events for founder intelligence and analytics.",
    ),
]


def get_declaration(repo: str) -> DownstreamDeclaration | None:
    """Return the compatibility declaration for a given repo slug, or None."""
    for dec in COMPATIBILITY_MATRIX:
        if dec.repo == repo:
            return dec
    return None


def validate_matrix(current_version: str | None = None) -> dict[str, Any]:
    """Check all COMPATIBILITY_MATRIX entries against current_version.

    Returns a dict with structure:
      {"compatible": [...], "incompatible": [...], "current_version": "..."}
    """
    if current_version is None:
        from adaptix_contracts.version import CONTRACT_VERSION

        current_version = CONTRACT_VERSION

    compatible = []
    incompatible = []

    for dec in COMPATIBILITY_MATRIX:
        ok = is_version_compatible(
            current_version, dec.min_contract_version, dec.max_contract_version
        )
        entry = {"repo": dec.repo, "min": dec.min_contract_version, "max": dec.max_contract_version}
        if ok:
            compatible.append(entry)
        else:
            incompatible.append(entry)

    return {
        "current_version": current_version,
        "compatible": compatible,
        "incompatible": incompatible,
    }
