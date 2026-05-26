"""Tests for the canonical TrustSign HTTP client.

Coverage:

* Construction-time validation rejects legacy Dropbox/HelloSign hostnames.
* ``create_request`` POSTs the JSON shape the server endpoint expects.
* ``get_request_status`` parses the server response into typed model.
* ``download_archive`` returns raw bytes and surfaces 404 as
  ``TrustSignValidationError``.
* ``void_request`` + ``resend_request`` round-trip with optional bodies.
* Webhook signature verification accepts a correct HMAC and rejects
  every malformed shape (no header, wrong prefix, tampered hex, wrong
  length, wrong secret).
* 401/403 → ``TrustSignUnauthorizedError``.
* 5xx → ``TrustSignServerError`` with structured body capture.
* Network failures → ``TrustSignTransportError``.

All HTTP traffic is stubbed via ``httpx.MockTransport`` — no live calls.
"""

from __future__ import annotations

import hashlib
import hmac
import json

import httpx
import pytest

from adaptix_contracts.trustsign_client import (
    CreateRequestInput,
    SignerSpec,
    TrustSignClient,
    TrustSignClientConfig,
    TrustSignConfigurationError,
    TrustSignServerError,
    TrustSignTransportError,
    TrustSignUnauthorizedError,
    TrustSignValidationError,
)


def _cfg(
    base_url: str = "https://api.adaptixcore.com", *, secret: str | None = None
) -> TrustSignClientConfig:
    return TrustSignClientConfig(
        base_url=base_url,
        bearer_token="test-bearer-token",
        webhook_secret=secret,
    )


# ── construction-time guards ──────────────────────────────────────────────


@pytest.mark.parametrize(
    "bad_url",
    [
        "https://api.hellosign.com",
        "https://hellosign.com",
        "https://api.dropboxsign.com",
        "https://dropboxsign.com",
        "http://app.hellosign.com",
    ],
)
def test_construction_refuses_legacy_signature_hosts(bad_url: str) -> None:
    with pytest.raises(TrustSignConfigurationError) as exc:
        TrustSignClient(_cfg(bad_url))
    assert "TrustSign is the only authorized signature system" in str(exc.value)


def test_construction_refuses_unknown_scheme() -> None:
    with pytest.raises(TrustSignConfigurationError):
        TrustSignClient(_cfg("ftp://example.com"))


def test_construction_refuses_missing_hostname() -> None:
    with pytest.raises(TrustSignConfigurationError):
        TrustSignClient(_cfg("https://"))


def test_construction_accepts_canonical_gateway() -> None:
    client = TrustSignClient(_cfg("https://api.adaptixcore.com"))
    assert client is not None


def test_construction_accepts_internal_service_mesh() -> None:
    client = TrustSignClient(_cfg("http://adaptix-billing:8000"))
    assert client is not None


