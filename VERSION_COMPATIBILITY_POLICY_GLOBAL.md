# Version Compatibility Policy — Global

This document describes the version compatibility policy that applies across
**all** repositories in the Adaptix polyrepo system, not just `adaptix-contracts`.

## Principles

1. **Semantic Versioning** — Every Adaptix repository uses semver.
2. **Explicit Declaration** — Each repo pins a compatible range of `adaptix-contracts`
   in its `contracts.json` and `COMPATIBILITY_MATRIX.json` entry.
3. **Producer Tagging** — Producers publish `schema_version` on every cross-repo event
   so consumers can detect incompatible payloads at deserialisation time.
4. **Consumer Guarding** — Consumers call `assert_compatible()` at startup to fail fast
   if the installed contracts version is outside the declared range.
5. **No Floating** — Repositories pin compatible core/contracts versions; they do NOT
   float to `main`. Upgrades are intentional and tested.

## Cross-Repo Upgrade Workflow

1. `adaptix-contracts` publishes a new MINOR or MAJOR version.
2. All downstream repos update their `contracts.json` to include the new version.
3. Each downstream repo runs `validate_matrix()` in CI to verify.
4. PRs that fail the matrix check are blocked until the declaration is updated.

## Breaking Change Protocol

Before any MAJOR bump:

1. A `PLANNED` entry is added to `BREAKING_CHANGES.md`.
2. All affected repos acknowledge via PR comment.
3. A migration window is agreed upon (typically one sprint).
4. The old behaviour is removed only after all consumers have migrated.

## EventEnvelope Contract

All cross-repo events MUST be wrapped in `EventEnvelope` (enforced from 1.0.0).
The envelope carries `contract_version` and `schema_version`, enabling consumers
to detect version drift at runtime without hard-coding expectations.

## Matrix Enforcement

`COMPATIBILITY_MATRIX.json` is the machine-readable source of truth.
CI in `adaptix-contracts` validates the matrix on every push.
Downstream repos validate their own entry at build time.
