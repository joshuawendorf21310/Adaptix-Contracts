"""
Tests for adaptix_contracts.envelope

Validates:
  - EventEnvelope construction and field defaults
  - wrap() convenience constructor
  - to_bus_dict() / from_bus_dict() round-trip
  - envelope_version and contract_version are always present
  - is_compatible_with() delegates correctly to compat layer
  - tenant_id isolation (UUID type enforced)
  - schema_version must be >= 1
"""

from __future__ import annotations

import uuid

import pytest

from adaptix_contracts.envelope import ENVELOPE_VERSION, EventEnvelope
from adaptix_contracts.version import CONTRACT_VERSION


TENANT = uuid.UUID("12345678-1234-5678-1234-567812345678")
ACTOR = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


class TestEventEnvelopeDefaults:
    def test_required_fields(self):
        env = EventEnvelope(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
        )
        assert env.event_type == "incident.created"
        assert env.source_repo == "adaptix-cad"
        assert env.tenant_id == TENANT

    def test_envelope_version_is_injected(self):
        env = EventEnvelope(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
        )
        assert env.envelope_version == ENVELOPE_VERSION

    def test_contract_version_is_injected(self):
        env = EventEnvelope(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
        )
        assert env.contract_version == CONTRACT_VERSION

    def test_schema_version_defaults_to_1(self):
        env = EventEnvelope(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
        )
        assert env.schema_version == 1

    def test_envelope_id_is_uuid_string(self):
        env = EventEnvelope(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
        )
        # Must be parseable as UUID
        uuid.UUID(env.envelope_id)

    def test_unique_envelope_ids(self):
        a = EventEnvelope(event_type="x", source_repo="y", tenant_id=TENANT)
        b = EventEnvelope(event_type="x", source_repo="y", tenant_id=TENANT)
        assert a.envelope_id != b.envelope_id

    def test_emitted_at_is_utc(self):
        import datetime

        env = EventEnvelope(event_type="x", source_repo="y", tenant_id=TENANT)
        assert env.emitted_at.tzinfo is not None
        assert env.emitted_at.tzinfo == datetime.timezone.utc

    def test_optional_fields_default_to_none(self):
        env = EventEnvelope(event_type="x", source_repo="y", tenant_id=TENANT)
        assert env.actor_id is None
        assert env.correlation_id is None
        assert env.causation_id is None

    def test_payload_defaults_to_empty_dict(self):
        env = EventEnvelope(event_type="x", source_repo="y", tenant_id=TENANT)
        assert env.payload == {}


class TestEventEnvelopeValidation:
    def test_schema_version_must_be_positive(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            EventEnvelope(
                event_type="x",
                source_repo="y",
                tenant_id=TENANT,
                schema_version=0,
            )

    def test_tenant_id_must_be_uuid(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            EventEnvelope(
                event_type="x",
                source_repo="y",
                tenant_id="not-a-uuid",  # type: ignore[arg-type]
            )

    def test_event_type_required(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            EventEnvelope(source_repo="y", tenant_id=TENANT)  # type: ignore[call-arg]


class TestWrapConstructor:
    def test_wrap_produces_valid_envelope(self):
        env = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={"incident_id": "abc"},
        )
        assert env.event_type == "incident.created"
        assert env.payload == {"incident_id": "abc"}
        assert env.schema_version == 1

    def test_wrap_passes_optional_fields(self):
        env = EventEnvelope.wrap(
            event_type="epcr.signed",
            source_repo="adaptix-epcr",
            tenant_id=TENANT,
            payload={},
            schema_version=2,
            actor_id=ACTOR,
            correlation_id="c0rr-1234",
            causation_id="c0rr-parent",
        )
        assert env.schema_version == 2
        assert env.actor_id == ACTOR
        assert env.correlation_id == "c0rr-1234"
        assert env.causation_id == "c0rr-parent"


class TestRoundTrip:
    def test_to_bus_dict_is_json_serialisable(self):
        import json

        env = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={"incident_id": "xyz"},
        )
        raw = env.to_bus_dict()
        # Must round-trip through JSON without error
        serialised = json.dumps(raw)
        assert "incident.created" in serialised

    def test_from_bus_dict_reconstructs_envelope(self):
        env = EventEnvelope.wrap(
            event_type="incident.created",
            source_repo="adaptix-cad",
            tenant_id=TENANT,
            payload={"key": "value"},
        )
        raw = env.to_bus_dict()
        reconstructed = EventEnvelope.from_bus_dict(raw)

        assert reconstructed.envelope_id == env.envelope_id
        assert reconstructed.event_type == env.event_type
        assert reconstructed.tenant_id == env.tenant_id
        assert reconstructed.payload == env.payload
        assert reconstructed.emitted_at == env.emitted_at


class TestCompatibilityCheck:
    def test_is_compatible_within_range(self):
        env = EventEnvelope.wrap(
            event_type="x",
            source_repo="y",
            tenant_id=TENANT,
            payload={},
        )
        assert env.is_compatible_with("0.1.0")

    def test_is_compatible_exact_match(self):
        env = EventEnvelope.wrap(
            event_type="x",
            source_repo="y",
            tenant_id=TENANT,
            payload={},
        )
        assert env.is_compatible_with(CONTRACT_VERSION)

    def test_is_not_compatible_when_too_old(self):
        env = EventEnvelope.wrap(
            event_type="x",
            source_repo="y",
            tenant_id=TENANT,
            payload={},
        )
        # Require a future version not yet released
        assert not env.is_compatible_with("99.0.0")
