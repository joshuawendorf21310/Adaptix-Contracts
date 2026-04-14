"""Integration domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class FhirBundleSentEvent(DomainEvent):
    event_type: str = "fhir.bundle.sent"
    entity_type: str = "fhir"

    bundle_id: str = ""
    destination: str = ""
    resource_count: int = 0
    sent_at: str = ""


class FhirResourceCreatedEvent(DomainEvent):
    event_type: str = "fhir.resource.created"
    entity_type: str = "fhir"

    resource_id: str = ""
    resource_type: str = ""
    source_entity_id: str = ""
    created_at: str = ""


class FhirResourceUpdatedEvent(DomainEvent):
    event_type: str = "fhir.resource.updated"
    entity_type: str = "fhir"

    resource_id: str = ""
    resource_type: str = ""
    updated_at: str = ""


class Hl7AckSentEvent(DomainEvent):
    event_type: str = "hl7.ack.sent"
    entity_type: str = "hl7"

    message_id: str = ""
    ack_code: str = ""
    sent_at: str = ""


class Hl7MessageReceivedEvent(DomainEvent):
    event_type: str = "hl7.message.received"
    entity_type: str = "hl7"

    message_id: str = ""
    message_type: str = ""
    source: str = ""
    received_at: str = ""


class Hl7MessageSentEvent(DomainEvent):
    event_type: str = "hl7.message.sent"
    entity_type: str = "hl7"

    message_id: str = ""
    message_type: str = ""
    destination: str = ""
    sent_at: str = ""


class IntegrationConnectedEvent(DomainEvent):
    event_type: str = "integration.connected"
    entity_type: str = "integration"

    integration_id: str = ""
    integration_type: str = ""
    tenant_id: str = ""
    connected_at: str = ""


class IntegrationDisconnectedEvent(DomainEvent):
    event_type: str = "integration.disconnected"
    entity_type: str = "integration"

    integration_id: str = ""
    integration_type: str = ""
    disconnected_at: str = ""


class IntegrationEmpiLookupRequestedEvent(DomainEvent):
    event_type: str = "integration.empi.lookup.requested"
    entity_type: str = "integration"

    lookup_id: str = ""
    patient_demographics: str = ""
    requested_at: str = ""


class IntegrationEmpiMatchFoundEvent(DomainEvent):
    event_type: str = "integration.empi.match.found"
    entity_type: str = "integration"

    lookup_id: str = ""
    match_confidence: str = ""
    matched_patient_id: str = ""


class IntegrationFhirBundleCreatedEvent(DomainEvent):
    event_type: str = "integration.fhir.bundle.created"
    entity_type: str = "integration"

    bundle_id: str = ""
    bundle_type: str = ""
    resource_count: int = 0
    created_at: str = ""


class IntegrationFhirResourceCreatedEvent(DomainEvent):
    event_type: str = "integration.fhir.resource.created"
    entity_type: str = "integration"

    resource_id: str = ""
    resource_type: str = ""
    created_at: str = ""


class IntegrationFhirResourceUpdatedEvent(DomainEvent):
    event_type: str = "integration.fhir.resource.updated"
    entity_type: str = "integration"

    resource_id: str = ""
    resource_type: str = ""
    updated_at: str = ""


class IntegrationHl7AckReceivedEvent(DomainEvent):
    event_type: str = "integration.hl7.ack.received"
    entity_type: str = "integration"

    message_id: str = ""
    ack_code: str = ""
    received_at: str = ""


class IntegrationHl7MessageReceivedEvent(DomainEvent):
    event_type: str = "integration.hl7.message.received"
    entity_type: str = "integration"

    message_id: str = ""
    message_type: str = ""
    source_system: str = ""
    received_at: str = ""


class IntegrationHl7MessageSentEvent(DomainEvent):
    event_type: str = "integration.hl7.message.sent"
    entity_type: str = "integration"

    message_id: str = ""
    message_type: str = ""
    destination_system: str = ""
    sent_at: str = ""


class IntegrationSyncCompletedEvent(DomainEvent):
    event_type: str = "integration.sync.completed"
    entity_type: str = "integration"

    integration_id: str = ""
    sync_type: str = ""
    records_synced: str = ""
    completed_at: str = ""


class IntegrationSyncFailedEvent(DomainEvent):
    event_type: str = "integration.sync.failed"
    entity_type: str = "integration"

    integration_id: str = ""
    sync_type: str = ""
    error_message: str = ""


class IntegrationWebhookFailedEvent(DomainEvent):
    event_type: str = "integration.webhook.failed"
    entity_type: str = "integration"

    webhook_id: str = ""
    event_type: str = ""
    failure_reason: str = ""
    failed_at: str = ""


class IntegrationWebhookInvokedEvent(DomainEvent):
    event_type: str = "integration.webhook.invoked"
    entity_type: str = "integration"

    webhook_id: str = ""
    event_type: str = ""
    target_url: str = ""
    invoked_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("fhir.bundle.sent", FhirBundleSentEvent)
_catalog.register("fhir.resource.created", FhirResourceCreatedEvent)
_catalog.register("fhir.resource.updated", FhirResourceUpdatedEvent)
_catalog.register("hl7.ack.sent", Hl7AckSentEvent)
_catalog.register("hl7.message.received", Hl7MessageReceivedEvent)
_catalog.register("hl7.message.sent", Hl7MessageSentEvent)
_catalog.register("integration.connected", IntegrationConnectedEvent)
_catalog.register("integration.disconnected", IntegrationDisconnectedEvent)
_catalog.register("integration.empi.lookup.requested", IntegrationEmpiLookupRequestedEvent)
_catalog.register("integration.empi.match.found", IntegrationEmpiMatchFoundEvent)
_catalog.register("integration.fhir.bundle.created", IntegrationFhirBundleCreatedEvent)
_catalog.register("integration.fhir.resource.created", IntegrationFhirResourceCreatedEvent)
_catalog.register("integration.fhir.resource.updated", IntegrationFhirResourceUpdatedEvent)
_catalog.register("integration.hl7.ack.received", IntegrationHl7AckReceivedEvent)
_catalog.register("integration.hl7.message.received", IntegrationHl7MessageReceivedEvent)
_catalog.register("integration.hl7.message.sent", IntegrationHl7MessageSentEvent)
_catalog.register("integration.sync.completed", IntegrationSyncCompletedEvent)
_catalog.register("integration.sync.failed", IntegrationSyncFailedEvent)
_catalog.register("integration.webhook.failed", IntegrationWebhookFailedEvent)
_catalog.register("integration.webhook.invoked", IntegrationWebhookInvokedEvent)
