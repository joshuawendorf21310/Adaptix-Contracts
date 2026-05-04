from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FireAIAssessment(BaseModel):
    incident_id: str
    tenant_id: str
    summary: str
    confidence: float | None = None
    risk_level: str | None = None
    human_review_required: bool = True
    input_fields: list[str] = Field(default_factory=list)
    created_at: datetime


__all__ = ["FireAIAssessment"]