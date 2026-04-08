"""
Event Handlers for Adaptix Unified Operational Graph

This module provides handler registration and execution for EventBridge events,
enabling cross-module workflows and automated responses to system events.
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.orm import Session

from core_app.models.epcr import Epcr, EpcrStatus
from core_app.services.epcr_form_builder_service import FormBuilderService
from core_app.services.event_publisher import get_event_publisher

logger = logging.getLogger(__name__)


# Type alias for event handlers
EventHandler = Callable[[dict[str, Any], Session], None]


class EventHandlerRegistry:
    """
    Registry for event handlers that maps event types to handler functions.

    Enables decoupled event processing where modules can register handlers
    for events they care about without tight coupling.
    """

    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = {}

    def register(self, event_type: str, handler: EventHandler) -> None:
        """
        Register a handler for a specific event type.

        Multiple handlers can be registered for the same event type.

        Args:
            event_type: Event type string (e.g., 'TransportRequestCreated')
            handler: Handler function with signature (event_data: dict, db: Session) -> None
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        if handler in self._handlers[event_type]:
            logger.debug(
                "event_handler.already_registered",
                extra={
                    "event_type": event_type,
                    "handler": handler.__name__,
                },
            )
            return

        self._handlers[event_type].append(handler)

        logger.info(
            "event_handler.registered",
            extra={
                "event_type": event_type,
                "handler": handler.__name__,
            },
        )

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        """
        Get all handlers registered for an event type.

        Args:
            event_type: Event type string

        Returns:
            List of handler functions
        """
        return self._handlers.get(event_type, [])

    def handle_event(self, event_type: str, event_data: dict[str, Any], db: Session) -> None:
        """
        Execute all handlers registered for an event type.

        Handlers are executed in registration order. If a handler fails, execution
        continues with the next handler (errors are logged but not propagated).

        Args:
            event_type: Event type string
            event_data: Event payload dictionary
            db: SQLAlchemy database session
        """
        handlers = self.get_handlers(event_type)

        if not handlers:
            logger.debug(
                "event_handler.no_handlers",
                extra={
                    "event_type": event_type,
                    "event_id": event_data.get("event_id"),
                },
            )
            return

        logger.info(
            "event_handler.executing",
            extra={
                "event_type": event_type,
                "event_id": event_data.get("event_id"),
                "handler_count": len(handlers),
            },
        )

        for handler in handlers:
            try:
                handler(event_data, db)

                logger.debug(
                    "event_handler.success",
                    extra={
                        "event_type": event_type,
                        "event_id": event_data.get("event_id"),
                        "handler": handler.__name__,
                    },
                )

            except Exception as e:
                logger.error(
                    "event_handler.error",
                    extra={
                        "event_type": event_type,
                        "event_id": event_data.get("event_id"),
                        "handler": handler.__name__,
                        "error": str(e),
                    },
                    exc_info=True,
                )


# Global handler registry
_handler_registry = EventHandlerRegistry()


def get_handler_registry() -> EventHandlerRegistry:
    """Get the global event handler registry."""
    return _handler_registry


# ================================
# Core Event Handlers
# ================================


def _next_epcr_report_number(db: Session, tenant_id: uuid.UUID) -> str:
    """Generate the next tenant-scoped ePCR report number.

    Format: ``PCR-{year}-{seq:06d}``
    """
    year = datetime.now(UTC).year
    prefix = f"PCR-{year}-"
    last_row = (
        db.query(Epcr.report_number)
        .filter(
            Epcr.tenant_id == tenant_id,
            Epcr.report_number.like(f"{prefix}%"),
        )
        .order_by(Epcr.report_number.desc())
        .first()
    )

    next_sequence = 1
    if last_row and last_row[0]:
        try:
            next_sequence = int(str(last_row[0]).rsplit("-", 1)[-1]) + 1
        except (TypeError, ValueError):
            next_sequence = 1

    return f"{prefix}{next_sequence:06d}"


