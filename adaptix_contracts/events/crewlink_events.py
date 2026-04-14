"""CrewLink domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from pydantic import Field

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class CrewlinkAlertCreatedEvent(DomainEvent):
    event_type: str = "crewlink.alert.created"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""
    page_type: str = ""
    priority: str = ""
    recipients: list[str] = Field(default_factory=list)

class CrewlinkAlertAcknowledgedEvent(DomainEvent):
    event_type: str = "crewlink.alert.acknowledged"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""
    user_id: str = ""
    device_id: str = ""
    acknowledged_at: str = ""

class CrewlinkAlertExpiredEvent(DomainEvent):
    event_type: str = "crewlink.alert.expired"
    entity_type: str = "crewlink_alert"

    alert_id: str = ""

class CrewlinkAssignmentAcceptedEvent(DomainEvent):
    event_type: str = "crewlink.assignment.accepted"
    entity_type: str = "crewlink_assignment"

    assignment_id: str = ""
    incident_id: str = ""
    user_id: str = ""
    unit_id: str = ""

class CrewlinkAssignmentDeclinedEvent(DomainEvent):
    event_type: str = "crewlink.assignment.declined"
    entity_type: str = "crewlink_assignment"

    assignment_id: str = ""
    user_id: str = ""
    reason: str = ""

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("crewlink.alert.created", CrewlinkAlertCreatedEvent)
_catalog.register("crewlink.alert.acknowledged", CrewlinkAlertAcknowledgedEvent)
_catalog.register("crewlink.alert.expired", CrewlinkAlertExpiredEvent)
_catalog.register("crewlink.assignment.accepted", CrewlinkAssignmentAcceptedEvent)
_catalog.register("crewlink.assignment.declined", CrewlinkAssignmentDeclinedEvent)
class CrewlinkAvailabilityUpdatedEvent(DomainEvent):
    event_type: str = "crewlink.availability.updated"
    entity_type: str = "crewlink"
    user_id: str = ""
    availability_status: str = ""
    updated_at: str = ""
class CrewlinkCrewMemberCheckedinEvent(DomainEvent):
    event_type: str = "crewlink.crew_member.checkedin"
    entity_type: str = "crewlink"
    user_id: str = ""
    unit_id: str = ""
    checkin_time: str = ""
class CrewlinkCrewMemberCheckedoutEvent(DomainEvent):
    event_type: str = "crewlink.crew_member.checkedout"
    entity_type: str = "crewlink"
    user_id: str = ""
    unit_id: str = ""
    checkout_time: str = ""
class CrewlinkDeviceRegisteredEvent(DomainEvent):
    event_type: str = "crewlink.device.registered"
    entity_type: str = "crewlink"
    device_id: str = ""
    user_id: str = ""
    push_token: str = ""
    platform: str = ""
class CrewlinkDeviceUnregisteredEvent(DomainEvent):
    event_type: str = "crewlink.device.unregistered"
    entity_type: str = "crewlink"
    device_id: str = ""
    user_id: str = ""
class CrewlinkPageDeliveredEvent(DomainEvent):
    event_type: str = "crewlink.page.delivered"
    entity_type: str = "crewlink"
    alert_id: str = ""
    user_id: str = ""
    device_id: str = ""
    delivered_at: str = ""
class CrewlinkPageFailedEvent(DomainEvent):
    event_type: str = "crewlink.page.failed"
    entity_type: str = "crewlink"
    alert_id: str = ""
    user_id: str = ""
    device_id: str = ""
    failure_reason: str = ""
class CrewlinkRosterPublishedEvent(DomainEvent):
    event_type: str = "crewlink.roster.published"
    entity_type: str = "crewlink"
    roster_id: str = ""
    shift_date: str = ""
    published_by: str = ""
    published_at: str = ""
class CrewlinkShiftTradeApprovedEvent(DomainEvent):
    event_type: str = "crewlink.shift.trade_approved"
    entity_type: str = "crewlink"
    trade_id: str = ""
    approved_by: str = ""
    approved_at: str = ""
class CrewlinkShiftTradeRequestedEvent(DomainEvent):
    event_type: str = "crewlink.shift.trade_requested"
    entity_type: str = "crewlink"
    trade_id: str = ""
    requesting_user: str = ""
    shift_id: str = ""
    requested_at: str = ""
class CrewlinkStaffingRequestCreatedEvent(DomainEvent):
    event_type: str = "crewlink.staffing.request_created"
    entity_type: str = "crewlink"
    request_id: str = ""
    shift_id: str = ""
    position: str = ""
    requested_at: str = ""
class CrewlinkStaffingRequestFilledEvent(DomainEvent):
    event_type: str = "crewlink.staffing.request_filled"
    entity_type: str = "crewlink"
    request_id: str = ""
    user_id: str = ""
    filled_at: str = ""
_catalog.register("crewlink.availability.updated", CrewlinkAvailabilityUpdatedEvent)
_catalog.register("crewlink.crew_member.checkedin", CrewlinkCrewMemberCheckedinEvent)
_catalog.register("crewlink.crew_member.checkedout", CrewlinkCrewMemberCheckedoutEvent)
_catalog.register("crewlink.device.registered", CrewlinkDeviceRegisteredEvent)
_catalog.register("crewlink.device.unregistered", CrewlinkDeviceUnregisteredEvent)
_catalog.register("crewlink.page.delivered", CrewlinkPageDeliveredEvent)
_catalog.register("crewlink.page.failed", CrewlinkPageFailedEvent)
_catalog.register("crewlink.roster.published", CrewlinkRosterPublishedEvent)
_catalog.register("crewlink.shift.trade_approved", CrewlinkShiftTradeApprovedEvent)
_catalog.register("crewlink.shift.trade_requested", CrewlinkShiftTradeRequestedEvent)
_catalog.register("crewlink.staffing.request_created", CrewlinkStaffingRequestCreatedEvent)
_catalog.register("crewlink.staffing.request_filled", CrewlinkStaffingRequestFilledEvent)
