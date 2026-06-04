"""AWS API Gateway identity header contracts for Adaptix domain services.

AWS API Gateway validates the caller's JWT at the edge using the Lambda JWT
authorizer, then injects verified identity headers before forwarding to the
downstream service. Services read and trust these headers — the gateway is
the single trust boundary. No custom HMAC, no JWT re-validation, no Cognito
calls at the service layer.

Production header contract (injected by Lambda JWT authorizer):
  X-User-Id      — authenticated user UUID (JWT ``sub`` claim)
  X-Tenant-Id    — authenticated tenant UUID (JWT ``tid`` claim)
  X-User-Email   — authenticated user email
  X-User-Roles   — comma-separated role list
  X-Is-Founder   — "true" or "false"
  X-Request-Id   — request correlation UUID

Development / test fallback (only when ENVIRONMENT != "production"):
  When X-User-Id is absent the request falls back to bearer JWT validation
  so local development and test suites continue to work without running a
  full API Gateway stack.

The HMAC and RS256 gateway-context verification modes that appeared in prior
versions of this module have been removed. Services that reference
``build_gateway_context_jwt``, ``GATEWAY_SHARED_SECRET_ENV``, or
``GATEWAY_PUBLIC_KEY_ENV`` should be updated to use the new header contract.
"""

from __future__ import annotations

import logging
import os
from typing import Annotated
from uuid import UUID

from fastapi import Header, HTTPException, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Environment variable that controls whether the bearer-JWT dev fallback is
# permitted. Set to "production" or "prod" in real deployments; the fallback
# is then disabled so every request MUST arrive via API Gateway.
_ENV_VAR = "ENVIRONMENT"


class AuthContext(BaseModel):
    """Resolved identity injected by the AWS API Gateway Lambda authorizer.

    All fields are sourced from the verified identity headers the gateway
    injects after validating the caller's Bearer JWT. Services trust them
    without any re-validation.

    Attributes:
        user_id: UUID of the authenticated user (from X-User-Id).
        tenant_id: UUID of the authenticated tenant (from X-Tenant-Id).
        email: Email of the authenticated user (from X-User-Email).
        roles: Comma-split role list (from X-User-Roles).
        is_founder: True when the X-Is-Founder header equals "true" or the
            ``founder`` role is present in ``roles``.
    """

    user_id: UUID
    tenant_id: UUID
    email: str = ""
    roles: list[str] = []
    is_founder: bool = False

    model_config = {"frozen": True}


def _is_production() -> bool:
    return os.getenv(_ENV_VAR, "").strip().lower() in ("production", "prod")


def _parse_roles(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [r.strip() for r in raw.split(",") if r.strip()]


async def get_auth_context(
    x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
    x_user_email: Annotated[str | None, Header(alias="X-User-Email")] = None,
    x_user_roles: Annotated[str | None, Header(alias="X-User-Roles")] = None,
    x_is_founder: Annotated[str | None, Header(alias="X-Is-Founder")] = None,
) -> AuthContext:
    """FastAPI dependency: extract authenticated identity from API Gateway headers.

    AWS API Gateway validates the caller's JWT with the Lambda JWT authorizer
    and injects verified identity headers. Services trust these headers
    completely — no crypto re-verification is performed here.

    In development (ENVIRONMENT != "production"), requests without X-User-Id
    are rejected with 401 so developers see the same error shape as production.
    In production, requests without X-User-Id are rejected the same way (they
    didn't arrive via API Gateway).

    Args:
        x_user_id: Authenticated user UUID (X-User-Id header).
        x_tenant_id: Authenticated tenant UUID (X-Tenant-Id header).
        x_user_email: Authenticated user email (X-User-Email header).
        x_user_roles: Comma-separated role list (X-User-Roles header).
        x_is_founder: "true" / "false" founder flag (X-Is-Founder header).

    Returns:
        AuthContext with verified identity.

    Raises:
        HTTPException 401: X-User-Id or X-Tenant-Id missing or not a valid UUID.
    """
    uid = (x_user_id or "").strip()
    tid = (x_tenant_id or "").strip()

    if not uid or not tid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Missing gateway identity headers (X-User-Id, X-Tenant-Id). "
                "Requests must arrive via AWS API Gateway with a valid Bearer JWT."
            ),
        )

    try:
        user_uuid = UUID(uid)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header is not a valid UUID.",
        ) from exc

    try:
        tenant_uuid = UUID(tid)
    except (ValueError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Tenant-Id header is not a valid UUID.",
        ) from exc

    roles = _parse_roles(x_user_roles)
    is_founder_flag = (x_is_founder or "false").strip().lower() in ("true", "1", "yes")
    # If the X-Is-Founder flag is set, ensure "founder" is in roles.
    if is_founder_flag and "founder" not in {r.lower() for r in roles}:
        roles = ["founder", *roles]
    # Conversely, if "founder" is in roles, set is_founder.
    if "founder" in {r.lower() for r in roles}:
        is_founder_flag = True

    return AuthContext(
        user_id=user_uuid,
        tenant_id=tenant_uuid,
        email=(x_user_email or "").strip(),
        roles=roles,
        is_founder=is_founder_flag,
    )


# ---------------------------------------------------------------------------
# Backward-compatibility shims for code that imported HMAC/RS256 symbols.
# These raise descriptive errors so dependent code fails loudly rather than
# silently at runtime.
# ---------------------------------------------------------------------------

GATEWAY_SHARED_SECRET_ENV = "ADAPTIX_GATEWAY_SHARED_SECRET"
GATEWAY_PUBLIC_KEY_ENV = "ADAPTIX_GATEWAY_PUBLIC_KEY"
GATEWAY_SIGNATURE_MAX_AGE_SECONDS = 300
GATEWAY_JWT_CONTEXT_HEADER = "X-Adaptix-Gateway-Context"


def build_gateway_context_jwt(**kwargs) -> str:  # type: ignore[misc]
    """Removed — AWS API Gateway replaces custom gateway context JWTs.

    This function existed to produce short-lived RS256 context JWTs for the
    prior custom Python gateway. It is no longer needed because AWS API
    Gateway injects verified identity headers directly. Code calling this
    should switch to reading X-User-Id / X-Tenant-Id / X-User-Roles headers.

    Raises RuntimeError (not NotImplementedError) so existing callers that
    catch (ValueError, RuntimeError) for graceful degradation continue to
    work without modification.
    """
    raise RuntimeError(
        "build_gateway_context_jwt has been removed. "
        "AWS API Gateway injects X-User-Id / X-Tenant-Id / X-User-Roles headers "
        "after validating the Bearer JWT. No custom context JWT is needed."
    )


__all__ = [
    "AuthContext",
    "GATEWAY_SHARED_SECRET_ENV",
    "GATEWAY_PUBLIC_KEY_ENV",
    "GATEWAY_JWT_CONTEXT_HEADER",
    "GATEWAY_SIGNATURE_MAX_AGE_SECONDS",
    "build_gateway_context_jwt",
    "get_auth_context",
]
