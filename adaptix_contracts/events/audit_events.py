"""Audit domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class AuditEntryCreatedEvent(DomainEvent):
    event_type: str = "audit.entry.created"
    entity_type: str = "audit_entry"

    entry_id: str = ""
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("audit.entry.created", AuditEntryCreatedEvent)
class AuditAccessTrackedEvent(DomainEvent):
    event_type: str = "audit.access.tracked"
    entity_type: str = "audit"
    resource_type: str = ""
    resource_id: str = ""

    access_type: str = ""
class AuditExportCompletedEvent(DomainEvent):
    event_type: str = "audit.export.completed"
    entity_type: str = "audit"
    export_id: str = ""
    record_count: int = 0
    file_url: str = ""
class AuditExportRequestedEvent(DomainEvent):
    event_type: str = "audit.export.requested"
    entity_type: str = "audit"
    export_id: str = ""

    requested_by: str = ""
    date_range: str = ""
class AuditMutationTrackedEvent(DomainEvent):
    event_type: str = "audit.mutation.tracked"
    entity_type: str = "audit"
    entity_type: str = ""

    mutation_type: str = ""

    changes: str = ""
class AuditRetentionEnforcedEvent(DomainEvent):
    event_type: str = "audit.retention.enforced"
    entity_type: str = "audit"

    records_purged: str = ""
    retention_days: str = ""
class AuditTraceCompletedEvent(DomainEvent):
    event_type: str = "audit.trace.completed"
    entity_type: str = "audit"
    trace_id: str = ""
    event_count: int = 0
    duration_ms: str = ""
class AuditTraceStartedEvent(DomainEvent):
    event_type: str = "audit.trace.started"
    entity_type: str = "audit"
    trace_id: str = ""

    initiating_event: str = ""
_catalog.register("audit.access.tracked", AuditAccessTrackedEvent)
_catalog.register("audit.export.completed", AuditExportCompletedEvent)
_catalog.register("audit.export.requested", AuditExportRequestedEvent)
_catalog.register("audit.mutation.tracked", AuditMutationTrackedEvent)
_catalog.register("audit.retention.enforced", AuditRetentionEnforcedEvent)
_catalog.register("audit.trace.completed", AuditTraceCompletedEvent)
_catalog.register("audit.trace.started", AuditTraceStartedEvent)
