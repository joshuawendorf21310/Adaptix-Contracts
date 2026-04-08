"""
Adaptix EventBridge-based Event System

This module provides a production-ready event infrastructure for the unified operational graph,
enabling real-time event-driven architecture across all EMS modules.
"""

from core_app.events.domain_event import DomainEvent
from core_app.events.event_bus import EventBridgeClient, get_event_bus_client
from core_app.events.event_catalog import EventCatalog
from core_app.events.event_publisher import EventPublisher, publish_batch_events, publish_event
from core_app.events.event_schema import (
    BaseEvent,
    BillingClaimGenerated,
    BillingClaimSubmitted,
    CrewAssignmentAccepted,
    CrewAssignmentAcknowledgedEvent,
    CrewAssignmentCreatedEvent,
    CrewAssignmentStatusChangedEvent,
    CrewPageSent,
    EpcrReportValidated,
    EventType,
    FireIncidentCreated,
    HemsLaunched,
    HemsTransportRequested,
    IncidentCreated,
    IncidentStatusChanged,
    InventoryLowStock,
    MdtStatusChanged,
    NarcoticDiscrepancy,
    SchedulePublished,
    ShiftAssigned,
    TransportPushedToCAD,
    TransportRequestCreated,
    TransportScheduled,
)

__all__ = [
    # Event Bus Client
    "EventBridgeClient",
    "get_event_bus_client",
    # Event Publisher
    "EventPublisher",
    "publish_event",
    "publish_batch_events",
    # Event Types Enum
    "EventType",
    # Base Event Schema
    "BaseEvent",
    # Transport Events
    "TransportRequestCreated",
    "TransportScheduled",
    "TransportPushedToCAD",
    # Crew Events
    "CrewPageSent",
    "CrewAssignmentAccepted",
    "CrewAssignmentCreatedEvent",
    "CrewAssignmentAcknowledgedEvent",
    "CrewAssignmentStatusChangedEvent",
    # Incident Events
    "IncidentCreated",
    "IncidentStatusChanged",
    # ePCR Events
    "EpcrReportValidated",
    # Billing Events
    "BillingClaimGenerated",
    "BillingClaimSubmitted",
    # Fire Events
    "FireIncidentCreated",
    # HEMS Events
    "HemsTransportRequested",
    "HemsLaunched",
    # Scheduling Events
    "SchedulePublished",
    "ShiftAssigned",
    # Inventory Events
    "InventoryLowStock",
    "NarcoticDiscrepancy",
    # MDT Events
    "MdtStatusChanged",
    # Domain Event System (typed pub/sub)
    "DomainEvent",
    "EventCatalog",
]
