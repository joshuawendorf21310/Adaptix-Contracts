"""Canonical permission registry for Adaptix platforms.

Each domain registers its permissions via contracts, eliminating hard-coded
permission strings in middleware. This enables domain-agnostic RBAC and
allows new domains to be added without modifying core middleware.
"""

from typing import Dict, Set

# Global permission registry, populated at startup by domain modules
_PERMISSION_REGISTRY: Dict[str, str] = {}


def register_permissions(domain: str, permissions: Dict[str, str]) -> None:
    """Register a domain's permissions in the canonical registry.

    Called during domain initialization to populate the global permission
    registry. Each permission is a dot-notation string (e.g., 'billing.claims.submit')
    with a human-readable description.

    Args:
        domain: Domain name for logging/organization (e.g., 'billing', 'epcr', 'cad')
        permissions: Dict mapping permission string → description
    """
    for perm, desc in permissions.items():
        if perm in _PERMISSION_REGISTRY:
            # Warn on duplicate but allow overwrite (last one wins)
            print(f"WARN: Permission '{perm}' already registered, overwriting from {domain}")
        _PERMISSION_REGISTRY[perm] = desc


def get_all_permissions() -> Dict[str, str]:
    """Get all registered permissions.

    Returns:
        Dict of all permission strings → descriptions
    """
    return dict(_PERMISSION_REGISTRY)


def permission_exists(perm: str) -> bool:
    """Check if a permission is registered.

    Args:
        perm: Permission string to check

    Returns:
        True if registered, False otherwise
    """
    return perm in _PERMISSION_REGISTRY


def get_permission_description(perm: str) -> str | None:
    """Get human-readable description for a permission.

    Args:
        perm: Permission string

    Returns:
        Description if found, None otherwise
    """
    return _PERMISSION_REGISTRY.get(perm)


# ============================================================================
# DEFAULT PERMISSION SET
# ============================================================================
# These are the baseline permissions loaded at startup.
# Domains can add additional permissions via register_permissions().

DEFAULT_PERMISSIONS: Dict[str, str] = {
    # Billing domain
    "billing.claims.submit": "Submit a new insurance claim",
    "billing.claims.review": "Review claim status and details",
    "billing.claims.void": "Void an existing claim",
    "billing.payments.record": "Record a payment against a claim",
    "billing.payments.refund": "Process a payment refund",
    "billing.reports.read": "View billing/revenue reports",
    "billing.settings.manage": "Manage billing configuration",
    # ePCR domain
    "epcr.document.create": "Create a new ePCR chart",
    "epcr.document.update": "Update ePCR chart fields",
    "epcr.document.lock": "Lock/sign an ePCR for submission",
    "epcr.document.read": "Read ePCR chart data",
    "epcr.vitals.record": "Record patient vital signs",
    "epcr.narrative.write": "Write ePCR narrative",
    "epcr.qa.review": "QA review an ePCR",
    "epcr.qa.approve": "QA approve an ePCR",
    # CAD / Incident domain
    "cad.incident.create": "Create a new incident",
    "cad.incident.dispatch": "Dispatch units to an incident",
    "cad.incident.update": "Update incident status/details",
    "cad.incident.read": "View incident information",
    "cad.incident.close": "Close an incident",
    "cad.unit.assign": "Assign a unit to an incident",
    # Scheduling domain
    "scheduling.shift.create": "Create a new shift",
    "scheduling.shift.update": "Update shift details",
    "scheduling.shift.read": "View schedules",
    "scheduling.shift.delete": "Delete a shift",
    "scheduling.overtime.approve": "Approve overtime requests",
    # CrewLink domain
    "crewlink.status.read": "View crew status board",
    "crewlink.status.update": "Update own crew status",
    "crewlink.alert.send": "Send CrewLink alerts",
    "crewlink.roster.manage": "Manage crew rosters",
    # Narcotic domain
    "narcotic.vault.create": "Create a narcotic vault",
    "narcotic.vault.read": "View narcotic vaults",
    "narcotic.vault.update": "Update a narcotic vault",
    "narcotic.medication.create": "Add narcotic medication to inventory",
    "narcotic.medication.read": "View narcotic medications",
    "narcotic.medication.update": "Update narcotic medication",
    "narcotic.transaction.issue": "Issue narcotics from vault",
    "narcotic.transaction.return": "Return narcotics to vault",
    "narcotic.transaction.administer": "Administer narcotics to patient",
    "narcotic.transaction.waste": "Waste narcotics with witness",
    "narcotic.transaction.transfer": "Transfer narcotics between vaults",
    "narcotic.transaction.read": "View narcotic transactions",
    "narcotic.audit.conduct": "Conduct narcotic vault audit",
    "narcotic.audit.read": "View narcotic audits",
    "narcotic.discrepancy.record": "Record narcotic discrepancy",
    "narcotic.discrepancy.resolve": "Resolve narcotic discrepancy",
    "narcotic.discrepancy.read": "View narcotic discrepancies",
    "narcotic.report.dea": "Generate DEA compliance report",
    "narcotic.report.expiring": "View expiring medications report",
    # Admin / Organization domain
    "admin.user.create": "Create a user account",
    "admin.user.read": "View user accounts",
    "admin.user.update": "Update user accounts",
    "admin.user.delete": "Deactivate/delete user accounts",
    "admin.user.invite": "Invite new users",
    "admin.org.read": "View organization details",
    "admin.org.update": "Update organization settings",
    "admin.org.settings": "Manage org-level configuration",
    # Audit / Compliance domain
    "audit.log.read": "Read audit trail",
    "compliance.review": "Perform compliance review",
    "compliance.nemsis.validate": "Run NEMSIS validation",
    # System domain (founder only)
    "system.tenant.create": "Create a new tenant",
    "system.tenant.read": "View all tenants",
    "system.tenant.update": "Update tenant configuration",
    "system.tenant.delete": "Deactivate a tenant",
    "system.config.manage": "Manage platform configuration",
    # Communications domain
    "comms.message.send": "Send communications messages",
    "comms.message.read": "Read communications",
    # MDT domain
    "mdt.view": "View mobile data terminal",
    "mdt.dispatch": "Send dispatch via MDT",
}

# Bootstrap the default permissions on module load
register_permissions("adaptix-core", DEFAULT_PERMISSIONS)
