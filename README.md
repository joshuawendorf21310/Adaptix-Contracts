# adaptix-contracts

**Version**: 0.2.0  
**Status**: Stable (0.x stabilisation — no breaking changes without major bump)

The single source of truth for all shared contracts in the Adaptix polyrepo system.
Every cross-repo integration flows through a type defined here.

---

## What This Package Owns

| Module | What It Provides |
|--------|-----------------|
| `adaptix_contracts.envelope` | `EventEnvelope` — canonical versioned event transport wrapper |
| `adaptix_contracts.registry` | `CONTRACT_REGISTRY` — 489-entry catalog of all platform event types, `validate_catalog_against_registry()` |
| `adaptix_contracts.compat` | `COMPATIBILITY_MATRIX` (18 repos), `assert_compatible()`, `DownstreamDeclaration` |
| `adaptix_contracts.version` | `CONTRACT_VERSION` and version constants |
| `adaptix_contracts.types.enums` | All domain enum types (no SQLAlchemy dependency) |
| `adaptix_contracts.utils.roles` | `normalize_role_claims()` |
| `adaptix_contracts.schemas.*` | 33 Pydantic schema files for every domain |
| `adaptix_contracts.events.*` | Typed `DomainEvent` subclasses for all 489 event types across 20 modules, `EventCatalog`, `import_all_events()` |

## What This Package Does NOT Own

- Service implementations
- Persistence / migration logic
- Business workflow execution
- UI components
- Runtime event bus infrastructure (that lives in `adaptix-core`)

---

## Quick Start

### Install

```bash
pip install "adaptix-contracts>=0.2.0"
```

### Wrap and publish a cross-repo event

```python
from adaptix_contracts.envelope import EventEnvelope
import uuid

envelope = EventEnvelope.wrap(
    event_type="incident.created",
    source_repo="adaptix-cad",
    tenant_id=uuid.UUID("..."),
    payload={
        "incident_id": "...",
        "priority": "charlie",
        "location": "123 Main St",
    },
)

# Publish to Redis / SQS / EventBridge
bus.publish(envelope.to_bus_dict())
```

### Consume a cross-repo event

```python
from adaptix_contracts.envelope import EventEnvelope

raw = bus.receive()  # dict from Redis / SQS / EventBridge
envelope = EventEnvelope.from_bus_dict(raw)

print(envelope.event_type)     # "incident.created"
print(envelope.tenant_id)      # UUID
print(envelope.schema_version) # 1
print(envelope.payload)        # {"incident_id": ..., ...}
```

### Declare compatibility at startup

```python
# In your repo's application startup (e.g. main.py)
from adaptix_contracts.compat import assert_compatible

assert_compatible(min_version="0.1.1", max_version="0.2.x")
# Raises RuntimeError if the installed adaptix-contracts is outside the declared range.
```

### Look up a contract

```python
from adaptix_contracts.registry import lookup_required

entry = lookup_required("epcr.signed")
print(entry.source_repo)     # "adaptix-epcr"
print(entry.schema_version)  # 1
print(entry.stability)       # "stable"
print(entry.payload_fields)  # ("epcr_id", "incident_id", "patient_id", "signed_by", "signed_at")
```

### Validate catalog completeness at startup

```python
from adaptix_contracts.events import import_all_events
from adaptix_contracts.registry import validate_catalog_against_registry

import_all_events()
result = validate_catalog_against_registry()
assert result["ok"], f"Missing catalog schemas: {result['missing']}"
```

---

## Event Envelope Contract

All cross-repo events MUST be wrapped in `EventEnvelope` before publication.
The envelope shape is frozen at `envelope_version=1.0` and will only change on a major version bump.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `envelope_id` | `str` (UUID) | auto | Unique envelope instance ID |
| `envelope_version` | `str` | `"1.0"` | Shape version — consumers MUST reject unknown major versions |
| `contract_version` | `str` | auto | Installed package semver |
| `schema_version` | `int` | `1` | Payload schema version — increment on payload breaking changes |
| `event_type` | `str` | required | Dot-namespaced type e.g. `"incident.created"` |
| `source_repo` | `str` | required | Publishing repo slug e.g. `"adaptix-cad"` |
| `tenant_id` | `UUID` | required | Tenant isolation key |
| `actor_id` | `UUID?` | optional | User/service that triggered the event |
| `correlation_id` | `str?` | optional | Tracing chain token |
| `causation_id` | `str?` | optional | `envelope_id` of the causing event |
| `emitted_at` | `datetime` | auto | UTC timestamp |
| `payload` | `dict` | `{}` | Domain-specific data |

---

## Compatibility Policy

| Bump type | Meaning | Downstream action required |
|-----------|---------|---------------------------|
| PATCH (0.1.x) | Bug fix | None |
| MINOR (0.x.0) | Additive (new fields, new event types) | Optional — new fields are ignored |
| MAJOR (x.0.0) | Breaking | **Required** — see `BREAKING_CHANGES.md` |

### Declaring compatibility in your repo

Create a `contracts.json` in your repo root:

```json
{
  "repo": "adaptix-your-repo",
  "min_contract_version": "0.1.1",
  "max_contract_version": "0.2.x",
  "event_types": ["incident.created", "epcr.signed"],
  "notes": "Update to 0.3.x after BRK-0001 migration is complete"
}
```

Then validate at startup:

```python
from adaptix_contracts.compat import DownstreamDeclaration

dec = DownstreamDeclaration.from_json_file("contracts.json")
dec.assert_or_raise()  # Raises RuntimeError if incompatible
```

---

## Architecture Policies (encoded as tests)

The following policies are enforced by `tests/test_compat.py` and `tests/test_registry.py`:

- **Fire isolation**: Fire standalone repos MUST NOT consume MDT, CAD, or CrewLink events.
- **CrewLink device-first**: Delivery targets are resolved via device registry (push token),
  never via phone number. Telnyx SMS events are forbidden in CrewLink event subscriptions.
- **Telnyx billing-only**: Telnyx is used for patient billing communications only.
  No operational SMS delivery uses Telnyx.
- **Core authority**: `adaptix-core` owns all auth, tenancy, audit, and governance events.
- **ePCR integration point**: `epcr.signed` triggers billing claim creation and AI review.

---

## Running Tests

```bash
# From the package root
python -m pytest tests -q --tb=short
# Expected: 1713 passed
```

---

## Version History

See [CHANGELOG.md](CHANGELOG.md) for full history.
See [BREAKING_CHANGES.md](BREAKING_CHANGES.md) for the breaking change registry.

---

## Publishing a New Version

1. Make changes.
2. Update `pyproject.toml` version, `adaptix_contracts/__init__.py` `__version__`,
   and `adaptix_contracts/version.py` `CONTRACT_VERSION`.
3. If the change is breaking: add an entry to `BREAKING_CHANGES.md` FIRST.
4. Update `CHANGELOG.md`.
5. Run tests: `python -m pytest tests -q`.
6. Tag `vX.Y.Z` and push.
7. All affected downstream repos update their `contracts.json` entries.
8. Update `COMPATIBILITY_MATRIX.json` to reflect new declared support.

