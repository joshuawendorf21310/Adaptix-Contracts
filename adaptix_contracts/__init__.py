"""Adaptix contracts package containing shared cross-domain schema definitions.

This package provides typed contract definitions for cross-domain communication
across the Adaptix polyrepo platform.

Import patterns:
    # Import all schemas
    from adaptix_contracts.schemas import *

    # Import specific schemas
    from adaptix_contracts.schemas import (
        ClaimContract,
        EpcrChartCreatedEvent,
        TransportRequestCreate,
    )
"""

from adaptix_contracts import schemas as _schemas

__version__ = "1.0.1"

# Re-export all schema symbols at package level for convenience.
__all__ = list(_schemas.__all__)
globals().update({name: getattr(_schemas, name) for name in __all__})

del _schemas
