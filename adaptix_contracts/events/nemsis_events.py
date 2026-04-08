"""NEMSIS Auto-Export Pipeline domain events.

Seven typed event models covering the full export lifecycle:
  lock → compliance check → queue → validate → submit → accept/reject

All inherit from DomainEvent and are registered with EventCatalog at import time.
"""

from __future__ import annotations

import uuid

from pydantic import Field

from .domain_event import DomainEvent
from .event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event Models
# ---------------------------------------------------------------------------


class EpcrLockedEvent(DomainEvent):
    """Fired when an ePCR chart is locked and ready for export processing."""

    event_type: str = Field(default="nemsis.epcr.locked", frozen=True)
    entity_type: str = Field(default="epcr", frozen=True)

    # domain payload
    lock_reason: str = Field(default="manual", description="Lock trigger: manual | auto | qa_complete")


class ComplianceCheckCompleted(DomainEvent):
    """Fired after the enforcement / compliance check finishes for an ePCR."""

    event_type: str = Field(default="nemsis.compliance.check_completed", frozen=True)
    entity_type: str = Field(default="epcr", frozen=True)

    is_compliant: bool = Field(..., description="True when record passes all checks")
    blocker_count: int = Field(default=0, description="Number of active blockers")
    readiness_state: str = Field(default="unknown", description="Resulting readiness state")


class ExportQueuedEvent(DomainEvent):
    """Fired when a compliant ePCR is queued for NEMSIS export."""

    event_type: str = Field(default="nemsis.export.queued", frozen=True)
    entity_type: str = Field(default="epcr", frozen=True)

    export_id: uuid.UUID | None = Field(default=None, description="ID of the created NEMSISExport row")
    export_format: str = Field(default="xml", description="Export format: xml | json")


class ExportValidatedEvent(DomainEvent):
    """Fired after an export passes XSD/Schematron strict validation."""

    event_type: str = Field(default="nemsis.export.validated", frozen=True)
    entity_type: str = Field(default="export", frozen=True)

    export_id: uuid.UUID = Field(..., description="ID of the validated NEMSISExport")
    validation_passed: bool = Field(default=True)
    error_count: int = Field(default=0)
    warning_count: int = Field(default=0)


class ExportSubmittedEvent(DomainEvent):
    """Fired when an export is submitted to a state NEMSIS endpoint."""

    event_type: str = Field(default="nemsis.export.submitted", frozen=True)
    entity_type: str = Field(default="export", frozen=True)

    export_id: uuid.UUID = Field(..., description="ID of the submitted NEMSISExport")
    submission_method: str = Field(default="api", description="api | sftp | manual")
    submission_id: str | None = Field(default=None, description="External receipt ID")


class ExportAcceptedEvent(DomainEvent):
    """Fired when a state endpoint accepts the submitted export."""

    event_type: str = Field(default="nemsis.export.accepted", frozen=True)
    entity_type: str = Field(default="export", frozen=True)

    export_id: uuid.UUID = Field(..., description="ID of the accepted NEMSISExport")
    state_reference: str | None = Field(default=None, description="State-provided reference")


class ExportRejectedEvent(DomainEvent):
    """Fired when a state endpoint rejects the submitted export."""

    event_type: str = Field(default="nemsis.export.rejected", frozen=True)
    entity_type: str = Field(default="export", frozen=True)

    export_id: uuid.UUID | None = Field(default=None, description="ID of the rejected NEMSISExport")
    rejection_count: int = Field(default=0, description="Number of rejection items parsed")
    rejection_codes: list[str] = Field(default_factory=list, description="Error codes from rejection XML")


# ---------------------------------------------------------------------------
# Catalog Registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()

_catalog.register("nemsis.epcr.locked", EpcrLockedEvent)
_catalog.register("nemsis.compliance.check_completed", ComplianceCheckCompleted)
_catalog.register("nemsis.export.queued", ExportQueuedEvent)
_catalog.register("nemsis.export.validated", ExportValidatedEvent)
_catalog.register("nemsis.export.submitted", ExportSubmittedEvent)
_catalog.register("nemsis.export.accepted", ExportAcceptedEvent)
_catalog.register("nemsis.export.rejected", ExportRejectedEvent)
