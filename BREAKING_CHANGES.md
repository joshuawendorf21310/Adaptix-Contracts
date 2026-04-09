# adaptix-contracts Breaking Change Registry

This document lists every past and planned breaking change to this package.
A breaking change is any change that requires downstream repos to update their
code before they can safely consume events from updated producers.

Policy: A breaking change MUST increment the MAJOR version.
Minor (additive) and patch (bug-fix) changes do NOT require downstream updates.

---

## Breaking Change Format

Every entry must include:
- **ID**: `BRK-NNNN` sequential
- **Version**: the version that introduced the break
- **Scope**: which module/field/type changed
- **Migration path**: exact steps for downstream repos
- **Affected repos**: list of repos that must migrate
- **Gate**: the date or milestone after which old behavior is removed

---

## Past Breaking Changes

*None.* The current major version is 0.x, meaning the package is still in
its initial stabilisation period. All 0.x minor bumps may contain additive
changes. The first MAJOR break will be tracked as BRK-0001.

---

## Planned / Pre-announced Breaking Changes

### [PLANNED] BRK-0001 — EventEnvelope becomes mandatory on event bus
- **Target version**: 1.0.0 (estimated Q3 2026)
- **Scope**: `EventEnvelope` wrapping will be enforced by the bus consumer router
- **What changes**: Raw `DomainEvent` messages will be REJECTED by event consumers.
  All producers must wrap events in `EventEnvelope` before publishing.
- **Migration path**:
  1. Replace `publisher.publish(domain_event)` with
     `publisher.publish(EventEnvelope.wrap(event_type=..., source_repo=..., payload=domain_event.model_dump()))`
  2. Consumer handlers receive `EventEnvelope`; extract `payload` and validate against `DomainEvent`.
  3. Update `max_contract_version` in your `COMPATIBILITY_MATRIX.json` entry and `contracts.json`.
- **Affected repos**: All repos that publish or consume domain events (all except adaptix-contracts itself).
- **Gate**: 0.x shim compatibility retained until 1.0.0 release. After 1.0.0, shim removed.

### [PLANNED] BRK-0002 — `DomainEvent.version` field renamed to `schema_version`
- **Target version**: 1.0.0
- **Scope**: `adaptix_contracts.events.domain_event.DomainEvent`
- **What changes**: `version: int` becomes `schema_version: int` to align with `EventEnvelope.schema_version`.
- **Migration path**: Replace all `event.version` field access with `event.schema_version`.
- **Affected repos**: Any repo that reads the `version` field from a `DomainEvent` instance.
- **Gate**: Paired with BRK-0001 in the 1.0.0 release.

---

## Pre-breaking Change Audit (Required Before 1.0.0)

The following items must be verified before releasing 1.0.0:

| Item | Owner | Status |
|------|-------|--------|
| All event publishers wrap in EventEnvelope | adaptix-core | Not started |
| All event consumers unwrap EventEnvelope | All product repos | Not started |
| EnvelopeVersion validation in event bus | adaptix-core | Not started |
| `DomainEvent.version` field migration | All repos reading `.version` | Not started |
| COMPATIBILITY_MATRIX.json updated to 1.0.x | All consumer repos | Not started |
| EventCatalog validates against CONTRACT_REGISTRY | adaptix-core | Not started |

---

## How to Propose a Breaking Change

1. Open a PR against this file adding a new `PLANNED` entry.
2. Tag the PR with `breaking-change` and `contracts-governance`.
3. All affected repos must acknowledge via PR comment before the PR merges.
4. The planned entry moves to `Past Breaking Changes` when the version is released.

Breaking changes that are merged without entries in this file are policy violations.
