"""Security regression tests for gateway-signed auth contracts."""
from __future__ import annotations

import hashlib
import hmac
import time
from uuid import uuid4

import pytest
from fastapi import HTTPException, status

from adaptix_contracts.auth_contracts import GATEWAY_SHARED_SECRET_ENV, get_auth_context


def _signature(secret: str, timestamp: int, user_id: object, tenant_id: object, email: str) -> str:
    payload = f"{timestamp}.{user_id}.{tenant_id}.{email}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


@pytest.mark.asyncio
async def test_get_auth_context_fails_closed_without_gateway_secret(monkeypatch) -> None:
    monkeypatch.delenv(GATEWAY_SHARED_SECRET_ENV, raising=False)

    with pytest.raises(HTTPException) as exc_info:
        await get_auth_context(
            x_user_id=str(uuid4()),
            x_tenant_id=str(uuid4()),
            x_user_email="admin@example.test",
            x_gateway_timestamp=str(int(time.time())),
            x_gateway_signature="deadbeef",
        )

    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exc_info.value.detail["status"] == "unavailable"
    assert exc_info.value.detail["reason"] == "configuration_missing"
    assert GATEWAY_SHARED_SECRET_ENV in exc_info.value.detail["required_configuration"]


@pytest.mark.asyncio
async def test_get_auth_context_rejects_unsigned_identity_headers(monkeypatch) -> None:
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, "test-shared-secret")

    with pytest.raises(HTTPException) as exc_info:
        await get_auth_context(
            x_user_id=str(uuid4()),
            x_tenant_id=str(uuid4()),
            x_user_email="admin@example.test",
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing gateway signature headers" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_get_auth_context_accepts_valid_gateway_signature(monkeypatch) -> None:
    secret = "test-shared-secret"
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, secret)
    user_id = uuid4()
    tenant_id = uuid4()
    email = "admin@example.test"
    timestamp = int(time.time())

    auth_context = await get_auth_context(
        x_user_id=str(user_id),
        x_tenant_id=str(tenant_id),
        x_user_email=email,
        x_gateway_timestamp=str(timestamp),
        x_gateway_signature=_signature(secret, timestamp, user_id, tenant_id, email),
    )

    assert auth_context.user_id == user_id
    assert auth_context.tenant_id == tenant_id
    assert auth_context.email == email


@pytest.mark.asyncio
async def test_get_auth_context_rejects_signature_mismatch(monkeypatch) -> None:
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, "test-shared-secret")

    with pytest.raises(HTTPException) as exc_info:
        await get_auth_context(
            x_user_id=str(uuid4()),
            x_tenant_id=str(uuid4()),
            x_user_email="admin@example.test",
            x_gateway_timestamp=str(int(time.time())),
            x_gateway_signature="invalid",
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Gateway identity signature is invalid."