# ── create_request ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_request_posts_expected_body_and_returns_parsed_response() -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/v1/trustsign/requests"
        assert request.headers["Authorization"] == "Bearer test-bearer-token"
        captured["body"] = json.loads(request.content)
        return httpx.Response(
            201,
            json={
                "request_id": "req_123",
                "verification_id": "ver_abc",
                "template_id": "msa_v2",
                "template_version": "1.0",
                "purpose": "msa_signing",
                "status": "pending",
                "expires_at": "2026-06-01T00:00:00+00:00",
                "signers": [
                    {
                        "signer_id": "sig_1",
                        "email": "signer@example.com",
                        "full_name": "Alex Signer",
                        "role": "signer",
                        "signing_url": "https://api.adaptixcore.com/api/v1/trustsign/sign/tok_xyz",
                        "expires_at": "2026-06-01T00:00:00+00:00",
                    }
                ],
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            resp = await client.create_request(
                CreateRequestInput(
                    purpose="msa_signing",
                    template_id="msa_v2",
                    template_version="1.0",
                    signers=[
                        SignerSpec(
                            email="signer@example.com",
                            full_name="Alex Signer",
                            role="signer",
                        )
                    ],
                    merge_fields={"agency_name": "Acme EMS"},
                    expiration_days=14,
                )
            )

    assert resp.request_id == "req_123"
    assert resp.signers[0].signing_url.endswith("/sign/tok_xyz")
    assert captured["body"]["purpose"] == "msa_signing"
    assert captured["body"]["signers"][0]["email"] == "signer@example.com"
    assert captured["body"]["merge_fields"] == {"agency_name": "Acme EMS"}
    assert captured["body"]["expiration_days"] == 14


@pytest.mark.asyncio
async def test_create_request_4xx_raises_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            422,
            json={"detail": {"code": "trustsign_invalid_purpose", "message": "bad"}},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            with pytest.raises(TrustSignValidationError) as exc:
                await client.create_request(
                    CreateRequestInput(
                        purpose="msa_signing",
                        template_id="msa_v2",
                        signers=[
                            SignerSpec(
                                email="x@example.com",
                                full_name="x",
                                role="signer",
                            )
                        ],
                    )
                )
            assert exc.value.status_code == 422


@pytest.mark.asyncio
async def test_create_request_5xx_raises_server_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "upstream_unavailable"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            with pytest.raises(TrustSignServerError) as exc:
                await client.create_request(
                    CreateRequestInput(
                        purpose="msa_signing",
                        template_id="msa_v2",
                        signers=[
                            SignerSpec(
                                email="x@example.com",
                                full_name="x",
                                role="signer",
                            )
                        ],
                    )
                )
            assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_create_request_401_raises_unauthorized() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "no token"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            with pytest.raises(TrustSignUnauthorizedError):
                await client.create_request(
                    CreateRequestInput(
                        purpose="msa_signing",
                        template_id="msa_v2",
                        signers=[
                            SignerSpec(
                                email="x@example.com",
                                full_name="x",
                                role="signer",
                            )
                        ],
                    )
                )


@pytest.mark.asyncio
async def test_create_request_transport_error_raises_transport_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            with pytest.raises(TrustSignTransportError):
                await client.create_request(
                    CreateRequestInput(
                        purpose="msa_signing",
                        template_id="msa_v2",
                        signers=[
                            SignerSpec(
                                email="x@example.com",
                                full_name="x",
                                role="signer",
                            )
                        ],
                    )
                )


# ── get_request_status ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_request_status_parses_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/trustsign/requests/req_abc"
        return httpx.Response(
            200,
            json={
                "request_id": "req_abc",
                "verification_id": "ver_abc",
                "purpose": "baa_signing",
                "status": "signed",
                "template_id": "baa_v3",
                "template_version": "3.1",
                "created_at": "2026-05-20T00:00:00+00:00",
                "expires_at": "2026-06-03T00:00:00+00:00",
                "archived_at": "2026-05-25T00:00:00+00:00",
                "signers": [{"signer_id": "sig_a", "status": "signed"}],
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            status = await client.get_request_status("req_abc")
    assert status.status == "signed"
    assert status.archived_at == "2026-05-25T00:00:00+00:00"


# ── download_archive ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_download_archive_returns_pdf_bytes() -> None:
    pdf = b"%PDF-1.7\nfake-archive-bytes\n%%EOF"

    def handler(request: httpx.Request) -> httpx.Response:
        assert (
            request.url.path == "/api/v1/trustsign/archives/by-request/req_xyz/download"
        )
        return httpx.Response(
            200, content=pdf, headers={"content-type": "application/pdf"}
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            content = await client.download_archive("req_xyz")
    assert content == pdf


@pytest.mark.asyncio
async def test_download_archive_404_raises_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "archive_not_found"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            with pytest.raises(TrustSignValidationError) as exc:
                await client.download_archive("req_missing")
            assert exc.value.status_code == 404


# ── void + resend ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_void_request_posts_reason() -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/trustsign/requests/req_void/void"
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"status": "cancelled"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            await client.void_request("req_void", reason="caller cancelled")
    assert captured["body"] == {"reason": "caller cancelled"}


@pytest.mark.asyncio
async def test_resend_request_posts_optional_expiration() -> None:
    captured: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        return httpx.Response(200, json={"status": "pending"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as raw:
        async with TrustSignClient(_cfg(), http_client=raw) as client:
            await client.resend_request("req_resend", expiration_days=21)
    assert captured["body"] == {"expiration_days": 21}


# ── webhook signature verification ────────────────────────────────────────


def _sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def test_webhook_signature_accepts_correct_hmac() -> None:
    secret = "shared-trustsign-secret"
    body = b'{"event":"request.signed","request_id":"req_1"}'
    assert TrustSignClient.verify_webhook_signature(
        body=body, signature_header=_sign(secret, body), secret=secret
    )


def test_webhook_signature_rejects_tampered_body() -> None:
    secret = "shared-trustsign-secret"
    sig = _sign(secret, b"original")
    assert not TrustSignClient.verify_webhook_signature(
        body=b"tampered", signature_header=sig, secret=secret
    )


def test_webhook_signature_rejects_wrong_secret() -> None:
    body = b"payload"
    sig = _sign("right-secret", body)
    assert not TrustSignClient.verify_webhook_signature(
        body=body, signature_header=sig, secret="wrong-secret"
    )


def test_webhook_signature_rejects_missing_header() -> None:
    assert not TrustSignClient.verify_webhook_signature(
        body=b"payload", signature_header=None, secret="anything"
    )


def test_webhook_signature_rejects_missing_secret() -> None:
    assert not TrustSignClient.verify_webhook_signature(
        body=b"payload", signature_header="sha256=" + "a" * 64, secret=""
    )


def test_webhook_signature_rejects_wrong_prefix() -> None:
    body = b"payload"
    expected_hex = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert not TrustSignClient.verify_webhook_signature(
        body=body, signature_header="md5=" + expected_hex, secret="secret"
    )


def test_webhook_signature_rejects_short_hex() -> None:
    assert not TrustSignClient.verify_webhook_signature(
        body=b"payload", signature_header="sha256=abc", secret="secret"
    )
