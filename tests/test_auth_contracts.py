"""Security regression tests for gateway-signed auth contracts.

Tests cover both verification modes:
- HMAC-SHA256 (backward compat): X-Adaptix-Gateway-Signature header
- RS256 JWT (enterprise): X-Adaptix-Gateway-Context header
"""

from __future__ import annotations

import asyncio
import hashlib
import hmac
import time
from uuid import uuid4

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import HTTPException, status

from adaptix_contracts.auth_contracts import (
    GATEWAY_SHARED_SECRET_ENV,
    GATEWAY_PUBLIC_KEY_ENV,
    AuthContext,
    build_gateway_context_jwt,
    get_auth_context,
)
from adaptix_contracts.auth.context import AdaptixAuthContext


# ---------------------------------------------------------------------------
# Test key helpers
# ---------------------------------------------------------------------------

def _generate_rsa_key_pair() -> tuple[str, str]:
    """Return (private_key_pem, public_key_pem) for test signing."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    return private_pem, public_pem


def _hmac_signature(
    secret: str, timestamp: int, user_id: object, tenant_id: object, email: str
) -> str:
    payload = f"{timestamp}.{user_id}.{tenant_id}.{email}".encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


# ---------------------------------------------------------------------------
# HMAC backward-compat tests (existing behaviour must not regress)
# ---------------------------------------------------------------------------

def test_get_auth_context_fails_closed_without_gateway_secret(monkeypatch) -> None:
    monkeypatch.delenv(GATEWAY_SHARED_SECRET_ENV, raising=False)

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=str(uuid4()),
                x_tenant_id=str(uuid4()),
                x_user_email="admin@example.test",
                x_gateway_timestamp=str(int(time.time())),
                x_gateway_signature="deadbeef",
            )
        )

    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert exc_info.value.detail["status"] == "unavailable"
    assert exc_info.value.detail["reason"] == "configuration_missing"
    assert GATEWAY_SHARED_SECRET_ENV in exc_info.value.detail["required_configuration"]


def test_get_auth_context_rejects_unsigned_identity_headers(monkeypatch) -> None:
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, "test-shared-secret")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=str(uuid4()),
                x_tenant_id=str(uuid4()),
                x_user_email="admin@example.test",
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing gateway signature headers" in str(exc_info.value.detail)


def test_get_auth_context_accepts_valid_gateway_signature(monkeypatch) -> None:
    secret = "test-shared-secret"
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, secret)
    user_id = uuid4()
    tenant_id = uuid4()
    email = "admin@example.test"
    timestamp = int(time.time())

    auth_context = asyncio.run(
        get_auth_context(
            x_user_id=str(user_id),
            x_tenant_id=str(tenant_id),
            x_user_email=email,
            x_gateway_timestamp=str(timestamp),
            x_gateway_signature=_hmac_signature(
                secret, timestamp, user_id, tenant_id, email
            ),
        )
    )

    assert auth_context.user_id == user_id
    assert auth_context.tenant_id == tenant_id
    assert auth_context.email == email
    assert auth_context.roles == []


def test_get_auth_context_rejects_signature_mismatch(monkeypatch) -> None:
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, "test-shared-secret")

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(
            get_auth_context(
                x_user_id=str(uuid4()),
                x_tenant_id=str(uuid4()),
                x_user_email="admin@example.test",
                x_gateway_timestamp=str(int(time.time())),
                x_gateway_signature="invalid",
            )
        )

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Gateway identity signature is invalid."


# ---------------------------------------------------------------------------
# RS256 JWT enterprise mode tests
# ---------------------------------------------------------------------------

def test_rs256_jwt_accepted_over_hmac_when_both_present(monkeypatch) -> None:
    """X-Adaptix-Gateway-Context JWT takes priority over HMAC headers."""
    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)
    monkeypatch.setenv(GATEWAY_SHARED_SECRET_ENV, "should-not-be-used")

    user_id = uuid4()
    tenant_id = uuid4()
    email = "founder@adaptix.test"
    roles = ["founder", "admin"]

    jwt_token = build_gateway_context_jwt(
        user_id=user_id,
        tenant_id=tenant_id,
        email=email,
        roles=roles,
        private_key_pem=private_pem,
        issuer="adaptix-gateway",
    )

    auth = asyncio.run(
        get_auth_context(
            x_user_id=str(uuid4()),
            x_tenant_id=str(uuid4()),
            x_user_email="different@wrong.test",
            x_gateway_timestamp=str(int(time.time())),
            x_gateway_signature="wrong-sig",
            x_gateway_context=jwt_token,
        )
    )

    assert auth.user_id == user_id
    assert auth.tenant_id == tenant_id
    assert auth.email == email
    assert "founder" in auth.roles
    assert "admin" in auth.roles


def test_rs256_jwt_gateway_issuer_accepted(monkeypatch) -> None:
    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)

    user_id = uuid4()
    tenant_id = uuid4()

    jwt_token = build_gateway_context_jwt(
        user_id=user_id,
        tenant_id=tenant_id,
        email="user@test.com",
        roles=["operator"],
        private_key_pem=private_pem,
        issuer="adaptix-gateway",
    )

    auth = asyncio.run(get_auth_context(x_gateway_context=jwt_token))
    assert auth.user_id == user_id
    assert auth.tenant_id == tenant_id


def test_rs256_jwt_core_issuer_accepted(monkeypatch) -> None:
    """adaptix-core issuer is trusted for direct Core-to-service calls."""
    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)

    user_id = uuid4()
    tenant_id = uuid4()

    jwt_token = build_gateway_context_jwt(
        user_id=user_id,
        tenant_id=tenant_id,
        email="core@internal",
        roles=[],
        private_key_pem=private_pem,
        issuer="adaptix-core",
    )

    auth = asyncio.run(get_auth_context(x_gateway_context=jwt_token))
    assert auth.user_id == user_id
    assert auth.tenant_id == tenant_id


def test_rs256_jwt_rejects_untrusted_issuer(monkeypatch) -> None:
    import jwt as pyjwt

    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)

    now = int(time.time())
    bad_token = pyjwt.encode(
        {"iss": "evil-service", "sub": str(uuid4()), "tid": str(uuid4()), "exp": now + 60, "iat": now},
        private_pem,
        algorithm="RS256",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_auth_context(x_gateway_context=bad_token))

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "evil-service" in str(exc_info.value.detail)


def test_rs256_jwt_rejects_expired_token(monkeypatch) -> None:
    import jwt as pyjwt

    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)

    past = int(time.time()) - 120
    expired_token = pyjwt.encode(
        {"iss": "adaptix-gateway", "sub": str(uuid4()), "tid": str(uuid4()), "exp": past, "iat": past - 60},
        private_pem,
        algorithm="RS256",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_auth_context(x_gateway_context=expired_token))

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_rs256_jwt_rejects_wrong_key(monkeypatch) -> None:
    private_pem1, _ = _generate_rsa_key_pair()
    _, public_pem2 = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem2)

    jwt_token = build_gateway_context_jwt(
        user_id=uuid4(),
        tenant_id=uuid4(),
        email="user@test.com",
        roles=[],
        private_key_pem=private_pem1,
        issuer="adaptix-gateway",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_auth_context(x_gateway_context=jwt_token))

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_rs256_jwt_falls_back_to_adaptix_jwt_public_key(monkeypatch) -> None:
    """ADAPTIX_JWT_PUBLIC_KEY is accepted as fallback when ADAPTIX_GATEWAY_PUBLIC_KEY absent."""
    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.delenv(GATEWAY_PUBLIC_KEY_ENV, raising=False)
    monkeypatch.setenv("ADAPTIX_JWT_PUBLIC_KEY", public_pem)

    user_id = uuid4()
    tenant_id = uuid4()

    jwt_token = build_gateway_context_jwt(
        user_id=user_id,
        tenant_id=tenant_id,
        email="user@test.com",
        roles=["billing_admin"],
        private_key_pem=private_pem,
        issuer="adaptix-gateway",
    )

    auth = asyncio.run(get_auth_context(x_gateway_context=jwt_token))
    assert auth.user_id == user_id
    assert "billing_admin" in auth.roles


def test_rs256_jwt_503_when_no_public_key_configured(monkeypatch) -> None:
    private_pem, _ = _generate_rsa_key_pair()
    monkeypatch.delenv(GATEWAY_PUBLIC_KEY_ENV, raising=False)
    monkeypatch.delenv("ADAPTIX_JWT_PUBLIC_KEY", raising=False)

    jwt_token = build_gateway_context_jwt(
        user_id=uuid4(),
        tenant_id=uuid4(),
        email="user@test.com",
        roles=[],
        private_key_pem=private_pem,
        issuer="adaptix-gateway",
    )

    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_auth_context(x_gateway_context=jwt_token))

    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert GATEWAY_PUBLIC_KEY_ENV in exc_info.value.detail["required_configuration"]


def test_rs256_jwt_roles_normalized_from_comma_string(monkeypatch) -> None:
    """Roles as comma-separated string are normalised to list."""
    import jwt as pyjwt

    private_pem, public_pem = _generate_rsa_key_pair()
    monkeypatch.setenv(GATEWAY_PUBLIC_KEY_ENV, public_pem)

    now = int(time.time())
    token = pyjwt.encode(
        {
            "iss": "adaptix-gateway",
            "sub": str(uuid4()),
            "tid": str(uuid4()),
            "email": "x@test.com",
            "roles": "founder,admin",
            "exp": now + 60,
            "iat": now,
        },
        private_pem,
        algorithm="RS256",
    )

    auth = asyncio.run(get_auth_context(x_gateway_context=token))
    assert "founder" in auth.roles
    assert "admin" in auth.roles


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
