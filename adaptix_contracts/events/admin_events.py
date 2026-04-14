"""Admin domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class InvestorFunnelStageChangedEvent(DomainEvent):
    event_type: str = "investor.funnel.stage_changed"
    entity_type: str = "investor"

    contact_id: str = ""
    previous_stage: str = ""
    new_stage: str = ""
    changed_at: str = ""


class InvestorIntakeApprovedEvent(DomainEvent):
    event_type: str = "investor.intake.approved"
    entity_type: str = "investor"

    intake_id: str = ""
    approved_by: str = ""
    approved_at: str = ""


class InvestorIntakeRejectedEvent(DomainEvent):
    event_type: str = "investor.intake.rejected"
    entity_type: str = "investor"

    intake_id: str = ""
    rejection_reason: str = ""
    rejected_by: str = ""


class InvestorIntakeSubmittedEvent(DomainEvent):
    event_type: str = "investor.intake.submitted"
    entity_type: str = "investor"

    intake_id: str = ""
    company_name: str = ""
    contact_email: str = ""
    submitted_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("investor.funnel.stage_changed", InvestorFunnelStageChangedEvent)
_catalog.register("investor.intake.approved", InvestorIntakeApprovedEvent)
_catalog.register("investor.intake.rejected", InvestorIntakeRejectedEvent)
_catalog.register("investor.intake.submitted", InvestorIntakeSubmittedEvent)
