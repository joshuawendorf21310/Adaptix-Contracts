# Changelog

All notable changes to `adaptix-contracts` are recorded in this file.

The format follows Keep a Changelog principles and uses semantic versioning.

## [1.0.2] - 2026-05-08

### Added
- Added machine-readable `--json` output to `validate_contracts.py` so release automation can consume structured validation proof.
- Added `scripts/audit_workspace_contracts.py` to detect shadow `adaptix_contracts` trees across a polyrepo workspace.
- Added `tests/test_release_readiness.py` to cover JSON validation output and workspace shadow-package auditing.
- Added `.env.example` documenting `ADAPTIX_CONTRACTS_WORKSPACE_ROOT` for release audits.
- Added `MARKET_READY_LEDGER.md` as the authoritative proof ledger for market-readiness status.

### Changed
- Removed the repo's dependency on `pytest-asyncio` by converting async auth contract tests to synchronous `asyncio.run(...)` calls.
- Extended CI to build wheel/sdist artifacts and run `twine check` on the generated distributions.
- Updated readiness/runbook documentation to treat shadow-package detection as a hard release gate.

## [1.0.1] - 2026-04-21

### Added
- Added a pytest regression suite for schema exports, enum integrity, JSON schema generation, serialization round-trips, and representative validation failures.
- Added GitHub Actions validation for import checks, contract regression tests, and coverage reporting.
- Added documented deprecation and backward-compatibility policy for downstream services.

### Changed
- Fixed package-level symbol re-exports so `adaptix_contracts.<Symbol>` resolves consistently with `adaptix_contracts.schemas.<Symbol>`.
- Hardened `validate_contracts.py` to resolve schema paths from the repository location instead of the process working directory.
- Updated documented domain coverage from 26 to 28 to reflect `clinical_visual` and `inventory` contracts already present in the package.

## [1.0.0] - 2026-04-21

### Added
- Initial published shared Adaptix contracts package with cross-domain schema coverage.