"""Pydantic schemas for demo request endpoints."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class DemoRequestCreate(BaseModel):
    full_name: str
    email: EmailStr
    company: str | None = None
    role: str | None = None
    notes: str | None = None


class DemoRequestOut(BaseModel):
    id: UUID
    full_name: str
    email: str
    company: str | None = None
    role: str | None = None
    notes: str | None = None
    status: str
    requested_at: datetime

    model_config = {"from_attributes": True}
