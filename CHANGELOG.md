# adaptix-contracts CHANGELOG

All notable changes to this package are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] — 2026-04-09

### BREAKING CHANGES
None. This release is fully backward-compatible with 0.1.x consumers.
All 0.1.1 consumers that declared `max_contract_version: "0.2.x"` can upgrade without changes.

### Added
- `adaptix_contracts.envelope.EventEnvelope` — canonical versioned event transport wrapper.
  All cross-repo events MUST be serialised inside an `EventEnvelope` before publication.
  Fields: `envelope_id`, `envelope_version`, `contract_version`, `schema_version`, `event_type`,
  `source_repo`, `tenant_id`, `actor_id`, `correlation_id`, `causation_id`, `emitted_at`, `payload`.
- `adaptix_contracts.version` — version constants module (`CONTRACT_VERSION`, `MIN_SUPPORTED_ENVELOPE_VERSION`,
  `DOWNSTREAM_MIN_REQUIRED`).
- `adaptix_contracts.compat` — compatibility checking module:
  - `is_version_compatible(version, min, max)` — semver range check with wildcard support
  - `assert_compatible(min, max)` — startup guard for downstream repos
  - `DownstreamDeclaration` — typed Pydantic model for consumer compatibility declarations
  - `COMPATIBILITY_MATRIX` — in-code list of all declared downstream consumers
  - `validate_matrix()` — checks all declarations against the current version
  - `get_declaration(repo)` — lookup by repo slug
- `adaptix_contracts.registry` — static contract registry:
  - `ContractEntry` — dataclass describing a single event contract
  - `CONTRACT_REGISTRY` — 55-entry authoritative catalog of all platform event types
  - `lookup(event_type)` / `lookup_required(event_type)` — event type resolution
  - `by_source_repo(repo)` / `by_stability(stability)` — filtered views
  - `catalog_summary()` — count summary by stability and repo
  - `validate_catalog_against_registry()` — validates EventCatalog coverage of all registry entries
- Typed `DomainEvent` subclasses for all 55 event types across 12 event modules
  (auth, audit, webhook, cad, mdt, epcr, billing, fire, crewlink, workforce, incident, nemsis)
- `adaptix_contracts.events.import_all_events()` — one-call function to populate the EventCatalog
- Sub-package `__init__.py` re-exports for events, types, utils, and schemas
- 7 NEMSIS export pipeline events added to CONTRACT_REGISTRY (lock → compliance → queue →
  validate → submit → accept/reject)
- `COMPATIBILITY_MATRIX.json` — machine-readable compatibility matrix. CI gate enforces updates.
- `BREAKING_CHANGES.md` — registry of all past and future planned breaking changes.
- `tests/test_envelope.py` — 19 envelope tests
- `tests/test_compat.py` — 35 compatibility tests including architecture policy enforcement
- `tests/test_registry.py` — 30 registry tests including service-line isolation policies
- `tests/test_enums.py` — 42 enum validation tests
- `tests/test_event_catalog.py` — 10 catalog coverage and schema lookup tests
- `tests/test_end_to_end.py` — 130+ end-to-end tests (golden path, NEMSIS pipeline, cross-domain
  integration, parametrized wrap/round-trip for all 55 events, catalog validation)
- `tests/test_roles.py` — 12 role normalization tests
- `tests/test_schemas.py` — 67 schema importability and validity tests

### Changed
- `pyproject.toml` bumped to v0.2.0.
- `adaptix_contracts/__init__.py` updated to v0.2.0.
- `adaptix_contracts/events/domain_event.py` — `DomainEvent.version` field was already present at `int=1`.
  No schema change; remains compatible.

### Architecture Policy Encoding
The following governing policies are now encoded as executable tests in `tests/test_registry.py`
and `tests/test_compat.py`:
- Fire standalone repos MUST NOT consume MDT, CAD, or CrewLink events.
- CrewLink MUST NOT consume Telnyx SMS events (Telnyx is billing-only).
- CrewLink delivery targets resolved via device registry, never phone number.
- `epcr.signed` is the canonical integration point for billing claim creation and AI review.
- `adaptix-core` owns all auth, tenancy, audit, and governance events.

---

## [0.1.1] — 2026-04-08

### Changed
- Enum fixes: added `CallType`, `DispatchPriority`, `CrewStatus`, `CrewAvailabilityStatus`,
  `InspectionStatus`, `TrainingType`.
- Added `ALLOWED_TRANSPORT_TRANSITIONS`, `allowed_transport_transition_targets`.

### Fixed
- Import patches for `narcotic.py` alias `NarcoticTransactionType as TransactionType`.
- Import patches for `inventory.py` alias `InventoryTransactionType as TransactionType`.

---

## [0.1.0] — 2026-04-08

### Added
- Initial release of adaptix-contracts as a pip-installable package.
- `adaptix_contracts.types.enums` — all domain enum types extracted from the Adaptix monorepo.
- `adaptix_contracts.utils.roles` — `normalize_role_claims()` utility.
- `adaptix_contracts.schemas.*` — 33 Pydantic schema files (auth, incident, epcr, billing, etc.).
- `adaptix_contracts.events.*` — 5 event type files (domain_event, event_catalog, event_schema,
  incident_events, nemsis_events).
- Monorepo shim layer: all 33 schema files and 5 event files in the monorepo now re-export
  from `adaptix_contracts.*` as the single source of truth.
