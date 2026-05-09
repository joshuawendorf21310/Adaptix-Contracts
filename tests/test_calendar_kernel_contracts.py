"""Tests for the reduced-scope TransportLink/Workforce calendar kernel contracts."""

from __future__ import annotations

from datetime import UTC, datetime

from adaptix_contracts import schemas


def test_calendar_kernel_exports_are_public() -> None:
    required = {
        "AdaptixCalendarProduct",
        "AdaptixCalendarEventStatus",
        "AdaptixCalendarEvent",
        "AdaptixCalendarResourceKind",
        "AdaptixCalendarResource",
        "AdaptixCalendarConflictReason",
        "AdaptixCalendarConflict",
        "AdaptixCalendarAuditAction",
        "AdaptixCalendarAuditEvent",
    }

    for name in required:
        assert name in schemas.__all__
        assert hasattr(schemas, name)


def test_calendar_event_contract_supports_aliases() -> None:
    event = schemas.AdaptixCalendarEvent(
        id="event-1",
        tenantId="tenant-1",
        product="transportlink",
        eventType="transport",
        sourceId="trip-1",
        sourceType="transport_request",
        title="Transport readiness lane",
        startAt=datetime(2026, 5, 8, 14, 0, tzinfo=UTC),
        endAt=datetime(2026, 5, 8, 15, 0, tzinfo=UTC),
        timezone="America/Chicago",
        resourceIds=["unit-12"],
        status="scheduled",
        locked=False,
        version=1,
        metadata={"readinessStatus": "partial"},
    )

    dumped = event.model_dump(by_alias=True)

    assert dumped["tenantId"] == "tenant-1"
    assert dumped["eventType"] == "transport"
    assert dumped["resourceIds"] == ["unit-12"]


def test_calendar_audit_contract_keeps_traceability_fields() -> None:
    audit = schemas.AdaptixCalendarAuditEvent(
        id="audit-1",
        tenantId="tenant-1",
        product="workforce",
        eventId="shift-1",
        actorId="supervisor-9",
        action="published",
        correlationId="corr-1",
        idempotencyKey="idem-1",
        occurredAt=datetime(2026, 5, 8, 16, 0, tzinfo=UTC),
        details={"status": "published"},
    )

    assert audit.product.value == "workforce"
    assert audit.action.value == "published"
    assert audit.correlation_id == "corr-1"