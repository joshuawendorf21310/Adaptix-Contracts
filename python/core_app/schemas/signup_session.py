"""Signup session Pydantic schemas (Phase 2, T234)."""
from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignupSessionCreate(BaseModel):
    """Create a new signup session."""

    model_config = ConfigDict(strict=True)

    email: EmailStr
    session_data: dict[str, Any] = Field(default_factory=dict)
    current_step: str = "start"


class SignupSessionUpdate(BaseModel):
    """Partial update for an in-progress signup session."""

    model_config = ConfigDict(strict=True)

    session_data: dict[str, Any] | None = None
    current_step: str | None = None


class SignupSessionResponse(BaseModel):
    """Public response for signup session state."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    session_data: dict[str, Any]
    current_step: str
    status: str
    expires_at: datetime
    resume_token: UUID
    created_at: datetime
    updated_at: datetime


class SignupSessionResumeRequest(BaseModel):
    """Resume a signup session by token."""

    model_config = ConfigDict(strict=True)

    resume_token: UUID
