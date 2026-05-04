from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class FireAROverlay(BaseModel):
    incident_id: str
    tenant_id: str
    overlay_version: str
    confidence: float | None = None
    source_attribution: list[str] = Field(default_factory=list)
    not_authoritative_warning: bool = True
    generated_at: datetime
    payload: dict[str, object] = Field(default_factory=dict)


__all__ = ["FireAROverlay"]