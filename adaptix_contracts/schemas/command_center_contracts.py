"""Shared command-center contracts for command execution, search, and timeline."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    """Request payload to submit a cross-domain command."""

    command_type: str = Field(min_length=1, max_length=200)
    target_domain: str = Field(min_length=1, max_length=100)
    resource_id: str | None = Field(default=None, max_length=255)
    parameters: dict[str, Any] = Field(default_factory=dict)


class CommandApprovalRequest(BaseModel):
    """Approval or rejection payload for a queued command."""

    approval_decision: str = Field(pattern="^(approved|rejected)$")
    reason: str = Field(min_length=1, max_length=2000)


class CommandExecution(BaseModel):
    """Current command execution state."""

    execution_id: Any
    command_type: str
    target_domain: str
    resource_id: str | None = None
    status: str
    result: dict[str, Any] | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None


class SearchQuery(BaseModel):
    """Cross-domain search query payload."""

    query_text: str | None = Field(default=None, max_length=500)
    domains: list[str] = Field(default_factory=list)
    resource_types: list[str] = Field(default_factory=list)
    filters: dict[str, Any] = Field(default_factory=dict)
    limit: int = Field(default=25, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class SearchResult(BaseModel):
    """A single search hit across platform domains."""

    id: str
    domain: str
    resource_type: str
    title: str
    snippet: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    matched_fields: list[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    """Search response payload for command-center queries."""

    query: str | None = None
    total_hits: int
    returned_count: int
    took_ms: int
    results: list[SearchResult] = Field(default_factory=list)


class TimelineEvent(BaseModel):
    """A unified timeline event aggregated across domains."""

    event_id: Any
    event_type: str
    source_domain: str
    occurred_at: datetime
    actor_user_id: str | None = None
    actor_name: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    resource_label: str | None = None
    summary: str
    details: dict[str, Any] | None = None


class TimelineResponse(BaseModel):
    """Aggregated timeline response payload."""

    total_events: int
    returned_count: int
    start_time: datetime | None = None
    end_time: datetime | None = None
    events: list[TimelineEvent] = Field(default_factory=list)