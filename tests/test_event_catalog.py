"""
Tests for adaptix_contracts.events — EventCatalog and typed event coverage.

Validates:
  - import_all_events() populates the catalog
  - Every registry event type has a corresponding catalog entry
  - Schema lookup returns a valid Pydantic model class
  - validate_event() round-trips for all event types
"""

from __future__ import annotations

import uuid

import pytest

from adaptix_contracts.events import EventCatalog, import_all_events
from adaptix_contracts.registry import CONTRACT_REGISTRY, all_event_types


TENANT = uuid.UUID("12345678-1234-5678-1234-567812345678")
ENTITY = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


@pytest.fixture(autouse=True)
def _populate_catalog():
    """Ensure all event modules are imported before every test."""
    import_all_events()


class TestCatalogCoverage:
    def test_import_all_events_populates_catalog(self):
        catalog = EventCatalog()
        registered = {e["event_type"] for e in catalog.list_events()}
        assert len(registered) >= len(CONTRACT_REGISTRY)

    def test_every_registry_event_has_catalog_entry(self):
        catalog = EventCatalog()
        registered = {e["event_type"] for e in catalog.list_events()}
        for entry in CONTRACT_REGISTRY:
            assert entry.event_type in registered, (
                f"Registry event {entry.event_type!r} has no catalog schema"
            )

    def test_all_event_types_in_catalog(self):
        catalog = EventCatalog()
        for event_type in all_event_types():
            schema = catalog.get_schema(event_type)
            assert schema is not None, f"No schema for {event_type!r}"


class TestSchemaLookup:
    def test_get_schema_returns_pydantic_model(self):
        from pydantic import BaseModel

        catalog = EventCatalog()
        for event_type in all_event_types():
            schema = catalog.get_schema(event_type)
            assert schema is not None
            assert issubclass(schema, BaseModel)

    def test_get_schema_unknown_returns_none(self):
        catalog = EventCatalog()
        assert catalog.get_schema("nonexistent.event") is None


class TestValidateEvent:
    def test_validate_each_registry_event(self):
        """Every registered event should be constructable with minimal required fields."""
        catalog = EventCatalog()
        for entry in CONTRACT_REGISTRY:
            schema = catalog.get_schema(entry.event_type)
            assert schema is not None, f"No schema for {entry.event_type!r}"
            # Construct with the minimum required DomainEvent fields
            instance = schema(
                event_type=entry.event_type,
                tenant_id=TENANT,
                entity_type=entry.event_type.split(".")[0],
                entity_id=ENTITY,
            )
            assert instance.event_type == entry.event_type

    def test_validate_event_helper(self):
        catalog = EventCatalog()
        result = catalog.validate_event(
            "incident.created",
            {
                "event_type": "incident.created",
                "tenant_id": str(TENANT),
                "entity_type": "incident",
                "entity_id": str(ENTITY),
            },
        )
        assert result is not None
        assert result.event_type == "incident.created"

    def test_validate_event_unknown_returns_none(self):
        catalog = EventCatalog()
        assert catalog.validate_event("nonexistent.event", {}) is None


class TestConsumerRegistration:
    def test_register_and_get_consumers(self):
        catalog = EventCatalog()

        def handler(event):
            pass

        catalog.register_consumer("incident.created", handler, "test handler")
        consumers = catalog.get_consumers("incident.created")
        assert handler in consumers

    def test_list_events_includes_consumer_count(self):
        catalog = EventCatalog()
        events = catalog.list_events()
        assert all("consumer_count" in e for e in events)
