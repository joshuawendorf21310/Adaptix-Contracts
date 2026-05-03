"""Provider health status contracts."""
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class ProviderHealthState(str, Enum):
    CONFIGURED = "configured"
    CREDENTIAL_GATED = "credential_gated"
    LIVE_VERIFIED = "live_verified"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    NOT_CONFIGURED = "not_configured"


class ProviderHealthStatus(BaseModel):
    provider: str
    state: ProviderHealthState
    reason: Optional[str] = None
    last_checked: Optional[str] = None
    features_affected: list[str] = []


class CredentialGatedState(BaseModel):
    status: str = "credential_gated"
    provider: str
    reason: str
    configuration_path: str
    affected_modules: list[str] = []
