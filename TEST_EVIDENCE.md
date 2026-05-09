# Adaptix-Contracts Test Evidence

Date: 2026-05-08

## Evidence Available
- `python validate_contracts.py` — PASS
- `python -m pytest tests/test_narcotic_enum_compat.py -q` — PASS
- `python -m pytest tests/test_auth_contracts.py tests/test_release_readiness.py -q` — PASS (11 tests)
- `python -m pytest --cov=adaptix_contracts --cov-report=term-missing` — PASS (79 tests)
- `python -m build --sdist --wheel` — PASS
- `python -m twine check dist/*` — PASS
- `c:/Users/fusio/Desktop/workspace/Adaptix-Core-Service/.venv/Scripts/python.exe -m pytest test_import_source_guard.py -q` — PASS
- `Adaptix-Inventory-Service/.venv311-contracts/Scripts/python.exe -m pytest tests/test_import_source_guard.py tests/test_inventory_complete.py -q` — PASS (6 tests)
- `Adaptix-Narcotics-Service/.venv/Scripts/python.exe -m pytest -o addopts= tests/test_import_source_guard.py tests/test_narcotic_service.py -q` — PASS (6 tests)
- `Adaptix-Integrations-Service/.venv311-contracts/Scripts/python.exe -m pytest tests/test_import_source_guard.py -q` — PASS
- `python scripts/audit_workspace_contracts.py --workspace-root C:\Users\fusio\Desktop\workspace --json` — PASS (`shadow_package_count = 0`)

## Evidence Missing
- None for the audited workspace consumer-drift remediation slice.

## Verdict
PASS.