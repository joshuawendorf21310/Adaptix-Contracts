"""Adaptix platform event bus contracts.

Provides the canonical ``LocalEventConsumerRegistry`` for domain services
to register event handlers, and the ``EventBusPublisherClient`` for
querying and updating event delivery state via the Core event bus.

These contracts are consumed by domain event processing workers such as
``cad_app.background_worker``.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any, Callable, Coroutine
from uuid import UUID

from sqlalchemy import DateTime, Integer, JSON, String, Text, Uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

logger = logging.getLogger(__name__)

# Type alias for async event handler callables
EventHandler = Callable[[dict, AsyncSession], Coroutine[Any, Any, bool]]


class _EventBusBase(DeclarativeBase):
    """Isolated declarative base for event bus models."""

    pass


class DomainEventRecord(_EventBusBase):
    """Pending cross-domain event record in the Core event bus.

    Written by publishing domains; consumed and marked delivered/failed
    by subscribing domain workers.

    Attributes:
        id: UUID primary key.
        tenant_id: Tenant context for the event.
        event_type: Dot-namespaced event type e.g. ``cad.case.created``.
        payload: JSON event payload.
        status: ``pending``, ``delivered``, or ``failed``.
        retry_count: Number of failed delivery attempts.
        error_message: Last failure message if status is ``failed``.
        created_at: UTC timestamp of event creation.
        delivered_at: UTC timestamp of successful delivery.
    """

    __tablename__ = "domain_event_records"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True
    )
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<DomainEventRecord {self.id} ({self.event_type} - {self.status})>"


class LocalEventConsumerRegistry:
    """Registry mapping event types to async handler functions.

    Domain workers register handlers at startup; the background worker
    uses ``get_handlers`` to dispatch events to the correct handlers.

    Usage::

        registry = LocalEventConsumerRegistry()
        registry.register("crewlink.page.acknowledged", handler_fn)
        handlers = registry.get_handlers("crewlink.page.acknowledged")
    """

    def __init__(self) -> None:
        """Initialize an empty handler registry."""
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def register(self, event_type: str, handler: EventHandler) -> None:
        """Register an async handler for the given event type.

        Args:
            event_type: Dot-namespaced event type string.
            handler: Async callable accepting (event_dict, session) and
                returning bool. True = success; False = soft failure.

        Raises:
            ValueError: If event_type is empty or handler is not callable.
        """
        if not event_type:
            raise ValueError("event_type must be a non-empty string")
        if not callable(handler):
            raise ValueError("handler must be callable")
        self._handlers[event_type].append(handler)
        logger.debug(
            "event_registry: registered handler=%s for event_type=%s",
            handler.__qualname__,
            event_type,
        )

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        """Return all handlers registered for the given event type.

        Args:
            event_type: Dot-namespaced event type string.

        Returns:
            List of async handler callables. Empty list if none registered.
        """
        return list(self._handlers.get(event_type, []))

    def registered_event_types(self) -> list[str]:
        """Return all event types with at least one registered handler.

        Returns:
            Sorted list of registered event type strings.
        """
        return sorted(self._handlers.keys())


class EventBusPublisherClient:
    """Client for querying and updating Core event bus state.

    Domain background workers use this client to retrieve pending events
    and update their delivery status. All operations use the caller's
    active async session.
    """

    @staticmethod
    async def get_pending_events_unfiltered(
        session: AsyncSession,
        limit: int = 10,
    ) -> list[dict]:
        """Retrieve pending events from the Core event bus (all tenants).

        Returns events with status ``pending``, ordered by creation time,
        up to ``limit`` records.

        Args:
            session: Active async session connected to the Core database.
            limit: Maximum number of events to retrieve (default 10).

        Returns:
            List of event dicts with keys: id, event_type, tenant_id,
            payload, status, retry_count.
        """
        from sqlalchemy import select

        stmt = (
            select(DomainEventRecord)
            .where(DomainEventRecord.status == "pending")
            .order_by(DomainEventRecord.created_at)
            .limit(limit)
        )
        result = await session.execute(stmt)
        records = result.scalars().all()
        return [
            {
                "id": str(r.id),
                "event_type": r.event_type,
                "tenant_id": r.tenant_id,
                "payload": r.payload,
                "status": r.status,
                "retry_count": r.retry_count,
            }
            for r in records
        ]

    @staticmethod
    async def mark_delivered(session: AsyncSession, event_id: UUID) -> None:
        """Mark a pending event as successfully delivered.

        Args:
            session: Active async session connected to the Core database.
            event_id: UUID of the event to mark as delivered.
        """
        from sqlalchemy import update

        await session.execute(
            update(DomainEventRecord)
            .where(DomainEventRecord.id == event_id)
            .values(status="delivered", delivered_at=datetime.now(UTC))
        )
        await session.flush()
        logger.info("event_bus: marked delivered event_id=%s", event_id)

    @staticmethod
    async def mark_failed(
        session: AsyncSession,
        event_id: UUID,
        error_message: str,
    ) -> None:
        """Mark a pending event as permanently failed.

        Args:
            session: Active async session connected to the Core database.
            event_id: UUID of the event to mark as failed.
            error_message: Human-readable failure reason (truncated to 500 chars).
        """
        from sqlalchemy import update

        await session.execute(
            update(DomainEventRecord)
            .where(DomainEventRecord.id == event_id)
            .values(
                status="failed",
                error_message=error_message[:500],
                retry_count=DomainEventRecord.retry_count + 1,
            )
        )
        await session.flush()
        logger.error(
            "event_bus: marked failed event_id=%s reason=%s", event_id, error_message[:200]
        )


__all__ = [
    "LocalEventConsumerRegistry",
    "EventBusPublisherClient",
    "DomainEventRecord",
    "EventHandler",
]
