"""Communications domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class CommunicationConsentRecordedEvent(DomainEvent):
    event_type: str = "communication.consent.recorded"
    entity_type: str = "communication"

    user_id: str = ""
    consent_type: str = ""
    granted: str = ""
    recorded_at: str = ""


class CommunicationDeliveryReceiptReceivedEvent(DomainEvent):
    event_type: str = "communication.delivery_receipt.received"
    entity_type: str = "communication"

    message_id: str = ""
    delivery_status: str = ""
    provider_id: str = ""
    received_at: str = ""


class CommunicationEscalationTriggeredEvent(DomainEvent):
    event_type: str = "communication.escalation.triggered"
    entity_type: str = "communication"

    message_id: str = ""
    escalation_level: int = 0
    escalated_to: str = ""
    triggered_at: str = ""


class CommunicationInboundReceivedEvent(DomainEvent):
    event_type: str = "communication.inbound.received"
    entity_type: str = "communication"

    message_id: str = ""
    sender: str = ""
    channel: str = ""
    content: str = ""
    received_at: str = ""


class CommunicationOutboundDeliveredEvent(DomainEvent):
    event_type: str = "communication.outbound.delivered"
    entity_type: str = "communication"

    message_id: str = ""
    delivered_at: str = ""


class CommunicationOutboundFailedEvent(DomainEvent):
    event_type: str = "communication.outbound.failed"
    entity_type: str = "communication"

    message_id: str = ""
    failure_reason: str = ""


class CommunicationOutboundSentEvent(DomainEvent):
    event_type: str = "communication.outbound.sent"
    entity_type: str = "communication"

    message_id: str = ""
    recipient: str = ""
    channel: str = ""
    template_id: str = ""
    sent_at: str = ""


class CommunicationPreferenceUpdatedEvent(DomainEvent):
    event_type: str = "communication.preference.updated"
    entity_type: str = "communication"

    user_id: str = ""
    channel: str = ""
    opt_in: str = ""
    updated_at: str = ""


class CommunicationTemplateCreatedEvent(DomainEvent):
    event_type: str = "communication.template.created"
    entity_type: str = "communication"

    template_id: str = ""
    template_name: str = ""
    channel: str = ""
    created_by: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("communication.consent.recorded", CommunicationConsentRecordedEvent)
_catalog.register("communication.delivery_receipt.received", CommunicationDeliveryReceiptReceivedEvent)
_catalog.register("communication.escalation.triggered", CommunicationEscalationTriggeredEvent)
_catalog.register("communication.inbound.received", CommunicationInboundReceivedEvent)
_catalog.register("communication.outbound.delivered", CommunicationOutboundDeliveredEvent)
_catalog.register("communication.outbound.failed", CommunicationOutboundFailedEvent)
_catalog.register("communication.outbound.sent", CommunicationOutboundSentEvent)
_catalog.register("communication.preference.updated", CommunicationPreferenceUpdatedEvent)
_catalog.register("communication.template.created", CommunicationTemplateCreatedEvent)
