"""
Adaptix Contracts — Contract Registry  v0.2.0

A static, auto-discovered catalog of every event type the platform may emit,
with its canonical source repo, current schema_version, and stability level.

This is SEPARATE from the runtime EventCatalog (which lives in adaptix-core).
The ContractRegistry is a build-time / documentation-time authority — it can
be imported without starting the application.

Stability levels:
  stable      — contract is finalized; only additive changes allowed
  beta        — contract is in active use but may have additive changes
  experimental — contract may change; downstream should not build hard dependencies
  deprecated  — contract will be removed in the next major version

Usage:
    from adaptix_contracts.registry import CONTRACT_REGISTRY, lookup

    contract = lookup("incident.created")
    print(contract.source_repo, contract.schema_version, contract.stability)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Stability = Literal["stable", "beta", "experimental", "deprecated"]


@dataclass(frozen=True, slots=True)
class ContractEntry:
    """A single registered contract."""

    event_type: str
    source_repo: str
    schema_version: int
    stability: Stability
    payload_fields: tuple[str, ...] = field(default_factory=tuple)
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "source_repo": self.source_repo,
            "schema_version": self.schema_version,
            "stability": self.stability,
            "payload_fields": list(self.payload_fields),
            "notes": self.notes,
        }


# ─── Registry ────────────────────────────────────────────────────────────────
# Authoritative list of all cross-repo events.  Add here when introducing a
# new event type; bump schema_version here when payload shape changes.

CONTRACT_REGISTRY: tuple[ContractEntry, ...] = (
    # ── Auth / Tenancy ────────────────────────────────────────────────────
    ContractEntry(
        event_type="tenant.created",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("tenant_id", "name", "service_lines"),
        notes="Emitted once when a new tenant is provisioned.",
    ),
    ContractEntry(
        event_type="tenant.suspended",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("tenant_id", "reason"),
    ),
    ContractEntry(
        event_type="user.created",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("user_id", "tenant_id", "email", "roles"),
    ),
    ContractEntry(
        event_type="user.deactivated",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("user_id", "tenant_id"),
    ),
    ContractEntry(
        event_type="feature_flag.toggled",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("flag_name", "enabled", "tenant_id"),
    ),
    # ── Audit ─────────────────────────────────────────────────────────────
    ContractEntry(
        event_type="audit.entry.created",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("entry_id", "action", "resource_type", "resource_id", "actor_id"),
    ),
    # ── Webhooks ──────────────────────────────────────────────────────────
    ContractEntry(
        event_type="webhook.delivered",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("webhook_id", "endpoint_url", "http_status"),
    ),
    ContractEntry(
        event_type="webhook.failed",
        source_repo="adaptix-core",
        schema_version=1,
        stability="stable",
        payload_fields=("webhook_id", "endpoint_url", "error", "attempt"),
    ),
    # ── Incident ──────────────────────────────────────────────────────────
    ContractEntry(
        event_type="incident.created",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("incident_id", "incident_number", "priority", "location", "call_type"),
    ),
    ContractEntry(
        event_type="incident.status_changed",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("incident_id", "previous_status", "new_status"),
    ),
    ContractEntry(
        event_type="incident.closed",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("incident_id", "disposition"),
    ),
    ContractEntry(
        event_type="unit.status_changed",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("unit_id", "unit_identifier", "previous_status", "new_status"),
    ),
    # ── CAD Sync ──────────────────────────────────────────────────────────
    ContractEntry(
        event_type="cad.sync.completed",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("sync_id", "cad_system_type", "incident_count"),
    ),
    ContractEntry(
        event_type="cad.sync.failed",
        source_repo="adaptix-cad",
        schema_version=1,
        stability="stable",
        payload_fields=("sync_id", "cad_system_type", "error"),
    ),
    # ── MDT ───────────────────────────────────────────────────────────────
    ContractEntry(
        event_type="mdt.login",
        source_repo="adaptix-field",
        schema_version=1,
        stability="stable",
        payload_fields=("unit_id", "user_id", "device_id"),
    ),
    ContractEntry(
        event_type="mdt.logout",
        source_repo="adaptix-field",
        schema_version=1,
        stability="stable",
        payload_fields=("unit_id", "user_id", "device_id"),
    ),
    ContractEntry(
        event_type="mdt.status_changed",
        source_repo="adaptix-field",
        schema_version=1,
        stability="stable",
        payload_fields=("unit_id", "status_code", "latitude", "longitude"),
    ),
    ContractEntry(
        event_type="mdt.message.sent",
        source_repo="adaptix-field",
        schema_version=1,
        stability="stable",
        payload_fields=("message_id", "unit_id", "body", "priority"),
    ),
    # ── ePCR ──────────────────────────────────────────────────────────────
    ContractEntry(
        event_type="epcr.created",
        source_repo="adaptix-epcr",
        schema_version=1,
        stability="stable",
        payload_fields=("epcr_id", "incident_id", "patient_id"),
    ),
    ContractEntry(
        event_type="epcr.signed",
        source_repo="adaptix-epcr",
        schema_version=1,
        stability="stable",
        payload_fields=("epcr_id", "incident_id", "patient_id", "signed_by", "signed_at"),
        notes="Triggers billing claim creation and AI narrative review.",
    ),
    ContractEntry(
        event_type="epcr.locked",
        source_repo="adaptix-epcr",
        schema_version=1,
        stability="stable",
        payload_fields=("epcr_id", "incident_id"),
    ),
    ContractEntry(
        event_type="epcr.nemsis.exported",
        source_repo="adaptix-epcr",
        schema_version=1,
        stability="stable",
        payload_fields=("export_id", "epcr_id", "state_code", "export_status"),
    ),
    # ── Billing ───────────────────────────────────────────────────────────
    ContractEntry(
        event_type="billing.claim.created",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("claim_id", "epcr_id", "patient_id", "payer"),
    ),
    ContractEntry(
        event_type="billing.claim.submitted",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("claim_id", "payer", "submitted_at"),
    ),
    ContractEntry(
        event_type="billing.claim.paid",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("claim_id", "amount_paid", "paid_at"),
    ),
    ContractEntry(
        event_type="billing.claim.denied",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("claim_id", "denial_code", "denial_reason"),
    ),
    ContractEntry(
        event_type="payment.posted",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("payment_id", "account_id", "amount"),
    ),
    ContractEntry(
        event_type="payment.failed",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("payment_id", "account_id", "error_code"),
    ),
    ContractEntry(
        event_type="payment.refunded",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("payment_id", "account_id", "refund_amount"),
    ),
    # ── Patient ───────────────────────────────────────────────────────────
    ContractEntry(
        event_type="patient.account.updated",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="stable",
        payload_fields=("account_id", "patient_id", "status"),
    ),
    ContractEntry(
        event_type="patient.financial.dispute.created",
        source_repo="adaptix-billing",
        schema_version=1,
        stability="beta",
        payload_fields=("dispute_id", "account_id", "amount_disputed"),
    ),
    # ── Fire / NERIS ──────────────────────────────────────────────────────
    ContractEntry(
        event_type="fire.incident.created",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("fire_incident_id", "incident_type", "address"),
    ),
    ContractEntry(
        event_type="fire.incident.status_changed",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("fire_incident_id", "previous_status", "new_status"),
    ),
    ContractEntry(
        event_type="fire.incident.closed",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("fire_incident_id", "disposition"),
    ),
    ContractEntry(
        event_type="neris.submission.created",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("submission_id", "fire_incident_id", "state_code"),
    ),
    ContractEntry(
        event_type="neris.submission.acknowledged",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("submission_id", "acknowledged_at"),
    ),
    ContractEntry(
        event_type="neris.submission.rejected",
        source_repo="adaptix-fire",
        schema_version=1,
        stability="stable",
        payload_fields=("submission_id", "rejection_reason"),
    ),
    # ── CrewLink ──────────────────────────────────────────────────────────
    ContractEntry(
        event_type="crewlink.alert.created",
        source_repo="adaptix-crewlink",
        schema_version=1,
        stability="stable",
        payload_fields=("alert_id", "page_type", "priority", "recipients"),
        notes="Push-first delivery. Recipients identified by device registry, not phone number.",
    ),
    ContractEntry(
        event_type="crewlink.alert.acknowledged",
        source_repo="adaptix-crewlink",
        schema_version=1,
        stability="stable",
        payload_fields=("alert_id", "user_id", "device_id", "acknowledged_at"),
    ),
    ContractEntry(
        event_type="crewlink.alert.expired",
        source_repo="adaptix-crewlink",
        schema_version=1,
        stability="stable",
        payload_fields=("alert_id",),
    ),
    ContractEntry(
        event_type="crewlink.assignment.accepted",
        source_repo="adaptix-crewlink",
        schema_version=1,
        stability="stable",
        payload_fields=("assignment_id", "incident_id", "user_id", "unit_id"),
    ),
    ContractEntry(
        event_type="crewlink.assignment.declined",
        source_repo="adaptix-crewlink",
        schema_version=1,
        stability="stable",
        payload_fields=("assignment_id", "user_id", "reason"),
    ),
    # ── Scheduling / Workforce ────────────────────────────────────────────
    ContractEntry(
        event_type="scheduling.shift.created",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="stable",
        payload_fields=("shift_id", "unit_id", "start_time", "end_time"),
    ),
    ContractEntry(
        event_type="scheduling.shift.filled",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="stable",
        payload_fields=("shift_id", "user_id"),
    ),
    ContractEntry(
        event_type="scheduling.shift.missed",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="stable",
        payload_fields=("shift_id",),
    ),
    ContractEntry(
        event_type="personnel.created",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="stable",
        payload_fields=("user_id", "first_name", "last_name", "role"),
    ),
    ContractEntry(
        event_type="personnel.deactivated",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="stable",
        payload_fields=("user_id", "reason"),
    ),
    ContractEntry(
        event_type="training.completed",
        source_repo="adaptix-workforce",
        schema_version=1,
        stability="beta",
        payload_fields=("training_id", "user_id", "course_name", "completed_at"),
    ),
)

# ─── Lookup helpers ───────────────────────────────────────────────────────────

_INDEX: dict[str, ContractEntry] = {e.event_type: e for e in CONTRACT_REGISTRY}


def lookup(event_type: str) -> ContractEntry | None:
    """Return the ContractEntry for a given event_type, or None if unregistered."""
    return _INDEX.get(event_type)


def lookup_required(event_type: str) -> ContractEntry:
    """Return the ContractEntry, raising KeyError if not registered."""
    entry = _INDEX.get(event_type)
    if entry is None:
        raise KeyError(
            f"Event type {event_type!r} is not registered in the adaptix-contracts registry. "
            f"Register it in adaptix_contracts/registry.py before publishing."
        )
    return entry


def all_event_types() -> list[str]:
    """Return a sorted list of all registered event_type strings."""
    return sorted(_INDEX.keys())


def by_source_repo(repo: str) -> list[ContractEntry]:
    """Return all contracts owned by a given source repo."""
    return [e for e in CONTRACT_REGISTRY if e.source_repo == repo]


def by_stability(stability: Stability) -> list[ContractEntry]:
    """Return all contracts with the given stability level."""
    return [e for e in CONTRACT_REGISTRY if e.stability == stability]


def catalog_summary() -> dict[str, object]:
    """Return a summary dict suitable for health checks or CI output."""
    by_stab: dict[str, int] = {}
    by_repo: dict[str, int] = {}
    for entry in CONTRACT_REGISTRY:
        by_stab[entry.stability] = by_stab.get(entry.stability, 0) + 1
        by_repo[entry.source_repo] = by_repo.get(entry.source_repo, 0) + 1

    return {
        "total_event_types": len(CONTRACT_REGISTRY),
        "by_stability": by_stab,
        "by_source_repo": by_repo,
    }
