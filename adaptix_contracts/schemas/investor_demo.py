"""Pydantic schemas for investor demo endpoints."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class InvestorLoginOut(BaseModel):
    token: str
    tenant_id: str
    role: Literal["investor_demo"]
    investor_status: str
    grant_id: str


class InvestorStatusOut(BaseModel):
    approved: bool
    grant_id: str | None = None
    expires_at: datetime | None = None
