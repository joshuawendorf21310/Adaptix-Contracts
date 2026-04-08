"""
Event Publisher Service for Adaptix

Production-ready event publishing with retry logic, batch processing, and idempotency.
Integrates with AWS EventBridge for the unified operational graph.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from core_app.core.config import get_settings
from core_app.events.event_bus import EventBridgePublishError, get_event_bus_client
from core_app.events.event_schema import BaseEvent, EventModel

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Production-ready event publisher with retry logic, idempotency, and dead-letter handling.

    Features:
    - Automatic retry with exponential backoff
    - Idempotency key generation and deduplication
    - Event archiving in PostgreSQL for audit trail
    - Dead-letter queue for failed events
    - Batch publishing support
    - Correlation ID tracking
    """

    def __init__(self, db_session: Session | None = None):
        """
        Initialize event publisher.

        Args:
            db_session: Optional SQLAlchemy session for event archiving
        """
        self.db_session = db_session
        self.event_bus = get_event_bus_client()
        self.settings = get_settings()

    def publish(
        self,
        event: EventModel | BaseEvent,
        *,
        resources: list[str] | None = None,
        idempotent: bool = True,
        retry_count: int = 3,
        retry_delay_seconds: float = 1.0,
    ) -> dict[str, Any]:
        """
        Publish a single event to EventBridge.

        Args:
            event: Event instance (any EventModel type)
            resources: Optional list of ARN resources associated with the event
            idempotent: Whether to ensure idempotency (default: True)
            retry_count: Number of retry attempts (default: 3)
            retry_delay_seconds: Initial retry delay in seconds (default: 1.0)

        Returns:
            Publishing result with event_id and status

        Raises:
            EventPublishError: If publishing fails after all retries
        """
        # Generate idempotency key if not provided and idempotency is enabled
        if idempotent and not event.idempotency_key:
            event.idempotency_key = self._generate_idempotency_key(event)

        # Check for duplicate event (idempotency)
        if idempotent and self.db_session and event.idempotency_key:
            if self._is_duplicate_event(event.idempotency_key, event.tenant_id):
                logger.info(
                    "event_publisher.duplicate_detected",
                    extra={
                        "event_type": event.event_type,
                        "idempotency_key": event.idempotency_key,
                        "tenant_id": str(event.tenant_id),
                    },
                )
                return {
                    "status": "duplicate",
                    "event_id": event.event_id,
                    "idempotency_key": event.idempotency_key,
                }

        # Archive event to PostgreSQL for audit trail
        if self.db_session:
            self._archive_event(event)

        # Prepare event for EventBridge
        source = event.source
        detail_type = event.event_type
        detail = event.model_dump(mode="json", exclude={"source"})

        # Publish to EventBridge with retry logic
        last_error = None
        for attempt in range(retry_count):
            try:
                result = self.event_bus.put_event(
                    source=source,
                    detail_type=detail_type,
                    detail=detail,
                    resources=resources,
                    trace_header=event.correlation_id,
                )

                logger.info(
                    "event_publisher.publish_success",
                    extra={
                        "event_type": event.event_type,
                        "event_id": event.event_id,
                        "tenant_id": str(event.tenant_id),
                        "eventbridge_event_id": result["event_id"],
                        "attempt": attempt + 1,
                    },
                )

                return {
                    "status": "published",
                    "event_id": event.event_id,
                    "eventbridge_event_id": result["event_id"],
                    "event_bus_name": result["event_bus_name"],
                    "idempotency_key": event.idempotency_key,
                }

            except EventBridgePublishError as e:
                last_error = e
                logger.warning(
                    "event_publisher.publish_retry",
                    extra={
                        "event_type": event.event_type,
                        "event_id": event.event_id,
                        "attempt": attempt + 1,
                        "max_attempts": retry_count,
                        "error": str(e),
                    },
                )

                # Exponential backoff
                if attempt < retry_count - 1:
                    delay = retry_delay_seconds * (2**attempt)
                    time.sleep(delay)

        # All retries exhausted - move to dead-letter queue
        logger.error(
            "event_publisher.publish_failed",
            extra={
                "event_type": event.event_type,
                "event_id": event.event_id,
                "tenant_id": str(event.tenant_id),
                "attempts": retry_count,
                "error": str(last_error),
            },
            exc_info=last_error,
        )

        if self.db_session:
            self._move_to_dead_letter_queue(event, str(last_error))

        raise EventPublishError(
            f"Failed to publish event {event.event_id} after {retry_count} attempts: {last_error}"
        )

    def publish_batch(
        self,
        events: list[EventModel | BaseEvent],
        *,
        idempotent: bool = True,
        retry_failed: bool = True,
    ) -> dict[str, Any]:
        """
        Publish multiple events in batch for better throughput.

        Args:
            events: List of event instances
            idempotent: Whether to ensure idempotency (default: True)
            retry_failed: Whether to retry failed events individually (default: True)

        Returns:
            Batch publishing result with success/failure counts
        """
        if not events:
            return {
                "status": "success",
                "total": 0,
                "successful": 0,
                "failed": 0,
                "duplicates": 0,
            }

        results = {
            "total": len(events),
            "successful": 0,
            "failed": 0,
            "duplicates": 0,
            "events": [],
        }

        # Filter out duplicate events
        events_to_publish = []
        for event in events:
            if idempotent and not event.idempotency_key:
                event.idempotency_key = self._generate_idempotency_key(event)

            if idempotent and self.db_session and event.idempotency_key:
                if self._is_duplicate_event(event.idempotency_key, event.tenant_id):
                    results["duplicates"] += 1
                    continue

            events_to_publish.append(event)

        # Archive all events to PostgreSQL
        if self.db_session:
            for event in events_to_publish:
                self._archive_event(event)

        # Prepare events for EventBridge batch API
        eventbridge_entries = []
        for event in events_to_publish:
            eventbridge_entries.append({
                "source": event.source,
                "detail_type": event.event_type,
                "detail": event.model_dump(mode="json", exclude={"source"}),
                "trace_header": event.correlation_id,
            })

        # Publish batch to EventBridge in groups of 10 (AWS limit)
        try:
            _AWS_BATCH_LIMIT = 10
            all_errors: list = []
            for i in range(0, len(eventbridge_entries), _AWS_BATCH_LIMIT):
                chunk = eventbridge_entries[i : i + _AWS_BATCH_LIMIT]
                batch_result = self.event_bus.put_events(chunk)

                results["successful"] += batch_result["successful"]
                results["failed"] += batch_result["failed"]
                # Adjust error indices relative to the full list
                for err in batch_result.get("errors", []):
                    adjusted = dict(err)
                    adjusted["event_index"] = err.get("event_index", 0) + i
                    all_errors.append(adjusted)

            logger.info(
                "event_publisher.batch_publish_complete",
                extra={
                    "total": results["total"],
                    "successful": results["successful"],
                    "failed": results["failed"],
                    "duplicates": results["duplicates"],
                },
            )

            # Retry failed events individually if requested
            if retry_failed and results["failed"] > 0:
                logger.info(
                    "event_publisher.batch_retry_failed",
                    extra={"failed_count": results["failed"]},
                )

                for error in all_errors:
                    event_idx = error["event_index"]
                    if event_idx < len(events_to_publish):
                        failed_event = events_to_publish[event_idx]
                        try:
                            self.publish(failed_event, idempotent=False)
                            results["successful"] += 1
                            results["failed"] -= 1
                        except EventPublishError:
                            # Already logged in publish()
                            pass

        except Exception as e:
            logger.error(
                "event_publisher.batch_publish_error",
                extra={
                    "total": results["total"],
                    "error": str(e),
                },
                exc_info=True,
            )
            results["failed"] = len(events_to_publish)

        return results

    def retry_failed_events(
        self,
        tenant_id: uuid.UUID | None = None,
        max_age_hours: int = 24,
        batch_size: int = 100,
    ) -> dict[str, Any]:
        """
        Retry events from the dead-letter queue.

        Args:
            tenant_id: Optional tenant filter
            max_age_hours: Maximum age of events to retry (default: 24 hours)
            batch_size: Number of events to retry per batch (default: 100)

        Returns:
            Retry result with success/failure counts
        """
        if not self.db_session:
            raise ValueError("Database session required for retrying failed events")

        # Query dead-letter queue
        query = """
            SELECT id, tenant_id, data
            FROM event_dead_letter_queue
            WHERE created_at > NOW() - INTERVAL '%s hours'
              AND retry_count < 5
        """
        params: dict[str, Any] = {}

        if tenant_id:
            query += " AND tenant_id = :tenant_id"
            params["tenant_id"] = str(tenant_id)

        query += " ORDER BY created_at ASC LIMIT :limit"
        params["limit"] = batch_size

        rows = self.db_session.execute(text(query % max_age_hours), params).mappings().all()

        results = {
            "total": len(rows),
            "successful": 0,
            "failed": 0,
        }

        for row in rows:
            event_data = row["data"]
            dlq_id = row["id"]

            try:
                # Reconstruct event from stored data
                event_type = event_data.get("event_type")
                # Note: In production, you'd have a registry to reconstruct the correct event type
                # For now, we'll use BaseEvent as a generic container

                from core_app.events.event_schema import BaseEvent

                event = BaseEvent(**event_data)

                # Retry publishing
                self.publish(event, idempotent=False, retry_count=1)

                # Remove from dead-letter queue
                self.db_session.execute(
                    text("DELETE FROM event_dead_letter_queue WHERE id = :id"),
                    {"id": str(dlq_id)},
                )
                self.db_session.commit()

                results["successful"] += 1

            except Exception as e:
                logger.error(
                    "event_publisher.retry_failed",
                    extra={
                        "dlq_id": str(dlq_id),
                        "event_type": event_data.get("event_type"),
                        "error": str(e),
                    },
                    exc_info=True,
                )

                # Increment retry count
                self.db_session.execute(
                    text(
                        "UPDATE event_dead_letter_queue "
                        "SET retry_count = retry_count + 1, "
                        "    updated_at = NOW() "
                        "WHERE id = :id"
                    ),
                    {"id": str(dlq_id)},
                )
                self.db_session.commit()

                results["failed"] += 1

        logger.info(
            "event_publisher.retry_complete",
            extra={
                "total": results["total"],
                "successful": results["successful"],
                "failed": results["failed"],
            },
        )

        return results

    def _generate_idempotency_key(self, event: BaseEvent) -> str:
        """
        Generate idempotency key from event content.

        Creates a deterministic hash from event type, tenant ID, and key fields.
        """
        key_parts = [
            str(event.event_type),
            str(event.tenant_id),
            str(event.timestamp.isoformat()),
        ]

        # Add event-specific identifying fields
        event_dict = event.model_dump()
        for field in ["transport_id", "incident_id", "epcr_id", "claim_id", "unit_id"]:
            if field in event_dict and event_dict[field]:
                key_parts.append(str(event_dict[field]))

        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()

    def _is_duplicate_event(self, idempotency_key: str, tenant_id: uuid.UUID) -> bool:
        """
        Check if event with this idempotency key already exists.
        """
        result = (
            self.db_session.execute(
                text(
                    "SELECT 1 FROM event_archive "
                    "WHERE tenant_id = :tenant_id "
                    "  AND data->>'idempotency_key' = :key "
                    "LIMIT 1"
                ),
                {"tenant_id": str(tenant_id), "key": idempotency_key},
            )
            .mappings()
            .first()
        )
        return result is not None

    def _archive_event(self, event: BaseEvent) -> None:
        """
        Archive event to PostgreSQL for audit trail.

        Events are stored in the event_archive table with JSONB for flexible querying.
        """
        try:
            event_data = event.model_dump(mode="json")

            self.db_session.execute(
                text(
                    "INSERT INTO event_archive (id, tenant_id, event_type, data, created_at) "
                    "VALUES (:id, :tenant_id, :event_type, CAST(:data AS jsonb), :created_at)"
                ),
                {
                    "id": event.event_id,
                    "tenant_id": str(event.tenant_id),
                    "event_type": event.event_type,
                    "data": json.dumps(event_data, default=str),
                    "created_at": event.timestamp,
                },
            )
            self.db_session.commit()

            logger.debug(
                "event_publisher.archive_success",
                extra={
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "tenant_id": str(event.tenant_id),
                },
            )

        except Exception as e:
            logger.error(
                "event_publisher.archive_failed",
                extra={
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "error": str(e),
                },
                exc_info=True,
            )
            # Don't fail event publishing if archiving fails
            self.db_session.rollback()

    def _move_to_dead_letter_queue(self, event: BaseEvent, error_message: str) -> None:
        """
        Move failed event to dead-letter queue for later retry or investigation.
        """
        try:
            event_data = event.model_dump(mode="json")
            event_data["error_message"] = error_message

            self.db_session.execute(
                text(
                    "INSERT INTO event_dead_letter_queue "
                    "(id, tenant_id, event_type, data, error_message, created_at) "
                    "VALUES (:id, :tenant_id, :event_type, CAST(:data AS jsonb), :error, NOW())"
                ),
                {
                    "id": str(uuid.uuid4()),
                    "tenant_id": str(event.tenant_id),
                    "event_type": event.event_type,
                    "data": json.dumps(event_data, default=str),
                    "error": error_message,
                },
            )
            self.db_session.commit()

            logger.info(
                "event_publisher.dead_letter_queued",
                extra={
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "tenant_id": str(event.tenant_id),
                },
            )

        except Exception as e:
            logger.error(
                "event_publisher.dead_letter_failed",
                extra={
                    "event_id": event.event_id,
                    "event_type": event.event_type,
                    "error": str(e),
                },
                exc_info=True,
            )
            self.db_session.rollback()


class EventPublishError(Exception):
    """Raised when event publishing fails after all retries."""
    pass


# Convenience functions for quick event publishing


def publish_event(
    event: EventModel | BaseEvent,
    db_session: Session | None = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Publish a single event (convenience function).

    Args:
        event: Event instance
        db_session: Optional database session
        **kwargs: Additional arguments passed to EventPublisher.publish()

    Returns:
        Publishing result
    """
    publisher = EventPublisher(db_session=db_session)
    return publisher.publish(event, **kwargs)


def publish_batch_events(
    events: list[EventModel | BaseEvent],
    db_session: Session | None = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Publish multiple events in batch (convenience function).

    Args:
        events: List of event instances
        db_session: Optional database session
        **kwargs: Additional arguments passed to EventPublisher.publish_batch()

    Returns:
        Batch publishing result
    """
    publisher = EventPublisher(db_session=db_session)
    return publisher.publish_batch(events, **kwargs)
