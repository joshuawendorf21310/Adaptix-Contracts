"""Fire and NERIS domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class FireIncidentCreatedEvent(DomainEvent):
    event_type: str = "fire.incident.created"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    incident_type: str = ""
    address: str = ""


class FireIncidentStatusChangedEvent(DomainEvent):
    event_type: str = "fire.incident.status_changed"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    previous_status: str = ""
    new_status: str = ""


class FireIncidentClosedEvent(DomainEvent):
    event_type: str = "fire.incident.closed"
    entity_type: str = "fire_incident"

    fire_incident_id: str = ""
    disposition: str = ""


class NerisSubmissionCreatedEvent(DomainEvent):
    event_type: str = "neris.submission.created"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    fire_incident_id: str = ""
    state_code: str = ""


class NerisSubmissionAcknowledgedEvent(DomainEvent):
    event_type: str = "neris.submission.acknowledged"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    acknowledged_at: str = ""


class NerisSubmissionRejectedEvent(DomainEvent):
    event_type: str = "neris.submission.rejected"
    entity_type: str = "neris_submission"

    submission_id: str = ""
    rejection_reason: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("fire.incident.created", FireIncidentCreatedEvent)
_catalog.register("fire.incident.status_changed", FireIncidentStatusChangedEvent)
_catalog.register("fire.incident.closed", FireIncidentClosedEvent)
_catalog.register("neris.submission.created", NerisSubmissionCreatedEvent)
_catalog.register("neris.submission.acknowledged", NerisSubmissionAcknowledgedEvent)
_catalog.register("neris.submission.rejected", NerisSubmissionRejectedEvent)
