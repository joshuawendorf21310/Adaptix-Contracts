"""Auth and tenancy domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from pydantic import Field

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class TenantCreatedEvent(DomainEvent):
    event_type: str = "tenant.created"
    entity_type: str = "tenant"

    name: str = ""
    service_lines: list[str] = Field(default_factory=list)


class TenantSuspendedEvent(DomainEvent):
    event_type: str = "tenant.suspended"
    entity_type: str = "tenant"

    reason: str = ""


class UserCreatedEvent(DomainEvent):
    event_type: str = "user.created"
    entity_type: str = "user"

    user_id: str = ""
    email: str = ""
    roles: list[str] = Field(default_factory=list)


class UserDeactivatedEvent(DomainEvent):
    event_type: str = "user.deactivated"
    entity_type: str = "user"

    user_id: str = ""


class FeatureFlagToggledEvent(DomainEvent):
    event_type: str = "feature_flag.toggled"
    entity_type: str = "feature_flag"

    flag_name: str = ""
    enabled: bool = False


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("tenant.created", TenantCreatedEvent)
_catalog.register("tenant.suspended", TenantSuspendedEvent)
_catalog.register("user.created", UserCreatedEvent)
_catalog.register("user.deactivated", UserDeactivatedEvent)
_catalog.register("feature_flag.toggled", FeatureFlagToggledEvent)
class ImpersonationEndedEvent(DomainEvent):
    event_type: str = "impersonation.ended"
    entity_type: str = "impersonation"
    impersonator_id: str = ""
    target_user_id: str = ""
    duration_seconds: str = ""
class ImpersonationStartedEvent(DomainEvent):
    event_type: str = "impersonation.started"
    entity_type: str = "impersonation"
    impersonator_id: str = ""
    target_user_id: str = ""
    tenant_id: str = ""
    reason: str = ""
class LoginFailedEvent(DomainEvent):
    event_type: str = "login.failed"
    entity_type: str = "login"
    email: str = ""
    ip_address: str = ""
    failure_reason: str = ""
class LoginSuccessfulEvent(DomainEvent):
    event_type: str = "login.successful"
    entity_type: str = "login"
    user_id: str = ""
    tenant_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
class LogoutCompletedEvent(DomainEvent):
    event_type: str = "logout.completed"
    entity_type: str = "logout"
    user_id: str = ""
    session_id: str = ""
class MfaChallengedEvent(DomainEvent):
    event_type: str = "mfa.challenged"
    entity_type: str = "mfa"
    user_id: str = ""
    session_id: str = ""
    challenge_method: str = ""
class MfaDisabledEvent(DomainEvent):
    event_type: str = "mfa.disabled"
    entity_type: str = "mfa"
    user_id: str = ""
    tenant_id: str = ""
class MfaEnabledEvent(DomainEvent):
    event_type: str = "mfa.enabled"
    entity_type: str = "mfa"
    user_id: str = ""
    tenant_id: str = ""
    mfa_method: str = ""
class MfaFailedEvent(DomainEvent):
    event_type: str = "mfa.failed"
    entity_type: str = "mfa"
    user_id: str = ""
    session_id: str = ""
    failure_reason: str = ""
class MfaVerifiedEvent(DomainEvent):
    event_type: str = "mfa.verified"
    entity_type: str = "mfa"
    user_id: str = ""
    session_id: str = ""
    verification_method: str = ""
class PasswordChangedEvent(DomainEvent):
    event_type: str = "password.changed"
    entity_type: str = "password"
    user_id: str = ""
    tenant_id: str = ""
    changed_by: str = ""
class PasswordResetCompletedEvent(DomainEvent):
    event_type: str = "password.reset_completed"
    entity_type: str = "password"
    user_id: str = ""
    reset_token_id: str = ""
class PasswordResetRequestedEvent(DomainEvent):
    event_type: str = "password.reset_requested"
    entity_type: str = "password"
    user_id: str = ""
    email: str = ""
    reset_token_id: str = ""
class PermissionGrantedEvent(DomainEvent):
    event_type: str = "permission.granted"
    entity_type: str = "permission"
    user_id: str = ""
    tenant_id: str = ""
    permission: str = ""
    resource_id: str = ""
class PermissionRevokedEvent(DomainEvent):
    event_type: str = "permission.revoked"
    entity_type: str = "permission"
    user_id: str = ""
    tenant_id: str = ""
    permission: str = ""
    resource_id: str = ""
class RoleAssignedEvent(DomainEvent):
    event_type: str = "role.assigned"
    entity_type: str = "role"
    user_id: str = ""
    tenant_id: str = ""
    role: str = ""
    assigned_by: str = ""
class RoleRevokedEvent(DomainEvent):
    event_type: str = "role.revoked"
    entity_type: str = "role"
    user_id: str = ""
    tenant_id: str = ""
    role: str = ""
    revoked_by: str = ""
class SessionCreatedEvent(DomainEvent):
    event_type: str = "session.created"
    entity_type: str = "session"
    session_id: str = ""
    user_id: str = ""
    tenant_id: str = ""
    ip_address: str = ""
    user_agent: str = ""
class SessionExpiredEvent(DomainEvent):
    event_type: str = "session.expired"
    entity_type: str = "session"
    session_id: str = ""
    user_id: str = ""
class SessionTerminatedEvent(DomainEvent):
    event_type: str = "session.terminated"
    entity_type: str = "session"
    session_id: str = ""
    user_id: str = ""
    termination_reason: str = ""
class TokenIssuedEvent(DomainEvent):
    event_type: str = "token.issued"
    entity_type: str = "token"
    token_id: str = ""
    user_id: str = ""
    tenant_id: str = ""
    token_type: str = ""
    expires_at: str = ""
class TokenRefreshedEvent(DomainEvent):
    event_type: str = "token.refreshed"
    entity_type: str = "token"
    old_token_id: str = ""
    new_token_id: str = ""
    user_id: str = ""
class TokenRevokedEvent(DomainEvent):
    event_type: str = "token.revoked"
    entity_type: str = "token"
    token_id: str = ""
    user_id: str = ""
    revocation_reason: str = ""
_catalog.register("impersonation.ended", ImpersonationEndedEvent)
_catalog.register("impersonation.started", ImpersonationStartedEvent)
_catalog.register("login.failed", LoginFailedEvent)
_catalog.register("login.successful", LoginSuccessfulEvent)
_catalog.register("logout.completed", LogoutCompletedEvent)
_catalog.register("mfa.challenged", MfaChallengedEvent)
_catalog.register("mfa.disabled", MfaDisabledEvent)
_catalog.register("mfa.enabled", MfaEnabledEvent)
_catalog.register("mfa.failed", MfaFailedEvent)
_catalog.register("mfa.verified", MfaVerifiedEvent)
_catalog.register("password.changed", PasswordChangedEvent)
_catalog.register("password.reset_completed", PasswordResetCompletedEvent)
_catalog.register("password.reset_requested", PasswordResetRequestedEvent)
_catalog.register("permission.granted", PermissionGrantedEvent)
_catalog.register("permission.revoked", PermissionRevokedEvent)
_catalog.register("role.assigned", RoleAssignedEvent)
_catalog.register("role.revoked", RoleRevokedEvent)
_catalog.register("session.created", SessionCreatedEvent)
_catalog.register("session.expired", SessionExpiredEvent)
_catalog.register("session.terminated", SessionTerminatedEvent)
_catalog.register("token.issued", TokenIssuedEvent)
_catalog.register("token.refreshed", TokenRefreshedEvent)
_catalog.register("token.revoked", TokenRevokedEvent)
