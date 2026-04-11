"""Workforce, scheduling, and training domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class SchedulingShiftCreatedEvent(DomainEvent):
    event_type: str = "scheduling.shift.created"
    entity_type: str = "shift"

    shift_id: str = ""
    unit_id: str = ""
    start_time: str = ""
    end_time: str = ""


class SchedulingShiftFilledEvent(DomainEvent):
    event_type: str = "scheduling.shift.filled"
    entity_type: str = "shift"

    shift_id: str = ""
    user_id: str = ""


class SchedulingShiftMissedEvent(DomainEvent):
    event_type: str = "scheduling.shift.missed"
    entity_type: str = "shift"

    shift_id: str = ""


class PersonnelCreatedEvent(DomainEvent):
    event_type: str = "personnel.created"
    entity_type: str = "personnel"

    user_id: str = ""
    first_name: str = ""
    last_name: str = ""
    role: str = ""


class PersonnelDeactivatedEvent(DomainEvent):
    event_type: str = "personnel.deactivated"
    entity_type: str = "personnel"

    user_id: str = ""
    reason: str = ""


class TrainingCompletedEvent(DomainEvent):
    event_type: str = "training.completed"
    entity_type: str = "training"

    training_id: str = ""
    user_id: str = ""
    course_name: str = ""
    completed_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("scheduling.shift.created", SchedulingShiftCreatedEvent)
_catalog.register("scheduling.shift.filled", SchedulingShiftFilledEvent)
_catalog.register("scheduling.shift.missed", SchedulingShiftMissedEvent)
_catalog.register("personnel.created", PersonnelCreatedEvent)
_catalog.register("personnel.deactivated", PersonnelDeactivatedEvent)
_catalog.register("training.completed", TrainingCompletedEvent)
