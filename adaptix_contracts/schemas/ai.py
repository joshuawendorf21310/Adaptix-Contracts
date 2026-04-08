from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class IncidentSummaryRequest(BaseModel):
    correlation_id: str
    incident_id: str
    incident_timeline: list[dict[str, Any]] = Field(default_factory=list)
    units: list[dict[str, Any]] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class NarrativeGenerationRequest(BaseModel):
    correlation_id: str
    incident_id: str
    dispatch_text: str = ""
    scene_notes: list[str] = Field(default_factory=list)
    patient_findings: dict[str, Any] = Field(default_factory=dict)
    interventions: list[str] = Field(default_factory=list)
    transport_notes: list[str] = Field(default_factory=list)


class DeploymentRecommendationRequest(BaseModel):
    correlation_id: str
    zone_id: str
    active_units: list[dict[str, Any]] = Field(default_factory=list)
    pending_calls: list[dict[str, Any]] = Field(default_factory=list)
    standby_posts: list[dict[str, Any]] = Field(default_factory=list)
    constraints: dict[str, Any] = Field(default_factory=dict)


class GenericAiTaskRequest(BaseModel):
    correlation_id: str
    module: str
    task_type: str
    priority: str = "background"
    context: dict[str, Any] = Field(default_factory=dict)
    max_tokens: int | None = None
    temperature: float | None = None


class AiHealthResponse(BaseModel):
    status: str
    ai_enabled: bool
    provider: str
    bedrock_region: str
