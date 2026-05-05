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
from adaptix_contracts.schemas.legal_execution_contracts import (
    ContractType,
    ContractStatus,
    TenantContractStatusMap,
    ContractSignatureEvent,
    ContractAccessCheckRequest,
    ContractAccessCheckResponse,
)
from adaptix_contracts.event_contracts import (
    EventSchema,
    EventMetadata,
    EventValidator,
    LocalEventConsumerRegistry,
)

__version__ = "1.0.1"

# Re-export all schema symbols at package level for convenience.
__all__ = list(_schemas.__all__)
_missing_exports = [name for name in __all__ if not hasattr(_schemas, name)]
if _missing_exports:
    raise ImportError(
        "adaptix_contracts.schemas.__all__ includes missing exports: "
        + ", ".join(sorted(_missing_exports))
    )

globals().update({name: getattr(_schemas, name) for name in _schemas.__all__})

del _schemas
