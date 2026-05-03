"""
Adaptix Event Registry
========================
Canonical registry of all domain events across the Adaptix platform.
Every service that publishes or consumes events MUST import from this registry.
"""

from __future__ import annotations
from typing import Final


# ─── Transport / CAD Events ───────────────────────────────────────────────────
TRANSPORT_SCHEDULED: Final[str] = "TransportScheduled"
TRANSPORT_PUSHED_TO_CAD: Final[str] = "TransportPushedToCAD"

# ─── Crew / CrewLink Events ───────────────────────────────────────────────────
CREW_PAGE_SENT: Final[str] = "CrewPageSent"
CREW_ASSIGNMENT_ACCEPTED: Final[str] = "CrewAssignmentAccepted"
CREW_ASSIGNMENT_DECLINED: Final[str] = "CrewAssignmentDeclined"

# ─── ePCR / Care Events ───────────────────────────────────────────────────────
EPCR_REPORT_CREATED: Final[str] = "EpcrReportCreated"
EPCR_REPORT_VALIDATED: Final[str] = "EpcrReportValidated"
EPCR_BILLING_PACKET_GENERATED: Final[str] = "EpcrBillingPacketGenerated"

# ─── Billing Events ───────────────────────────────────────────────────────────
BILLING_CLAIM_GENERATED: Final[str] = "BillingClaimGenerated"
BILLING_CLAIM_SUBMITTED: Final[str] = "BillingClaimSubmitted"
BILLING_CLAIM_STATUS_UPDATED: Final[str] = "BillingClaimStatusUpdated"
BILLING_ERA_IMPORTED: Final[str] = "BillingEraImported"

# ─── Fire / NERIS Events ──────────────────────────────────────────────────────
FIRE_INCIDENT_CREATED: Final[str] = "FireIncidentCreated"
FIRE_LINKED_CARE_CHART_CREATED: Final[str] = "FireLinkedCareChartCreated"

# ─── HEMS / Air Events ────────────────────────────────────────────────────────
HEMS_TRANSPORT_REQUESTED: Final[str] = "HemsTransportRequested"
HEMS_PILOT_GO_NO_GO_COMPLETED: Final[str] = "HemsPilotGoNoGoCompleted"
HEMS_LAUNCHED: Final[str] = "HemsLaunched"

# ─── Inventory Events ─────────────────────────────────────────────────────────
INVENTORY_LOW_STOCK: Final[str] = "InventoryLowStock"
INVENTORY_DEPLETED: Final[str] = "InventoryDepleted"

# ─── Narcotics Events ─────────────────────────────────────────────────────────
NARCOTIC_DISCREPANCY_CREATED: Final[str] = "NarcoticDiscrepancyCreated"
NARCOTIC_WASTE_WITNESSED: Final[str] = "NarcoticWasteWitnessed"

# ─── MDT / Field Events ───────────────────────────────────────────────────────
MDT_STATUS_CHANGED: Final[str] = "MdtStatusChanged"
MDT_UNIT_LOCATION_UPDATED: Final[str] = "MdtUnitLocationUpdated"
MDT_FATIGUE_RESTRICTION_CREATED: Final[str] = "MdtFatigueRestrictionCreated"
LIGHTS_SIRENS_INTERVAL_RECORDED: Final[str] = "LightsSirensIntervalRecorded"

# ─── Document Events ──────────────────────────────────────────────────────────
DOCUMENT_REQUIREMENT_MISSING: Final[str] = "DocumentRequirementMissing"
DOCUMENT_REQUIREMENT_SATISFIED: Final[str] = "DocumentRequirementSatisfied"

# ─── Core / Auth Events ───────────────────────────────────────────────────────
FOUNDER_POLICY_CHANGED: Final[str] = "FounderPolicyChanged"
USER_CREATED: Final[str] = "UserCreated"
USER_UPDATED: Final[str] = "UserUpdated"
TENANT_CREATED: Final[str] = "TenantCreated"
TENANT_UPDATED: Final[str] = "TenantUpdated"
ROLE_ASSIGNED: Final[str] = "RoleAssigned"
SESSION_CREATED: Final[str] = "SessionCreated"
SESSION_REVOKED: Final[str] = "SessionRevoked"


