"""
ADAPTIX GRAVITY CONTRACTS
ADAPTIX_PLATFORM_GRAVITY_COMPLETION_LOCK

Shared Pydantic contracts for all gravity-level modules.
These are the authoritative cross-service contracts.
"""

from .modules import (
    GravityModuleState,
    GravityAIRunPayload,
    GravityAuditEventPayload,
    GravityNotificationPayload,
    GravityActionPayload,
    GravityValidationResult,
    GravityErrorEnvelope,
    GravityPaginatedResponse,
)

__all__ = [
    "GravityModuleState",
    "GravityAIRunPayload",
    "GravityAuditEventPayload",
    "GravityNotificationPayload",
    "GravityActionPayload",
    "GravityValidationResult",
    "GravityErrorEnvelope",
    "GravityPaginatedResponse",
]
