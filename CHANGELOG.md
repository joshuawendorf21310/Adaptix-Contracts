# Changelog

All notable changes to `adaptix-contracts` are recorded in this file.

The format follows Keep a Changelog principles and uses semantic versioning.

## [1.1.0] - 2026-05-09

### Added
- Added LICENSE file (Apache 2.0) for open-source distribution readiness.
- Added CONTRIBUTING.md with contributor guidelines.
- Added `py.typed` marker file for PEP 561 type hint support.
- Added 14 missing symbols to `schemas/__all__`: duty_auth contracts (9) and ePCR sub-contracts (5).
- Added full PyPI metadata to pyproject.toml: classifiers, license, keywords, URLs.

### Changed
- Updated README.md with accurate domain coverage (48 domains, 572 exports, 461 models, 103 enums).
- Updated README.md package structure listing to reflect all current schema files.
- Replaced "Internal Adaptix package" license notice with proper Apache 2.0 reference.
- Bumped version to 1.1.0.

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