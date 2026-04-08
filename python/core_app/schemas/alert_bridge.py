"""Pydantic schemas for Grafana alert webhook bridge."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GrafanaAlert(BaseModel):
    """Single alert item within a Grafana webhook payload."""

    status: str = ""  # "firing" or "resolved"
    labels: dict[str, str] = Field(default_factory=dict)
    annotations: dict[str, str] = Field(default_factory=dict)
    startsAt: str = ""
    endsAt: str = ""
    generatorURL: str = ""
    fingerprint: str = ""
    silenceURL: str = ""
    dashboardURL: str = ""
    panelURL: str = ""
    values: dict[str, Any] = Field(default_factory=dict)


class GrafanaWebhookPayload(BaseModel):
    """Top-level Grafana alerting webhook body (unified alerting format)."""

    receiver: str = ""
    status: str = ""  # "firing" or "resolved"
    orgId: int = 0
    alerts: list[GrafanaAlert] = Field(default_factory=list)
    groupLabels: dict[str, str] = Field(default_factory=dict)
    commonLabels: dict[str, str] = Field(default_factory=dict)
    commonAnnotations: dict[str, str] = Field(default_factory=dict)
    externalURL: str = ""
    version: str = ""
    groupKey: str = ""
    truncatedAlerts: int = 0
    title: str = ""
    state: str = ""
    message: str = ""
