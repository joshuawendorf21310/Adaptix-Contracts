"""
Tests for adaptix_contracts.schemas — importability and validity.

Validates:
  - Every schema module under schemas/ is importable
  - Each module exports at least one Pydantic BaseModel subclass
  - No import errors or circular dependencies
"""

from __future__ import annotations

import importlib
import pkgutil

import pytest
from pydantic import BaseModel

import adaptix_contracts.schemas as schemas_pkg


def _schema_module_names() -> list[str]:
    """Discover all schema sub-module names."""
    return [
        name
        for _importer, name, _ispkg in pkgutil.iter_modules(schemas_pkg.__path__)
        if not name.startswith("_")
    ]


SCHEMA_MODULES = _schema_module_names()


class TestSchemaImportability:
    @pytest.mark.parametrize("module_name", SCHEMA_MODULES)
    def test_schema_module_is_importable(self, module_name: str):
        mod = importlib.import_module(f"adaptix_contracts.schemas.{module_name}")
        assert mod is not None

    @pytest.mark.parametrize("module_name", SCHEMA_MODULES)
    def test_schema_module_has_pydantic_models(self, module_name: str):
        mod = importlib.import_module(f"adaptix_contracts.schemas.{module_name}")
        models = [
            obj
            for name in dir(mod)
            if not name.startswith("_")
            for obj in [getattr(mod, name)]
            if isinstance(obj, type) and issubclass(obj, BaseModel) and obj is not BaseModel
        ]
        assert len(models) > 0, (
            f"Schema module {module_name!r} has no Pydantic model classes"
        )

    def test_all_expected_schema_modules_present(self):
        expected = {
            "auth", "incident", "billing", "cad", "mdt", "nemsis",
            "fire_core", "crewlink", "patient", "patient_financial",
            "inventory", "narcotic", "transportlink", "scheduling",
            "audit", "feature_flags", "error",
        }
        actual = set(SCHEMA_MODULES)
        missing = expected - actual
        assert not missing, f"Missing expected schema modules: {missing}"
