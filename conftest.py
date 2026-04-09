"""
conftest.py for adaptix-contracts test suite.

Ensures the package root is on sys.path so tests run without needing
a full pip install.  Run from the package root:

    c:/python314/python.exe -m pytest tests -q --tb=short
"""
import sys
from pathlib import Path

# Insert the package root so `adaptix_contracts` is importable
pkg_root = str(Path(__file__).parent)
if pkg_root not in sys.path:
    sys.path.insert(0, pkg_root)