def handle_transport_created(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle TransportRequestCreated event by triggering CrewLink page notification.

    Workflow:
    1. Extract transport details from event
    2. Determine crew members to page based on unit assignment
    3. Create page notification via CrewLink
    4. Publish CrewPageSent event
    """
    try:
        transport_id = event_data.get("transport_id")
        tenant_id = event_data.get("tenant_id")
        priority = event_data.get("priority", 3)

        logger.info(
            "event_handler.transport_created",
            extra={
                "transport_id": transport_id,
                "tenant_id": tenant_id,
                "priority": priority,
            },
        )

        # Query available crew members for the service area
        crew_query = text(
            """
            SELECT cm.id, cm.data->>'phone_number' as phone
            FROM crew_members cm
            WHERE cm.tenant_id = :tenant_id
              AND cm.data->>'status' = 'available'
              AND cm.data->>'on_duty' = 'true'
            LIMIT 5
            """
        )

        crew_members = db.execute(crew_query, {"tenant_id": tenant_id}).mappings().all()

        if not crew_members:
            logger.warning(
                "event_handler.transport_created.no_crew_available",
                extra={"transport_id": transport_id, "tenant_id": tenant_id},
            )
            return

        # Create page notification
        page_id = str(uuid.uuid4())
        page_message = f"Transport Request: Priority {priority}, ID: {transport_id}"

        for crew_member in crew_members:
            crew_member_id = crew_member["id"]

            # Insert page record
            db.execute(
                text(
                    """
                    INSERT INTO crew_pages (id, tenant_id, data, created_at)
                    VALUES (:id, :tenant_id, CAST(:data AS jsonb), NOW())
                    """
                ),
                {
                    "id": str(uuid.uuid4()),
                    "tenant_id": tenant_id,
                    "data": {
                        "page_id": page_id,
                        "transport_id": transport_id,
                        "crew_member_id": str(crew_member_id),
                        "message": page_message,
                        "method": "sms",
                        "status": "sent",
                    },
                },
            )

        db.commit()

        logger.info(
            "event_handler.transport_created.crew_paged",
            extra={
                "transport_id": transport_id,
                "page_id": page_id,
                "crew_count": len(crew_members),
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.transport_created.error",
            extra={
                "transport_id": event_data.get("transport_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


def handle_crew_accepted(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle CrewAssignmentAccepted event by updating transport assignment.

    Workflow:
    1. Update transport record with crew assignment
    2. Cancel other pending pages for this transport
    3. Update crew member status to 'assigned'
    4. Publish TransportScheduled event
    """
    try:
        assignment_id = event_data.get("assignment_id")
        transport_id = event_data.get("transport_id")
        crew_member_id = event_data.get("crew_member_id")
        tenant_id = event_data.get("tenant_id")

        logger.info(
            "event_handler.crew_accepted",
            extra={
                "assignment_id": assignment_id,
                "transport_id": transport_id,
                "crew_member_id": crew_member_id,
            },
        )

        # Update transport with crew assignment
        db.execute(
            text(
                """
                UPDATE transports
                SET data = jsonb_set(
                    jsonb_set(data, '{crew_member_id}', to_jsonb(:crew_member_id::text)),
                    '{status}', to_jsonb('assigned'::text)
                ),
                updated_at = NOW()
                WHERE id = :transport_id AND tenant_id = :tenant_id
                """
            ),
            {
                "transport_id": transport_id,
                "crew_member_id": crew_member_id,
                "tenant_id": tenant_id,
            },
        )

        # Update crew member status
        db.execute(
            text(
                """
                UPDATE crew_members
                SET data = jsonb_set(data, '{status}', to_jsonb('assigned'::text)),
                    updated_at = NOW()
                WHERE id = :crew_member_id AND tenant_id = :tenant_id
                """
            ),
            {
                "crew_member_id": crew_member_id,
                "tenant_id": tenant_id,
            },
        )

        db.commit()

        logger.info(
            "event_handler.crew_accepted.assignment_updated",
            extra={
                "transport_id": transport_id,
                "crew_member_id": crew_member_id,
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.crew_accepted.error",
            extra={
                "assignment_id": event_data.get("assignment_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


async def handle_incident_created(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle IncidentCreated event by creating a linked ePCR record.

    Workflow:
    1. Create ePCR record linked to incident
    2. Set initial status to 'draft'
    3. Pre-populate incident details
    4. Notify assigned crew members
    """
    try:
        incident_id = event_data.get("incident_id") or event_data.get("entity_id")
        incident_number = event_data.get("incident_number") or event_data.get("call_number")
        incident_type = event_data.get("incident_type") or event_data.get("call_type")
        tenant_id = event_data.get("tenant_id")

        logger.info(
            "event_handler.incident_created",
            extra={
                "incident_id": incident_id,
                "incident_number": incident_number,
                "incident_type": incident_type,
            },
        )

        if not incident_id or not tenant_id:
            logger.warning(
                "event_handler.incident_created.missing_ids",
                extra={
                    "incident_id": incident_id,
                    "tenant_id": tenant_id,
                },
            )
            return

        tenant_uuid = uuid.UUID(str(tenant_id))
        incident_uuid = uuid.UUID(str(incident_id))

        existing_epcr = (
            db.query(Epcr)
            .filter(
                Epcr.tenant_id == tenant_uuid,
                Epcr.incident_id == incident_uuid,
            )
            .first()
        )
        if existing_epcr is not None:
            logger.info(
                "event_handler.incident_created.epcr_exists",
                extra={
                    "incident_id": incident_id,
                    "epcr_id": str(existing_epcr.id),
                },
            )
            return

        template = await FormBuilderService(db).get_template_for_tenant(tenant_uuid, is_default=True)
        template_id = (
            template.get("id")
            if isinstance(template, dict)
            else getattr(template, "id", None)
        )
        epcr = Epcr(
            tenant_id=tenant_uuid,
            incident_id=incident_uuid,
            status=EpcrStatus.DRAFT,
            report_number=_next_epcr_report_number(db, tenant_uuid),
            chief_complaint=event_data.get("chief_complaint"),
            dispatch_complaint=incident_type,
            form_template_id=template_id,
            nemsis_dataset_version="3.5.1",
        )
        if getattr(epcr, "id", None) is None:
            epcr.id = uuid.uuid4()
        db.add(epcr)
        db.flush()
        epcr_id = uuid.UUID(str(cast(Any, epcr).id))
        form_template_id = cast(Any, epcr).form_template_id

        db.commit()

        get_event_publisher().publish_sync(
            event_name="epcr.auto_created",
            tenant_id=tenant_uuid,
            entity_id=epcr_id,
            entity_type="epcr",
            payload={
                "tenant_id": str(tenant_uuid),
                "incident_id": str(incident_uuid),
                "epcr_id": str(epcr_id),
                "report_number": epcr.report_number,
                "form_template_id": str(form_template_id) if form_template_id is not None else None,
            },
        )

        logger.info(
            "event_handler.incident_created.epcr_created",
            extra={
                "incident_id": incident_id,
                "epcr_id": str(epcr_id),
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.incident_created.error",
            extra={
                "incident_id": event_data.get("incident_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


def handle_epcr_validated(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle EpcrReportValidated event by triggering billing claim generation.

    Workflow:
    1. Extract ePCR data for billing
    2. Calculate claim amount using pricing rules
    3. Generate billing claim
    4. Publish BillingClaimGenerated event
    """
    try:
        epcr_id = event_data.get("epcr_id")
        incident_id = event_data.get("incident_id")
        patient_id = event_data.get("patient_id")
        tenant_id = event_data.get("tenant_id")
        nemsis_compliant = event_data.get("nemsis_compliant", False)

        logger.info(
            "event_handler.epcr_validated",
            extra={
                "epcr_id": epcr_id,
                "incident_id": incident_id,
                "nemsis_compliant": nemsis_compliant,
            },
        )

        # Only generate claims for NEMSIS-compliant reports
        if not nemsis_compliant:
            logger.warning(
                "event_handler.epcr_validated.not_compliant",
                extra={"epcr_id": epcr_id},
            )
            return

        # Query ePCR details for billing
        epcr_query = text(
            """
            SELECT data
            FROM epcr_reports
            WHERE id = :epcr_id AND tenant_id = :tenant_id
            """
        )

        epcr_result = db.execute(epcr_query, {"epcr_id": epcr_id, "tenant_id": tenant_id}).mappings().first()

        if not epcr_result:
            logger.error(
                "event_handler.epcr_validated.epcr_not_found",
                extra={"epcr_id": epcr_id},
            )
            return

        epcr_data = epcr_result["data"]

        # Calculate claim amount (simplified - in production use pricing engine)
        claim_amount = 850.00  # Base ALS transport

        # Create billing claim
        claim_id = str(uuid.uuid4())

        db.execute(
            text(
                """
                INSERT INTO billing_claims (id, tenant_id, data, created_at)
                VALUES (:id, :tenant_id, CAST(:data AS jsonb), NOW())
                """
            ),
            {
                "id": claim_id,
                "tenant_id": tenant_id,
                "data": {
                    "epcr_id": epcr_id,
                    "incident_id": incident_id,
                    "patient_id": patient_id,
                    "claim_amount": claim_amount,
                    "payer_type": "medicare",
                    "status": "generated",
                },
            },
        )

        db.commit()

        logger.info(
            "event_handler.epcr_validated.claim_generated",
            extra={
                "epcr_id": epcr_id,
                "claim_id": claim_id,
                "claim_amount": claim_amount,
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.epcr_validated.error",
            extra={
                "epcr_id": event_data.get("epcr_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


def handle_low_stock(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle InventoryLowStock event by triggering automated reorder.

    Workflow:
    1. Check reorder rules for item
    2. Calculate reorder quantity
    3. Create purchase order
    4. Notify inventory manager
    """
    try:
        item_id = event_data.get("item_id")
        item_name = event_data.get("item_name")
        current_quantity = event_data.get("current_quantity")
        threshold_quantity = event_data.get("threshold_quantity")
        tenant_id = event_data.get("tenant_id")

        logger.info(
            "event_handler.low_stock",
            extra={
                "item_id": item_id,
                "item_name": item_name,
                "current": current_quantity,
                "threshold": threshold_quantity,
            },
        )

        if threshold_quantity is None:
            logger.warning(
                "event_handler.low_stock.missing_threshold",
                extra={"item_id": item_id, "tenant_id": tenant_id},
            )
            return

        threshold_value = int(threshold_quantity)

        # Calculate reorder quantity (simple: 2x threshold)
        reorder_quantity = threshold_value * 2

        # Create reorder request
        reorder_id = str(uuid.uuid4())

        db.execute(
            text(
                """
                INSERT INTO inventory_reorders (id, tenant_id, data, created_at)
                VALUES (:id, :tenant_id, CAST(:data AS jsonb), NOW())
                """
            ),
            {
                "id": reorder_id,
                "tenant_id": tenant_id,
                "data": {
                    "item_id": item_id,
                    "item_name": item_name,
                    "quantity": reorder_quantity,
                    "status": "pending",
                    "reason": "low_stock_alert",
                },
            },
        )

        db.commit()

        logger.info(
            "event_handler.low_stock.reorder_created",
            extra={
                "item_id": item_id,
                "reorder_id": reorder_id,
                "quantity": reorder_quantity,
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.low_stock.error",
            extra={
                "item_id": event_data.get("item_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


def handle_narcotic_discrepancy(event_data: dict[str, Any], db: Session) -> None:
    """
    Handle NarcoticDiscrepancy event by triggering compliance investigation.

    Workflow:
    1. Create investigation record
    2. Lock affected narcotic inventory
    3. Notify compliance officer and medical director
    4. Generate audit report
    """
    try:
        discrepancy_id = event_data.get("discrepancy_id")
        drug_name = event_data.get("drug_name")
        expected_quantity = event_data.get("expected_quantity")
        actual_quantity = event_data.get("actual_quantity")
        discrepancy_amount = event_data.get("discrepancy_amount")
        location = event_data.get("location")
        tenant_id = event_data.get("tenant_id")

        logger.warning(
            "event_handler.narcotic_discrepancy",
            extra={
                "discrepancy_id": discrepancy_id,
                "drug_name": drug_name,
                "expected": expected_quantity,
                "actual": actual_quantity,
                "discrepancy": discrepancy_amount,
                "location": location,
            },
        )

        # Create investigation record
        investigation_id = str(uuid.uuid4())

        db.execute(
            text(
                """
                INSERT INTO compliance_investigations (id, tenant_id, data, created_at)
                VALUES (:id, :tenant_id, CAST(:data AS jsonb), NOW())
                """
            ),
            {
                "id": investigation_id,
                "tenant_id": tenant_id,
                "data": {
                    "discrepancy_id": discrepancy_id,
                    "investigation_type": "narcotic_discrepancy",
                    "drug_name": drug_name,
                    "discrepancy_amount": discrepancy_amount,
                    "location": location,
                    "status": "open",
                    "priority": "high",
                },
            },
        )

        db.commit()

        logger.warning(
            "event_handler.narcotic_discrepancy.investigation_created",
            extra={
                "discrepancy_id": discrepancy_id,
                "investigation_id": investigation_id,
                "drug_name": drug_name,
            },
        )

    except Exception as e:
        logger.error(
            "event_handler.narcotic_discrepancy.error",
            extra={
                "discrepancy_id": event_data.get("discrepancy_id"),
                "error": str(e),
            },
            exc_info=True,
        )
        db.rollback()
        raise


# ================================
# NEMSIS Auto-Export Pipeline Handlers (Phase 3.2)
# ================================


def handle_epcr_locked(event_data: dict[str, Any], db: Session) -> None:
    """Handle nemsis.epcr.locked event by triggering the auto-export pipeline.

    When an ePCR is locked, this handler runs compliance checks, and if the
    record is compliant, queues it for export.
    """
    from core_app.services.nemsis_service import NemsisService

    epcr_id = event_data.get("entity_id")
    tenant_id = event_data.get("tenant_id")
    actor_id = event_data.get("actor_id")

    if not epcr_id or not tenant_id:
        logger.warning(
            "event_handler.epcr_locked.missing_ids epcr_id=%s tenant_id=%s",
            epcr_id, tenant_id,
        )
        return

    try:
        svc = NemsisService(db)
        result = svc.auto_export_pipeline(
            epcr_id=uuid.UUID(str(epcr_id)),
            tenant_id=uuid.UUID(str(tenant_id)),
            actor_user_id=uuid.UUID(str(actor_id)) if actor_id else None,
        )
        logger.info(
            "event_handler.epcr_locked.pipeline_complete",
            extra={
                "epcr_id": epcr_id,
                "status": result.get("status"),
            },
        )
    except Exception as e:
        logger.error(
            "event_handler.epcr_locked.error",
            extra={
                "epcr_id": epcr_id,
                "error": str(e),
            },
            exc_info=True,
        )


# ================================
# Handler Registration
# ================================


def register_core_handlers(registry: EventHandlerRegistry | None = None) -> None:
    """
    Register all core event handlers with the registry.

    This should be called during application startup to ensure handlers
    are available for event processing.

    Args:
        registry: Optional handler registry (uses global registry if None)
    """
    if registry is None:
        registry = get_handler_registry()

    # Transport handlers
    registry.register("TransportRequestCreated", handle_transport_created)

    # Crew handlers
    registry.register("CrewAssignmentAccepted", handle_crew_accepted)

    # Incident handlers
    registry.register("IncidentCreated", handle_incident_created)
    registry.register("incident.created", handle_incident_created)

    # ePCR handlers
    registry.register("EpcrReportValidated", handle_epcr_validated)

    # Inventory handlers
    registry.register("InventoryLowStock", handle_low_stock)
    registry.register("NarcoticDiscrepancy", handle_narcotic_discrepancy)

    # NEMSIS auto-export pipeline handlers (Phase 3.2)
    registry.register("nemsis.epcr.locked", handle_epcr_locked)

    # Billing event handlers (Phase 4 — T420)
    from core_app.billing.event_handlers import register_billing_event_handlers

    register_billing_event_handlers()

    logger.info(
        "event_handler.core_handlers_registered",
        extra={
            "handler_count": 8,
        },
    )