# ─── Registry Map ─────────────────────────────────────────────────────────────
ALL_EVENTS: Final[dict] = {
    # Transport / CAD
    TRANSPORT_SCHEDULED: {
        "version": "1.0",
        "source_service": "adaptix-transportlink",
        "description": "A transport has been scheduled",
        "channels": ["cad.case.updated"],
    },
    TRANSPORT_PUSHED_TO_CAD: {
        "version": "1.0",
        "source_service": "adaptix-transportlink",
        "description": "Transport request pushed to CAD for dispatch",
        "channels": ["cad.case.updated"],
    },
    # Crew
    CREW_PAGE_SENT: {
        "version": "1.0",
        "source_service": "adaptix-crewlink",
        "description": "A crew page has been sent",
        "channels": ["crewlink.page.updated"],
    },
    CREW_ASSIGNMENT_ACCEPTED: {
        "version": "1.0",
        "source_service": "adaptix-crewlink",
        "description": "Crew member accepted assignment",
        "channels": ["crewlink.page.updated"],
    },
    CREW_ASSIGNMENT_DECLINED: {
        "version": "1.0",
        "source_service": "adaptix-crewlink",
        "description": "Crew member declined assignment",
        "channels": ["crewlink.page.updated"],
    },
    # ePCR
    EPCR_REPORT_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-epcr",
        "description": "ePCR chart created",
        "channels": ["epcr.chart.updated"],
    },
    EPCR_REPORT_VALIDATED: {
        "version": "1.0",
        "source_service": "adaptix-epcr",
        "description": "ePCR chart passed NEMSIS validation",
        "channels": ["epcr.chart.updated"],
    },
    EPCR_BILLING_PACKET_GENERATED: {
        "version": "1.0",
        "source_service": "adaptix-epcr",
        "description": "Billing packet generated from ePCR chart",
        "channels": ["epcr.chart.updated", "billing.claim.updated"],
    },
    # Billing
    BILLING_CLAIM_GENERATED: {
        "version": "1.0",
        "source_service": "adaptix-billing",
        "description": "Billing claim generated",
        "channels": ["billing.claim.updated"],
    },
    BILLING_CLAIM_SUBMITTED: {
        "version": "1.0",
        "source_service": "adaptix-billing",
        "description": "Billing claim submitted to clearinghouse",
        "channels": ["billing.claim.updated"],
    },
    BILLING_CLAIM_STATUS_UPDATED: {
        "version": "1.0",
        "source_service": "adaptix-billing",
        "description": "Billing claim status updated from clearinghouse",
        "channels": ["billing.claim.updated"],
    },
    BILLING_ERA_IMPORTED: {
        "version": "1.0",
        "source_service": "adaptix-billing",
        "description": "835/ERA imported and payments posted",
        "channels": ["billing.claim.updated"],
    },
    # Fire
    FIRE_INCIDENT_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-fire",
        "description": "Fire incident created",
        "channels": ["fire.incident.updated"],
    },
    FIRE_LINKED_CARE_CHART_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-fire",
        "description": "Care chart linked to fire incident",
        "channels": ["fire.incident.updated", "epcr.chart.updated"],
    },
    # HEMS
    HEMS_TRANSPORT_REQUESTED: {
        "version": "1.0",
        "source_service": "adaptix-air",
        "description": "HEMS transport requested",
        "channels": ["cad.case.updated"],
    },
    HEMS_PILOT_GO_NO_GO_COMPLETED: {
        "version": "1.0",
        "source_service": "adaptix-air-pilot",
        "description": "Pilot go/no-go checklist completed",
        "channels": ["cad.case.updated"],
    },
    HEMS_LAUNCHED: {
        "version": "1.0",
        "source_service": "adaptix-air",
        "description": "HEMS mission launched",
        "channels": ["cad.tracking.updated"],
    },
    # Inventory
    INVENTORY_LOW_STOCK: {
        "version": "1.0",
        "source_service": "adaptix-inventory",
        "description": "Inventory item below threshold",
        "channels": [],
    },
    INVENTORY_DEPLETED: {
        "version": "1.0",
        "source_service": "adaptix-inventory",
        "description": "Inventory item fully depleted",
        "channels": [],
    },
    # Narcotics
    NARCOTIC_DISCREPANCY_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-narcotics",
        "description": "Controlled substance discrepancy recorded",
        "channels": [],
    },
    NARCOTIC_WASTE_WITNESSED: {
        "version": "1.0",
        "source_service": "adaptix-narcotics",
        "description": "Controlled substance waste witnessed",
        "channels": [],
    },
    # MDT
    MDT_STATUS_CHANGED: {
        "version": "1.0",
        "source_service": "adaptix-field",
        "description": "Unit status changed",
        "channels": ["mdt.status.updated", "cad.tracking.updated"],
    },
    MDT_UNIT_LOCATION_UPDATED: {
        "version": "1.0",
        "source_service": "adaptix-field",
        "description": "Unit GPS location updated",
        "channels": ["mdt.location.updated", "cad.tracking.updated"],
    },
    MDT_FATIGUE_RESTRICTION_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-field",
        "description": "Fatigue restriction placed on unit",
        "channels": ["mdt.status.updated"],
    },
    LIGHTS_SIRENS_INTERVAL_RECORDED: {
        "version": "1.0",
        "source_service": "adaptix-field",
        "description": "Lights and sirens interval recorded",
        "channels": [],
    },
    # Documents
    DOCUMENT_REQUIREMENT_MISSING: {
        "version": "1.0",
        "source_service": "adaptix-epcr",
        "description": "Required document missing from chart",
        "channels": [],
    },
    DOCUMENT_REQUIREMENT_SATISFIED: {
        "version": "1.0",
        "source_service": "adaptix-epcr",
        "description": "Required document satisfied",
        "channels": [],
    },
    # Core
    FOUNDER_POLICY_CHANGED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "Founder-level policy changed",
        "channels": ["founder.health.updated"],
    },
    USER_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "User account created",
        "channels": [],
    },
    USER_UPDATED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "User account updated",
        "channels": [],
    },
    TENANT_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "Tenant/agency created",
        "channels": [],
    },
    TENANT_UPDATED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "Tenant/agency updated",
        "channels": [],
    },
    ROLE_ASSIGNED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "Role assigned to user",
        "channels": [],
    },
    SESSION_CREATED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "User session created",
        "channels": [],
    },
    SESSION_REVOKED: {
        "version": "1.0",
        "source_service": "adaptix-core",
        "description": "User session revoked",
        "channels": [],
    },
}


# ─── Realtime Channels ────────────────────────────────────────────────────────
REALTIME_CHANNELS: Final[list] = [
    "cad.case.updated",
    "cad.tracking.updated",
    "crewlink.page.updated",
    "mdt.location.updated",
    "mdt.status.updated",
    "epcr.chart.updated",
    "billing.claim.updated",
    "fire.incident.updated",
    "voice.room.updated",
    "founder.health.updated",
]


def get_event_channels(event_type: str) -> list:
    """Return the realtime channels for a given event type."""
    entry = ALL_EVENTS.get(event_type)
    if entry:
        return entry.get("channels", [])
    return []


def is_registered_event(event_type: str) -> bool:
    """Return True if the event type is in the canonical registry."""
    return event_type in ALL_EVENTS
