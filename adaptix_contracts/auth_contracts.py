"""Gateway-trust header auth contracts for Adaptix domain services.

Domain services behind the Adaptix API gateway trust identity headers
injected after JWT validation. This module provides the canonical
AuthContext model and the get_auth_context FastAPI dependency used by
all downstream domain services.

Trusted headers injected by the gateway:
  X-User-ID     — UUID of the authenticated user (JWT ``sub`` claim)
  X-Tenant-ID   — UUID of the authenticated tenant (JWT ``tid`` claim)
  X-User-Email  — Email of the authenticated user (JWT ``email`` claim)
"""
from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from pydantic import BaseModel


class AuthContext(BaseModel):
    """Resolved gateway-injected authentication context.

    Attributes:
        user_id: UUID of the authenticated user.
        tenant_id: UUID of the authenticated tenant.
        email: Email address of the authenticated user.
    """

    user_id: UUID
    tenant_id: UUID
    email: str

    model_config = {"frozen": True}


async def get_auth_context(
    x_user_id: Annotated[str | None, Header(alias="X-User-ID")] = None,
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-ID")] = None,
    x_user_email: Annotated[str | None, Header(alias="X-User-Email")] = None,
) -> AuthContext:
    """FastAPI dependency: extract authenticated identity from gateway headers.

    The Adaptix gateway validates the caller's JWT and injects ``X-User-ID``,
    ``X-Tenant-ID``, and ``X-User-Email`` into every forwarded request. This
    dependency trusts those headers. Requests without all three headers, or with
    non-UUID values for the ID fields, are rejected with HTTP 401.

    Args:
        x_user_id: User UUID from the ``X-User-ID`` header.
        x_tenant_id: Tenant UUID from the ``X-Tenant-ID`` header.
        x_user_email: User email from the ``X-User-Email`` header.

    Returns:
        AuthContext with resolved user and tenant identity.

    Raises:
        HTTPException: 401 if any required identity header is absent or invalid.
    """
    if not x_user_id or not x_tenant_id or not x_user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing gateway identity headers (X-User-ID, X-Tenant-ID, X-User-Email).",
        )

    try:
        user_uuid = UUID(x_user_id.strip())
    except (ValueError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-ID header is not a valid UUID.",
        ) from exc

    try:
        tenant_uuid = UUID(x_tenant_id.strip())
    except (ValueError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-Tenant-ID header is not a valid UUID.",
        ) from exc

    return AuthContext(
        user_id=user_uuid,
        tenant_id=tenant_uuid,
        email=x_user_email.strip(),
    )


__all__ = ["AuthContext", "get_auth_context"]
