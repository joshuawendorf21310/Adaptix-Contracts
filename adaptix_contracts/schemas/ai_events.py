from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AiTaskRequestedEvent(BaseModel):
    event_type: str = "adaptix.ai.task.requested"
    tenant_id: str
    actor_id: str
    actor_role: str
    module: str
    task_type: str
    priority: str
    correlation_id: str
    timestamp: str
    context: dict[str, Any] = Field(default_factory=dict)


class AiTaskCompletedEvent(BaseModel):
    event_type: str = "adaptix.ai.task.completed"
    tenant_id: str
    actor_id: str
    module: str
    task_type: str
    correlation_id: str
    timestamp: str
    model_id: str
    latency_ms: int
    output_summary: dict[str, Any] = Field(default_factory=dict)


class AiTaskFailedEvent(BaseModel):
    event_type: str = "adaptix.ai.task.failed"
    tenant_id: str
    actor_id: str
    module: str
    task_type: str
    correlation_id: str
    timestamp: str
    error_code: str
    error_message: str
