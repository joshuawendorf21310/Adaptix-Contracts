"""Adaptix Contracts — versioned shared schema authority v0.2.0"""
__version__ = "0.2.0"

from adaptix_contracts.version import CONTRACT_VERSION as CONTRACT_VERSION  # noqa: F401
from adaptix_contracts.envelope import EventEnvelope as EventEnvelope  # noqa: F401
from adaptix_contracts.registry import (
    lookup as lookup,  # noqa: F401
    lookup_required as lookup_required,  # noqa: F401
    catalog_summary as catalog_summary,  # noqa: F401
)
from adaptix_contracts.compat import (
    assert_compatible as assert_compatible,  # noqa: F401
    is_version_compatible as is_version_compatible,  # noqa: F401
)
