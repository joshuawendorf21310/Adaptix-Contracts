"""Event Catalog — singleton registry for all typed domain events.

Domains register their event classes at import time.  The catalog provides:
- schema lookup by event_type string
- consumer registration per event_type
- enumeration of all registered events (for observability / docs)
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class _ConsumerEntry:
    __slots__ = ("handler", "description")

    def __init__(self, handler: Callable[..., Any], description: str = ""):
        self.handler = handler
        self.description = description


class EventCatalog:
    """Thread-safe singleton that holds event type → schema mappings."""

    _instance: EventCatalog | None = None
    _lock = threading.Lock()

    def __new__(cls) -> EventCatalog:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._schemas: dict[str, type[BaseModel]] = {}
                    inst._consumers: dict[str, list[_ConsumerEntry]] = {}
                    cls._instance = inst
        return cls._instance

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        event_type: str,
        schema: type[BaseModel],
    ) -> None:
        """Register an event type with its Pydantic schema."""
        if event_type in self._schemas:
            existing = self._schemas[event_type]
            if existing is not schema:
                logger.warning(
                    "event_catalog.overwrite event_type=%s old=%s new=%s",
                    event_type,
                    existing.__name__,
                    schema.__name__,
                )
        self._schemas[event_type] = schema
        logger.debug("event_catalog.registered event_type=%s schema=%s", event_type, schema.__name__)

    def register_consumer(
        self,
        event_type: str,
        handler: Callable[..., Any],
        description: str = "",
    ) -> None:
        """Register a consumer handler for an event type."""
        self._consumers.setdefault(event_type, []).append(
            _ConsumerEntry(handler=handler, description=description)
        )

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_schema(self, event_type: str) -> type[BaseModel] | None:
        """Return the Pydantic schema for *event_type*, or ``None``."""
        return self._schemas.get(event_type)

    def list_events(self) -> list[dict[str, Any]]:
        """Return a list of all registered event types with metadata."""
        result: list[dict[str, Any]] = []
        for etype, schema in sorted(self._schemas.items()):
            consumers = self._consumers.get(etype, [])
            result.append(
                {
                    "event_type": etype,
                    "schema": schema.__name__,
                    "consumer_count": len(consumers),
                    "consumers": [c.description or c.handler.__name__ for c in consumers],
                }
            )
        return result

    def get_consumers(self, event_type: str) -> list[Callable[..., Any]]:
        """Return handler callables registered for *event_type*."""
        return [c.handler for c in self._consumers.get(event_type, [])]

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    def validate_event(self, event_type: str, data: dict[str, Any]) -> BaseModel | None:
        """Validate *data* against the registered schema, returning the model instance or ``None``."""
        schema = self.get_schema(event_type)
        if schema is None:
            return None
        return schema.model_validate(data)

    def clear(self) -> None:
        """Clear all registrations.  **Test-only** — never call in production."""
        self._schemas.clear()
        self._consumers.clear()
