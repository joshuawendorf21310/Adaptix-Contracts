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
