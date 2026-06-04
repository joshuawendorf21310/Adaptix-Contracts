"""Security regression tests for AWS API Gateway header auth contracts.

Tests verify that:
- Valid X-User-Id / X-Tenant-Id headers produce a correct AuthContext.
- Missing or invalid headers raise HTTP 401.
- X-Is-Founder flag and role normalisation work correctly.
- The AuthContext is frozen (immutable).
- AdaptixAuthContext legacy behaviour is preserved.
"""

from __future__ import annotations

import asyncio
from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from adaptix_contracts.auth_contracts import (
    AuthContext,
    get_auth_context,
)
from adaptix_contracts.auth.context import AdaptixAuthContext


# ---------------------------------------------------------------------------
# Happy-path tests
# ---------------------------------------------------------------------------

def test_get_auth_context_accepts_valid_gateway_headers() -> None:
    user_id = uuid4()
    tenant_id = uuid4()
    email = "admin@example.test"

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
            x_user_email=email,
            x_user_roles="billing_admin,user",
            x_is_founder="false",
        )
    )

    assert auth.user_id == user_id
    assert auth.tenant_id == tenant_id
    assert auth.email == email
    assert "billing_admin" in auth.roles
    assert "user" in auth.roles
    assert auth.is_founder is False


def test_get_auth_context_is_founder_flag_true() -> None:
    user_id = uuid4()
    tenant_id = uuid4()

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
            x_user_email="founder@adaptix.test",
            x_user_roles="admin",
            x_is_founder="true",
        )
    )

    assert auth.is_founder is True
    assert "founder" in auth.roles


def test_get_auth_context_founder_via_role() -> None:
    """When X-User-Roles contains 'founder', is_founder should be True."""
    user_id = uuid4()
    tenant_id = uuid4()

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
            x_user_email="founder@adaptix.test",
            x_user_roles="founder,super_admin",
            x_is_founder="false",
        )
    )

    assert auth.is_founder is True
    assert "founder" in auth.roles


def test_get_auth_context_empty_roles_default() -> None:
    user_id = uuid4()
    tenant_id = uuid4()

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
        )
    )

    assert auth.roles == []
    assert auth.is_founder is False
    assert auth.email == ""


def test_get_auth_context_whitespace_stripped() -> None:
    user_id = uuid4()
    tenant_id = uuid4()

    auth = asyncio.run(
        get_auth_context(
            x_user_id=f"  {user_id}  ",
            x_tenant_id=f"  {tenant_id}  ",
            x_user_email="  user@test.com  ",
            x_user_roles="  admin , user  ",
        )
    )

    assert auth.user_id == user_id
    assert auth.tenant_id == tenant_id
    assert "admin" in auth.roles
    assert "user" in auth.roles


# ---------------------------------------------------------------------------
# Rejection tests
# ---------------------------------------------------------------------------

def test_get_auth_context_fails_without_user_id() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=None,
                x_tenant_id=str(uuid4()),
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "X-User-Id" in str(exc_info.value.detail)


def test_get_auth_context_fails_without_tenant_id() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=str(uuid4()),
                x_tenant_id=None,
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "X-Tenant-Id" in str(exc_info.value.detail)


def test_get_auth_context_fails_with_invalid_user_id_uuid() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id="not-a-uuid",
                x_tenant_id=str(uuid4()),
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "X-User-Id" in str(exc_info.value.detail)


def test_get_auth_context_fails_with_invalid_tenant_id_uuid() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=str(uuid4()),
                x_tenant_id="not-a-uuid",
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "X-Tenant-Id" in str(exc_info.value.detail)


def test_get_auth_context_fails_with_empty_user_id() -> None:
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id="   ",
                x_tenant_id=str(uuid4()),
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


# ---------------------------------------------------------------------------
# Immutability test
# ---------------------------------------------------------------------------

def test_auth_context_is_frozen() -> None:
    user_id = uuid4()
    tenant_id = uuid4()

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
        )
    )

    with pytest.raises(Exception):
        auth.user_id = uuid4()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# AdaptixAuthContext legacy tests (must not regress)
# ---------------------------------------------------------------------------

def test_from_token_payload_rejects_missing_tenant_id() -> None:
    with pytest.raises(ValueError, match="tenant_id"):
        AdaptixAuthContext.from_token_payload(
            {
                "sub": str(uuid4()),
                "session_id": str(uuid4()),
            }
        )


def test_from_token_payload_rejects_missing_sub() -> None:
    with pytest.raises(ValueError, match="sub"):
        AdaptixAuthContext.from_token_payload(
            {
                "tenant_id": str(uuid4()),
                "session_id": str(uuid4()),
            }
        )


def test_from_token_payload_rejects_missing_session_id() -> None:
    with pytest.raises(ValueError, match="session_id"):
        AdaptixAuthContext.from_token_payload(
            {
                "tenant_id": str(uuid4()),
                "sub": str(uuid4()),
            }
        )


def test_from_token_payload_rejects_trusted_tenant_mismatch() -> None:
    with pytest.raises(ValueError, match="mismatch"):
        AdaptixAuthContext.from_token_payload(
            {
                "tenant_id": str(uuid4()),
                "sub": str(uuid4()),
                "session_id": str(uuid4()),
            },
            trusted_tenant_id=str(uuid4()),
        )


def test_from_token_payload_accepts_trusted_tenant_match() -> None:
    tenant_id = str(uuid4())
    context = AdaptixAuthContext.from_token_payload(
        {
            "tenant_id": tenant_id,
            "sub": str(uuid4()),
            "session_id": str(uuid4()),
            "roles": ["founder"],
        },
        trusted_tenant_id=tenant_id,
    )

    assert context.tenant_id == tenant_id
