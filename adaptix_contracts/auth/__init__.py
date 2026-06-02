"""Adaptix auth context contracts."""

from adaptix_contracts.auth.context import (
    AdaptixRole,
    AdaptixRoleSet,
    AdaptixTenantContext,
    AdaptixAuthContext,
    AdaptixServiceContext,
    AdaptixSignedInternalContext,
)
from adaptix_contracts.auth.module_entitlement_gate import (
    require_module_entitlement,
)

__all__ = [
    "AdaptixRole",
    "AdaptixRoleSet",
    "AdaptixTenantContext",
    "AdaptixAuthContext",
    "AdaptixServiceContext",
    "AdaptixSignedInternalContext",
    "require_module_entitlement",
]
