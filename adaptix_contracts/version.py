"""
Adaptix Contracts — Version constants  v0.2.0

Single source of truth for the package version string.
Import this instead of reading __version__ from __init__.
"""

from __future__ import annotations

CONTRACT_VERSION: str = "0.2.0"

# Minimum envelope version this package can parse.
MIN_SUPPORTED_ENVELOPE_VERSION: str = "1.0"

# Downstream consumers should declare support for AT LEAST this version.
DOWNSTREAM_MIN_REQUIRED: str = "0.1.1"
