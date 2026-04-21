"""Regression tests for the Adaptix contracts package surface."""

from __future__ import annotations

from enum import Enum
from importlib import import_module
from pathlib import Path
import tomllib

import adaptix_contracts
from adaptix_contracts import schemas
from pydantic import BaseModel


def _load_project_version() -> str:
    """Return the package version declared in ``pyproject.toml``."""

    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    project_config = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return project_config["project"]["version"]


def test_package_version_matches_pyproject_metadata() -> None:
    """Keep runtime and packaging versions aligned for reproducible releases."""

    assert adaptix_contracts.__version__ == _load_project_version()


def test_schema_public_exports_are_unique_and_resolvable() -> None:
    """Ensure every declared public export exists exactly once."""

    assert len(schemas.__all__) == len(set(schemas.__all__))
    for symbol_name in schemas.__all__:
        assert hasattr(schemas, symbol_name), f"Missing schema export: {symbol_name}"


def test_package_root_reexports_schema_symbols() -> None:
    """Expose the same contract surface at the package root and schema module."""

    assert adaptix_contracts.__all__ == schemas.__all__
    for symbol_name in schemas.__all__:
        assert getattr(adaptix_contracts, symbol_name) is getattr(schemas, symbol_name)


def test_every_schema_module_imports_cleanly() -> None:
    """Prevent orphaned schema modules that import only in selective environments."""

    schema_dir = Path(__file__).resolve().parents[1] / "adaptix_contracts" / "schemas"
    for schema_path in schema_dir.glob("*.py"):
        if schema_path.name == "__init__.py":
            continue
        import_module(f"adaptix_contracts.schemas.{schema_path.stem}")


def test_all_exported_models_can_emit_json_schema() -> None:
    """Guarantee the contract surface remains introspectable for downstream tooling."""

    for symbol_name in schemas.__all__:
        symbol = getattr(schemas, symbol_name)
        if isinstance(symbol, type) and issubclass(symbol, BaseModel):
            emitted_schema = symbol.model_json_schema()
            assert isinstance(emitted_schema, dict)
            assert emitted_schema
            assert (
                "title" in emitted_schema
                or "properties" in emitted_schema
                or "$defs" in emitted_schema
                or "type" in emitted_schema
            ), f"Unexpected JSON schema shape for {symbol_name}"


def test_all_exported_enums_have_unique_values() -> None:
    """Protect enum consumers from ambiguous serialized values."""

    for symbol_name in schemas.__all__:
        symbol = getattr(schemas, symbol_name)
        if isinstance(symbol, type) and issubclass(symbol, Enum):
            values = [member.value for member in symbol]
            assert len(values) == len(set(values)), f"Duplicate enum values in {symbol_name}"