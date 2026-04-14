"""Webhook domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class WebhookDeliveredEvent(DomainEvent):
    event_type: str = "webhook.delivered"
    entity_type: str = "webhook"

    webhook_id: str = ""
    endpoint_url: str = ""
    http_status: int = 0

class WebhookFailedEvent(DomainEvent):
    event_type: str = "webhook.failed"
    entity_type: str = "webhook"

    webhook_id: str = ""
    endpoint_url: str = ""
    error: str = ""
    attempt: int = 0

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("webhook.delivered", WebhookDeliveredEvent)
_catalog.register("webhook.failed", WebhookFailedEvent)
class WebhookRegisteredEvent(DomainEvent):
    event_type: str = "webhook.registered"
    entity_type: str = "webhook"
    webhook_id: str = ""
    endpoint_url: str = ""
    event_types: str = ""
    registered_by: str = ""
class WebhookUnregisteredEvent(DomainEvent):
    event_type: str = "webhook.unregistered"
    entity_type: str = "webhook"
    webhook_id: str = ""
    unregistered_by: str = ""
    unregistered_at: str = ""
_catalog.register("webhook.registered", WebhookRegisteredEvent)
_catalog.register("webhook.unregistered", WebhookUnregisteredEvent)
