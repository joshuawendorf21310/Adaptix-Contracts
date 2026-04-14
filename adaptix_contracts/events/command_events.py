"""Command domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class DashboardAlertAcknowledgedEvent(DomainEvent):
    event_type: str = "dashboard.alert.acknowledged"
    entity_type: str = "dashboard"

    alert_id: str = ""
    acknowledged_by: str = ""
    acknowledged_at: str = ""


class DashboardAlertResolvedEvent(DomainEvent):
    event_type: str = "dashboard.alert.resolved"
    entity_type: str = "dashboard"

    alert_id: str = ""
    resolved_by: str = ""
    resolved_at: str = ""


class DashboardAlertTriggeredEvent(DomainEvent):
    event_type: str = "dashboard.alert.triggered"
    entity_type: str = "dashboard"

    alert_type: str = ""
    severity: int = 0
    description: str = ""
    triggered_at: str = ""


class DashboardKpiCalculatedEvent(DomainEvent):
    event_type: str = "dashboard.kpi.calculated"
    entity_type: str = "dashboard"

    kpi_name: str = ""
    value: str = ""
    trend: str = ""
    calculated_at: str = ""


class DashboardWidgetCustomizedEvent(DomainEvent):
    event_type: str = "dashboard.widget.customized"
    entity_type: str = "dashboard"

    user_id: str = ""
    widget_id: str = ""
    configuration: str = ""
    customized_at: str = ""


class KpiResponseTimeCalculatedEvent(DomainEvent):
    event_type: str = "kpi.response_time.calculated"
    entity_type: str = "kpi"

    incident_id: str = ""
    response_time_seconds: str = ""
    calculated_at: str = ""


class KpiTurnaroundTimeCalculatedEvent(DomainEvent):
    event_type: str = "kpi.turnaround_time.calculated"
    entity_type: str = "kpi"

    incident_id: str = ""
    turnaround_time_seconds: str = ""
    calculated_at: str = ""


class KpiUnitHourUtilizationCalculatedEvent(DomainEvent):
    event_type: str = "kpi.unit_hour_utilization.calculated"
    entity_type: str = "kpi"

    unit_id: str = ""
    shift_id: str = ""
    utilization_percent: float = 0.0
    calculated_at: str = ""


class MetricsOnSceneTimeRecordedEvent(DomainEvent):
    event_type: str = "metrics.on_scene_time.recorded"
    entity_type: str = "metrics"

    incident_id: str = ""
    unit_id: str = ""
    on_scene_time_seconds: str = ""
    recorded_at: str = ""


class MetricsResponseTimeRecordedEvent(DomainEvent):
    event_type: str = "metrics.response_time.recorded"
    entity_type: str = "metrics"

    incident_id: str = ""
    unit_id: str = ""
    response_time_seconds: str = ""
    recorded_at: str = ""


class MetricsTransportTimeRecordedEvent(DomainEvent):
    event_type: str = "metrics.transport_time.recorded"
    entity_type: str = "metrics"

    incident_id: str = ""
    unit_id: str = ""
    transport_time_seconds: str = ""
    recorded_at: str = ""


class MetricsTurnaroundTimeRecordedEvent(DomainEvent):
    event_type: str = "metrics.turnaround_time.recorded"
    entity_type: str = "metrics"

    incident_id: str = ""
    unit_id: str = ""
    turnaround_time_seconds: str = ""
    recorded_at: str = ""


class MetricsUtilizationCalculatedEvent(DomainEvent):
    event_type: str = "metrics.utilization.calculated"
    entity_type: str = "metrics"

    unit_id: str = ""
    date: str = ""
    utilization_percent: float = 0.0
    calculated_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("dashboard.alert.acknowledged", DashboardAlertAcknowledgedEvent)
_catalog.register("dashboard.alert.resolved", DashboardAlertResolvedEvent)
_catalog.register("dashboard.alert.triggered", DashboardAlertTriggeredEvent)
_catalog.register("dashboard.kpi.calculated", DashboardKpiCalculatedEvent)
_catalog.register("dashboard.widget.customized", DashboardWidgetCustomizedEvent)
_catalog.register("kpi.response_time.calculated", KpiResponseTimeCalculatedEvent)
_catalog.register("kpi.turnaround_time.calculated", KpiTurnaroundTimeCalculatedEvent)
_catalog.register("kpi.unit_hour_utilization.calculated", KpiUnitHourUtilizationCalculatedEvent)
_catalog.register("metrics.on_scene_time.recorded", MetricsOnSceneTimeRecordedEvent)
_catalog.register("metrics.response_time.recorded", MetricsResponseTimeRecordedEvent)
_catalog.register("metrics.transport_time.recorded", MetricsTransportTimeRecordedEvent)
_catalog.register("metrics.turnaround_time.recorded", MetricsTurnaroundTimeRecordedEvent)
_catalog.register("metrics.utilization.calculated", MetricsUtilizationCalculatedEvent)
