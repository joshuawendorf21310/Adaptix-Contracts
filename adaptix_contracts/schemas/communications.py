"""Communications response schemas (Phase 2, T218).

Pydantic v2 response models for communications timeline and delivery endpoints.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class DeliverySummaryResponse(BaseModel):
    total_sent: int
    total_delivered: int
    total_failed: int
    delivery_rate_pct: float
    as_of: str | None = None


class CommunicationStatsResponse(BaseModel):
    total_messages: int
    by_channel: dict[str, int] = {}
    failed_count: int = 0
    pending_count: int = 0
    period_start: str | None = None
    period_end: str | None = None
