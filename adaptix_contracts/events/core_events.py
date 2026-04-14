"""Core platform domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class ConfigUpdatedEvent(DomainEvent):
    event_type: str = "config.updated"
    entity_type: str = "config"
    config_key: str = ""
    previous_value: str = ""
    new_value: str = ""
    updated_by: str = ""
class ConsentRecordedEvent(DomainEvent):
    event_type: str = "consent.recorded"
    entity_type: str = "consent"
    user_id: str = ""
    consent_type: str = ""
    consent_version: str = ""
    granted: str = ""
    recorded_at: str = ""
class ConsentWithdrawnEvent(DomainEvent):
    event_type: str = "consent.withdrawn"
    entity_type: str = "consent"
    user_id: str = ""
    consent_type: str = ""
    withdrawn_at: str = ""
class CrmContactSyncedEvent(DomainEvent):
    event_type: str = "crm.contact.synced"
    entity_type: str = "crm"
    contact_id: str = ""
    crm_system: str = ""
    sync_direction: str = ""
    synced_at: str = ""
class DataDeletionCompletedEvent(DomainEvent):
    event_type: str = "data.deletion.completed"
    entity_type: str = "data"
    request_id: str = ""
    records_deleted: str = ""
    completed_at: str = ""
class DataDeletionRequestedEvent(DomainEvent):
    event_type: str = "data.deletion.requested"
    entity_type: str = "data"
    request_id: str = ""
    user_id: str = ""
    data_scope: str = ""
    requested_at: str = ""
class DataExportCompletedEvent(DomainEvent):
    event_type: str = "data.export.completed"
    entity_type: str = "data"
    export_id: str = ""
    file_url: str = ""
    record_count: int = 0
    completed_at: str = ""
class DataExportRequestedEvent(DomainEvent):
    event_type: str = "data.export.requested"
    entity_type: str = "data"
    export_id: str = ""
    user_id: str = ""
    data_type: str = ""
    requested_at: str = ""
class DeviceRegisteredEvent(DomainEvent):
    event_type: str = "device.registered"
    entity_type: str = "device"
    device_id: str = ""
    user_id: str = ""
    tenant_id: str = ""
    device_type: str = ""
    device_name: str = ""
class DeviceTrustRevokedEvent(DomainEvent):
    event_type: str = "device.trust_revoked"
    entity_type: str = "device"
    device_id: str = ""
    user_id: str = ""
    revocation_reason: str = ""
class DeviceUnregisteredEvent(DomainEvent):
    event_type: str = "device.unregistered"
    entity_type: str = "device"
    device_id: str = ""
    user_id: str = ""
class ErrorRateElevatedEvent(DomainEvent):
    event_type: str = "error.rate.elevated"
    entity_type: str = "error"
    service_name: str = ""
    error_rate: str = ""
    threshold: str = ""
    detected_at: str = ""
class ModuleStatusChangedEvent(DomainEvent):
    event_type: str = "module.status.changed"
    entity_type: str = "module"
    module_name: str = ""
    previous_status: str = ""
    new_status: str = ""
    health_score: float = 0.0
class NotificationBatchCreatedEvent(DomainEvent):
    event_type: str = "notification.batch.created"
    entity_type: str = "notification"
    batch_id: str = ""
    notification_type: str = ""
    recipient_count: int = 0
    created_at: str = ""
class NotificationBatchSentEvent(DomainEvent):
    event_type: str = "notification.batch.sent"
    entity_type: str = "notification"
    batch_id: str = ""
    sent_count: int = 0
    failed_count: int = 0
    sent_at: str = ""
class NotificationCreatedEvent(DomainEvent):
    event_type: str = "notification.created"
    entity_type: str = "notification"
    notification_id: str = ""
    user_id: str = ""
    notification_type: str = ""
    title: str = ""
    created_at: str = ""
class NotificationDismissedEvent(DomainEvent):
    event_type: str = "notification.dismissed"
    entity_type: str = "notification"
    notification_id: str = ""
    user_id: str = ""
    dismissed_at: str = ""
class NotificationReadEvent(DomainEvent):
    event_type: str = "notification.read"
    entity_type: str = "notification"
    notification_id: str = ""
    user_id: str = ""
    read_at: str = ""
class ReportExportedEvent(DomainEvent):
    event_type: str = "report.exported"
    entity_type: str = "report"
    report_id: str = ""
    export_format: str = ""
    file_url: str = ""
    exported_at: str = ""
class ReportGeneratedEvent(DomainEvent):
    event_type: str = "report.generated"
    entity_type: str = "report"
    report_id: str = ""
    report_type: str = ""
    tenant_id: str = ""
    generated_by: str = ""
    generated_at: str = ""
class ReportScheduledEvent(DomainEvent):
    event_type: str = "report.scheduled"
    entity_type: str = "report"
    schedule_id: str = ""
    report_type: str = ""
    frequency: str = ""
    recipients: str = ""
    scheduled_by: str = ""
class SecurityBreachContainedEvent(DomainEvent):
    event_type: str = "security.breach.contained"
    entity_type: str = "security"
    breach_id: str = ""
    containment_actions: str = ""
    contained_by: str = ""
    contained_at: str = ""
class SecurityBreachDetectedEvent(DomainEvent):
    event_type: str = "security.breach.detected"
    entity_type: str = "security"
    breach_id: str = ""
    breach_type: str = ""
    severity: int = 0
    affected_resources: str = ""
    detected_at: str = ""
class SecurityIpBlockedEvent(DomainEvent):
    event_type: str = "security.ip_blocked"
    entity_type: str = "security"
    ip_address: str = ""
    block_reason: str = ""
    blocked_at: str = ""
    block_duration: str = ""
class SecurityIpUnblockedEvent(DomainEvent):
    event_type: str = "security.ip_unblocked"
    entity_type: str = "security"
    ip_address: str = ""
    unblocked_by: str = ""
    unblocked_at: str = ""
class SecurityRateLimitExceededEvent(DomainEvent):
    event_type: str = "security.rate_limit.exceeded"
    entity_type: str = "security"
    user_id: str = ""
    endpoint: str = ""
    limit: str = ""
    attempts: str = ""
    exceeded_at: str = ""
class SecuritySuspiciousActivityDetectedEvent(DomainEvent):
    event_type: str = "security.suspicious_activity.detected"
    entity_type: str = "security"
    activity_id: str = ""
    user_id: str = ""
    activity_type: str = ""
    risk_score: float = 0.0
    detected_at: str = ""
class ServiceHealthDegradedEvent(DomainEvent):
    event_type: str = "service.health.degraded"
    entity_type: str = "service"
    service_name: str = ""
    health_score: float = 0.0
    failing_checks: str = ""
class ServiceHealthRecoveredEvent(DomainEvent):
    event_type: str = "service.health.recovered"
    entity_type: str = "service"
    service_name: str = ""
    health_score: float = 0.0
    recovered_at: str = ""
class SystemBackupCompletedEvent(DomainEvent):
    event_type: str = "system.backup.completed"
    entity_type: str = "system"
    backup_id: str = ""
    size_bytes: str = ""
    duration_seconds: str = ""
    completed_at: str = ""
class SystemBackupFailedEvent(DomainEvent):
    event_type: str = "system.backup.failed"
    entity_type: str = "system"
    backup_id: str = ""
    failure_reason: str = ""
class SystemBackupStartedEvent(DomainEvent):
    event_type: str = "system.backup.started"
    entity_type: str = "system"
    backup_id: str = ""
    backup_type: str = ""
    started_at: str = ""
class SystemDeploymentCompletedEvent(DomainEvent):
    event_type: str = "system.deployment.completed"
    entity_type: str = "system"
    deployment_id: str = ""
    version: str = ""
    completed_at: str = ""
class SystemDeploymentRolledBackEvent(DomainEvent):
    event_type: str = "system.deployment.rolled_back"
    entity_type: str = "system"
    deployment_id: str = ""
    rollback_reason: str = ""
    rolled_back_at: str = ""
class SystemDeploymentStartedEvent(DomainEvent):
    event_type: str = "system.deployment.started"
    entity_type: str = "system"
    deployment_id: str = ""
    version: str = ""
    environment: str = ""
    started_at: str = ""
class SystemHealthCheckedEvent(DomainEvent):
    event_type: str = "system.health.checked"
    entity_type: str = "system"
    check_id: str = ""
    system_health: str = ""
    unhealthy_components: str = ""
    checked_at: str = ""
class SystemMaintenanceCompletedEvent(DomainEvent):
    event_type: str = "system.maintenance.completed"
    entity_type: str = "system"
    maintenance_id: str = ""
    completed_at: str = ""
    changes_applied: str = ""
class SystemMaintenanceScheduledEvent(DomainEvent):
    event_type: str = "system.maintenance.scheduled"
    entity_type: str = "system"
    maintenance_id: str = ""
    maintenance_type: str = ""
    scheduled_start: str = ""
    estimated_duration: str = ""
class SystemMaintenanceStartedEvent(DomainEvent):
    event_type: str = "system.maintenance.started"
    entity_type: str = "system"
    maintenance_id: str = ""
    started_at: str = ""
class TenantComplianceCheckCompletedEvent(DomainEvent):
    event_type: str = "tenant.compliance_check.completed"
    entity_type: str = "tenant"
    tenant_id: str = ""
    check_type: str = ""
    is_compliant: bool = False
    findings: str = ""
class TenantFeatureDisabledEvent(DomainEvent):
    event_type: str = "tenant.feature_disabled"
    entity_type: str = "tenant"
    tenant_id: str = ""
    feature_name: str = ""
class TenantFeatureEnabledEvent(DomainEvent):
    event_type: str = "tenant.feature_enabled"
    entity_type: str = "tenant"
    tenant_id: str = ""
    feature_name: str = ""
class TenantIsolationViolatedEvent(DomainEvent):
    event_type: str = "tenant.isolation.violated"
    entity_type: str = "tenant"
    tenant_id: str = ""
    violation_type: str = ""
    source_tenant_id: str = ""
class TenantMembershipAddedEvent(DomainEvent):
    event_type: str = "tenant.membership.added"
    entity_type: str = "tenant"
    tenant_id: str = ""
    user_id: str = ""
    roles: str = ""
class TenantMembershipRemovedEvent(DomainEvent):
    event_type: str = "tenant.membership.removed"
    entity_type: str = "tenant"
    tenant_id: str = ""
    user_id: str = ""
    removal_reason: str = ""
class TenantMembershipRoleChangedEvent(DomainEvent):
    event_type: str = "tenant.membership.role_changed"
    entity_type: str = "tenant"
    tenant_id: str = ""
    user_id: str = ""
    previous_roles: str = ""
    new_roles: str = ""
class TenantUpdatedEvent(DomainEvent):
    event_type: str = "tenant.updated"
    entity_type: str = "tenant"
    tenant_id: str = ""
    updated_fields: str = ""
class UserPreferencesUpdatedEvent(DomainEvent):
    event_type: str = "user.preferences.updated"
    entity_type: str = "user"
    user_id: str = ""
    preference_type: str = ""
    preference_value: str = ""
class UserProfileUpdatedEvent(DomainEvent):
    event_type: str = "user.profile.updated"
    entity_type: str = "user"
    user_id: str = ""
    tenant_id: str = ""
    updated_fields: str = ""


class ApiKeyCreatedEvent(DomainEvent):
    event_type: str = "api.key.created"
    entity_type: str = "api"

    key_id: str = ""
    tenant_id: str = ""
    created_by: str = ""
    scopes: str = ""


class ApiKeyRevokedEvent(DomainEvent):
    event_type: str = "api.key.revoked"
    entity_type: str = "api"

    key_id: str = ""
    revoked_by: str = ""
    revoked_at: str = ""


class ApiQuotaExceededEvent(DomainEvent):
    event_type: str = "api.quota.exceeded"
    entity_type: str = "api"

    tenant_id: str = ""
    quota_type: str = ""
    limit: int = 0
    usage: int = 0


class ComplianceAttestationRequiredEvent(DomainEvent):
    event_type: str = "compliance.attestation.required"
    entity_type: str = "compliance"

    user_id: str = ""
    attestation_type: str = ""
    required_by: str = ""


class ComplianceAttestationCompletedEvent(DomainEvent):
    event_type: str = "compliance.attestation.completed"
    entity_type: str = "compliance"

    user_id: str = ""
    attestation_type: str = ""
    completed_at: str = ""


class ComplianceHipaaBreachDetectedEvent(DomainEvent):
    event_type: str = "compliance.hipaa.breach.detected"
    entity_type: str = "compliance"

    breach_id: str = ""
    breach_type: str = ""
    affected_records: str = ""
    detected_at: str = ""


class ComplianceHipaaBreachReportedEvent(DomainEvent):
    event_type: str = "compliance.hipaa.breach.reported"
    entity_type: str = "compliance"

    breach_id: str = ""
    reported_to: str = ""
    reported_by: str = ""
    reported_at: str = ""


class CompliancePolicyAcknowledgedEvent(DomainEvent):
    event_type: str = "compliance.policy.acknowledged"
    entity_type: str = "compliance"

    user_id: str = ""
    policy_id: str = ""
    policy_version: str = ""
    acknowledged_at: str = ""


class ComplianceViolationDetectedEvent(DomainEvent):
    event_type: str = "compliance.violation.detected"
    entity_type: str = "compliance"

    violation_id: str = ""
    violation_type: str = ""
    severity: int = 0
    detected_at: str = ""


class ComplianceViolationResolvedEvent(DomainEvent):
    event_type: str = "compliance.violation.resolved"
    entity_type: str = "compliance"

    violation_id: str = ""
    resolution: str = ""
    resolved_by: str = ""
    resolved_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("api.key.created", ApiKeyCreatedEvent)
_catalog.register("api.key.revoked", ApiKeyRevokedEvent)
_catalog.register("api.quota.exceeded", ApiQuotaExceededEvent)
_catalog.register("compliance.attestation.required", ComplianceAttestationRequiredEvent)
_catalog.register("compliance.attestation.completed", ComplianceAttestationCompletedEvent)
_catalog.register("compliance.hipaa.breach.detected", ComplianceHipaaBreachDetectedEvent)
_catalog.register("compliance.hipaa.breach.reported", ComplianceHipaaBreachReportedEvent)
_catalog.register("compliance.policy.acknowledged", CompliancePolicyAcknowledgedEvent)
_catalog.register("compliance.violation.detected", ComplianceViolationDetectedEvent)
_catalog.register("compliance.violation.resolved", ComplianceViolationResolvedEvent)
_catalog.register("config.updated", ConfigUpdatedEvent)
_catalog.register("consent.recorded", ConsentRecordedEvent)
_catalog.register("consent.withdrawn", ConsentWithdrawnEvent)
_catalog.register("crm.contact.synced", CrmContactSyncedEvent)
_catalog.register("data.deletion.completed", DataDeletionCompletedEvent)
_catalog.register("data.deletion.requested", DataDeletionRequestedEvent)
_catalog.register("data.export.completed", DataExportCompletedEvent)
_catalog.register("data.export.requested", DataExportRequestedEvent)
_catalog.register("device.registered", DeviceRegisteredEvent)
_catalog.register("device.trust_revoked", DeviceTrustRevokedEvent)
_catalog.register("device.unregistered", DeviceUnregisteredEvent)
_catalog.register("error.rate.elevated", ErrorRateElevatedEvent)
_catalog.register("module.status.changed", ModuleStatusChangedEvent)
_catalog.register("notification.batch.created", NotificationBatchCreatedEvent)
_catalog.register("notification.batch.sent", NotificationBatchSentEvent)
_catalog.register("notification.created", NotificationCreatedEvent)
_catalog.register("notification.dismissed", NotificationDismissedEvent)
_catalog.register("notification.read", NotificationReadEvent)
_catalog.register("report.exported", ReportExportedEvent)
_catalog.register("report.generated", ReportGeneratedEvent)
_catalog.register("report.scheduled", ReportScheduledEvent)
_catalog.register("security.breach.contained", SecurityBreachContainedEvent)
_catalog.register("security.breach.detected", SecurityBreachDetectedEvent)
_catalog.register("security.ip_blocked", SecurityIpBlockedEvent)
_catalog.register("security.ip_unblocked", SecurityIpUnblockedEvent)
_catalog.register("security.rate_limit.exceeded", SecurityRateLimitExceededEvent)
_catalog.register("security.suspicious_activity.detected", SecuritySuspiciousActivityDetectedEvent)
_catalog.register("service.health.degraded", ServiceHealthDegradedEvent)
_catalog.register("service.health.recovered", ServiceHealthRecoveredEvent)
_catalog.register("system.backup.completed", SystemBackupCompletedEvent)
_catalog.register("system.backup.failed", SystemBackupFailedEvent)
_catalog.register("system.backup.started", SystemBackupStartedEvent)
_catalog.register("system.deployment.completed", SystemDeploymentCompletedEvent)
_catalog.register("system.deployment.rolled_back", SystemDeploymentRolledBackEvent)
_catalog.register("system.deployment.started", SystemDeploymentStartedEvent)
_catalog.register("system.health.checked", SystemHealthCheckedEvent)
_catalog.register("system.maintenance.completed", SystemMaintenanceCompletedEvent)
_catalog.register("system.maintenance.scheduled", SystemMaintenanceScheduledEvent)
_catalog.register("system.maintenance.started", SystemMaintenanceStartedEvent)
_catalog.register("tenant.compliance_check.completed", TenantComplianceCheckCompletedEvent)
_catalog.register("tenant.feature_disabled", TenantFeatureDisabledEvent)
_catalog.register("tenant.feature_enabled", TenantFeatureEnabledEvent)
_catalog.register("tenant.isolation.violated", TenantIsolationViolatedEvent)
_catalog.register("tenant.membership.added", TenantMembershipAddedEvent)
_catalog.register("tenant.membership.removed", TenantMembershipRemovedEvent)
_catalog.register("tenant.membership.role_changed", TenantMembershipRoleChangedEvent)
_catalog.register("tenant.updated", TenantUpdatedEvent)
_catalog.register("user.preferences.updated", UserPreferencesUpdatedEvent)
_catalog.register("user.profile.updated", UserProfileUpdatedEvent)
