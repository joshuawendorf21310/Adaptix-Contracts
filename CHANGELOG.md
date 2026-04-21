# Changelog

All notable changes to `adaptix-contracts` are recorded in this file.

The format follows Keep a Changelog principles and uses semantic versioning.

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