"""Adaptix cross-domain contract schemas.

All Pydantic models for events and read-only contracts used across domain boundaries.
"""

# Air
from .air_contracts import (
    AirMissionCreatedEvent,
    AirMissionStatusUpdatedEvent,
    AirMissionContract,
    AirLandingZoneContract,
)

# Air Pilot
from .air_pilot_contracts import (
    PilotGoNoGoEvent,
    PilotReadinessStatus,
)

# Audit
from .audit_contracts import (
    AuditActorType,
    AuditActionType,
    AuditSeverity,
    ComplianceReviewStatus,
    AuditContext,
    AuditRecord,
    PhiAccessRecord,
    SecurityEventRecord,
    ComplianceReviewItem,
    AuditRecordCreatedEvent,
    PhiAccessLoggedEvent,
    SecurityEventDetectedEvent,
    ComplianceReviewOpenedEvent,
)

# Billing
from .billing_contracts import (
    ClaimStatus,
    DenialStatus,
    PaymentStatus,
    ClearinghouseStatus,
    ClearinghouseProvider,
    PayerType,
    ClaimLineItem,
    AdjustmentContract,
    PayerContract,
    ClaimContract,
    DenialContract,
    PaymentContract,
    RemittanceContract,
    ClearinghouseSubmission,
    ClaimCreatedEvent,
    ClaimSubmittedEvent,
    ClaimStatusUpdatedEvent,
    DenialCreatedEvent,
    PaymentPostedEvent,
    RemittanceReceivedEvent,
    ClearinghouseAckReceivedEvent,
)

# Billing Auth
from .billing_auth_contracts import (
    BillingRole,
    BillingPostAuthRoute,
    MFARequirement,
    SessionAnomalyState,
    BillingSignInContext,
    BillingAccessResolution,
    BillingOrgSelectorEntry,
)

# Billing Clearinghouse
from .billing_clearinghouse_contracts import (
    SubmissionStatus,
    AckType,
    ClaimSubmissionRequest,
    ClaimSubmissionResponse,
    ClearinghouseAck,
    ClaimAckStatus,
    RemittanceIngestRequest,
    RemittanceClaimPayment,
    RemittanceIngestResponse,
    ClaimSubmittedToClearinghouseEvent,
    RemittanceIngestedEvent,
)

# Billing Eligibility
from .billing_eligibility_contracts import (
    EligibilityStatus,
    CoverageLevel,
    AuthorizationStatus,
    EligibilityRequest,
    EligibilityBenefitSummary,
    EligibilityResponse,
    EligibilityCheckedEvent,
    AuthorizationStatusUpdatedEvent,
)

# Billing Portal
from .billing_portal_contracts import (
    SurfaceAvailability,
    UrgencyLevel,
    BillingPriorityQueueSummary,
    BillingBlockedClaimsSummary,
    BillingDenialQueueSummary,
    BillingAgedARSummary,
    BillingUnderpaymentSummary,
    BillingPatientFinancialSummary,
    BillingIntegrationHealthSummary,
    BillingOperatorSummary,
    BillingPortalHomeSummary,
    ClaimDefectSeverity,
    ClaimDefect,
    ClaimReadinessSummary,
    ClaimIntakeRecord,
    SubmissionAttempt,
    SubmissionTimelineEvent,
    DenialRecord,
    DenialCluster,
    DenialRootCauseSummary,
    DenialRecoveryForecast,
    FounderTenantFinancialSummary,
    FounderBillingOverview,
)

# Billing Transport
from .billing_transport_contracts import (
    TransportReadinessRequest,
    TransportReadinessResponse,
    BillingReadinessGate,
    TransportReadinessGateStatus,
    ClaimArtifactAttachRequest,
    ClaimArtifactAttachResponse,
    BillingTransportLinkEvent,
    ClaimReadinessResolvedEvent,
)

# CAD
from .cad_contracts import (
    CadCaseCreatedEvent,
    CadCaseStatusUpdatedEvent,
    CadCaseContract,
    CadUnitAssignedEvent,
)

# CAD Transport
from .cad_transport_contracts import (
    CadTransportLaneStatus,
    ScheduledTransportLaneItem,
    DispatchReadyItem,
    CadTransportException,
    CadTransportActivateRequest,
    CadTransportActivateResponse,
    CadTransportSyncPayload,
    CadTransportSyncResponse,
    TransportActivatedEvent,
    TransportStatusSyncedEvent,
)

# Communications
from .communications_contracts import (
    NotificationRequest,
    NotificationDeliveredEvent,
    NotificationFailedEvent,
)

# Core
from .core_contracts import (
    DomainEvent,
    UserAuthContext,
)

# CrewLink
from .crewlink_contracts import (
    CrewPageSentEvent,
    CrewPageAcknowledgedEvent,
    CrewMemberContract,
    CrewRosterSyncContract,
)

# ePCR
from .epcr_contracts import (
    EpcrChartCreatedEvent,
    EpcrChartFinalizedEvent,
    EpcrChartContract,
    EpcrNemsissComplianceContract,
)

# Feature Flags
from .feature_flag_contracts import (
    FeatureFlagStatus,
    TargetType,
    FeatureFlagRule,
    FeatureFlagContract,
    FeatureFlagResolutionRequest,
    FeatureFlagResolutionResponse,
    FeatureFlagUpdatedEvent,
)

# Field
from .field_contracts import (
    UnitStatusEvent,
    UnitTelemetryEvent,
)

# Fire
from .fire_contracts import (
    FireIncidentCreatedEvent,
    FireIncidentStatusUpdatedEvent,
    FireIncidentContract,
    NerisReadinessContract,
)

# Metrics
from .metrics_contracts import (
    MetricSeverity,
    ServiceHealthStatus,
    QueueMetric,
    LatencyMetric,
    ErrorRateMetric,
    ThroughputMetric,
    ServiceHealthSummary,
    ServiceHealthReportedEvent,
)

# NEMSIS
from .nemsis_exports import (
    ExportLifecycleStatus,
    ExportFailureType,
    ExportTriggerSource,
    ExportReadinessSnapshot,
    ExportArtifactMetadata,
    ExportAttemptSummary,
    ExportAttemptDetail,
    GenerateExportRequest,
    GenerateExportResponse,
    ExportHistoryResponse,
    ExportDetailResponse,
    RetryExportRequest,
    RetryExportResponse,
)

# OCR
from .ocr_contracts import (
    OcrSourceType,
    OcrJobStatus,
    OcrFieldConfidence,
    OcrJobCreate,
    OcrJobStatusResponse,
    OcrJobDetailResponse,
    OcrFieldCandidateResponse,
    OcrFieldApproval,
    OcrApprovalRequest,
    OcrApprovalResponse,
    OcrExtractionCompletedEvent,
    OcrFieldsApprovedEvent,
)

# Patient Portal
from .patient_portal_contracts import (
    PatientVerificationMethod,
    PaymentMethod,
    DisputeReason,
    PatientVerifyRequest,
    PatientVerifyResponse,
    PatientAccountSummary,
    StatementSummaryResponse,
    StatementDetailResponse,
    StatementLineItem,
    PaymentOptionResponse,
    PaymentSubmitRequest,
    PaymentSubmitResponse,
    PaymentPlanRequest,
    PaymentPlanResponse,
    DisputeSubmitRequest,
    DisputeSubmitResponse,
    PatientDocumentResponse,
    CommunicationEventResponse,
    AiExplanationRequest,
    AiExplanationResponse,
    SupportEscalationRequest,
    SupportEscalationResponse,
)

# Search
from .search_contracts import (
    SearchDomain,
    SearchResultType,
    SearchSortOrder,
    SearchQueryRequest,
    SearchResultItem,
    SearchResponse,
    IndexDocumentRequest,
    IndexDocumentResponse,
    DeleteIndexDocumentRequest,
    DeleteIndexDocumentResponse,
    SearchExecutedEvent,
    DocumentIndexedEvent,
    DocumentDeletedEvent,
)

# Transport
from .transport_contracts import (
    TransportRequestTypeContract,
    TransportRequestStatusContract,
    RecurrencePatternContract,
    TransportRequestCreate,
    TransportRequestResponse,
    TripScheduleRequest,
    TripResponse,
    RecurringSeriesCreate,
    RecurringSeriesResponse,
    CalendarEventResponse,
    SlotSuggestionRequest,
    SlotSuggestionResponse,
    DocumentPackageResponse,
    DocumentItemResponse,
    SignatureStatusResponse,
    SignerStatusResponse,
    ReadinessStateResponse,
    ReadinessGate,
    FacilityResponse,
    CadPushRequest,
    CadPushResponse,
    TransportRequestCreatedEvent,
    TripScheduledEvent,
    SignatureCompletedEvent,
    CadPushRequestedEvent,
)

# Voice
from .voice_contracts import (
    VoiceRoomCreatedEvent,
    VoiceRoomClosedEvent,
)

# Workflow
from .workflow_contracts import (
    WorkflowStatus,
    WorkflowStepStatus,
    WorkflowStep,
    WorkflowContext,
    WorkflowExecution,
    WorkflowStartRequest,
    WorkflowStartResponse,
    WorkflowStepCompletedEvent,
    WorkflowFailedEvent,
    WorkflowCompensationTriggeredEvent,
)

# Explicit public surface
__all__ = [
    # Air
    "AirMissionCreatedEvent",
    "AirMissionStatusUpdatedEvent",
    "AirMissionContract",
    "AirLandingZoneContract",
    # Air Pilot
    "PilotGoNoGoEvent",
    "PilotReadinessStatus",
    # Audit
    "AuditActorType",
    "AuditActionType",
    "AuditSeverity",
    "ComplianceReviewStatus",
    "AuditContext",
    "AuditRecord",
    "PhiAccessRecord",
    "SecurityEventRecord",
    "ComplianceReviewItem",
    "AuditRecordCreatedEvent",
    "PhiAccessLoggedEvent",
    "SecurityEventDetectedEvent",
    "ComplianceReviewOpenedEvent",
    # Billing
    "ClaimStatus",
    "DenialStatus",
    "PaymentStatus",
    "ClearinghouseStatus",
    "ClearinghouseProvider",
    "PayerType",
    "ClaimLineItem",
    "AdjustmentContract",
    "PayerContract",
    "ClaimContract",
    "DenialContract",
    "PaymentContract",
    "RemittanceContract",
    "ClearinghouseSubmission",
    "ClaimCreatedEvent",
    "ClaimSubmittedEvent",
    "ClaimStatusUpdatedEvent",
    "DenialCreatedEvent",
    "PaymentPostedEvent",
    "RemittanceReceivedEvent",
    "ClearinghouseAckReceivedEvent",
    # Billing Auth
    "BillingRole",
    "BillingPostAuthRoute",
    "MFARequirement",
    "SessionAnomalyState",
    "BillingSignInContext",
    "BillingAccessResolution",
    "BillingOrgSelectorEntry",
    # Billing Clearinghouse
    "SubmissionStatus",
    "AckType",
    "ClaimSubmissionRequest",
    "ClaimSubmissionResponse",
    "ClearinghouseAck",
    "ClaimAckStatus",
    "RemittanceIngestRequest",
    "RemittanceClaimPayment",
    "RemittanceIngestResponse",
    "ClaimSubmittedToClearinghouseEvent",
    "RemittanceIngestedEvent",
    # Billing Eligibility
    "EligibilityStatus",
    "CoverageLevel",
    "AuthorizationStatus",
    "EligibilityRequest",
    "EligibilityBenefitSummary",
    "EligibilityResponse",
    "EligibilityCheckedEvent",
    "AuthorizationStatusUpdatedEvent",
    # Billing Portal
    "SurfaceAvailability",
    "UrgencyLevel",
    "BillingPriorityQueueSummary",
    "BillingBlockedClaimsSummary",
    "BillingDenialQueueSummary",
    "BillingAgedARSummary",
    "BillingUnderpaymentSummary",
    "BillingPatientFinancialSummary",
    "BillingIntegrationHealthSummary",
    "BillingOperatorSummary",
    "BillingPortalHomeSummary",
    "ClaimDefectSeverity",
    "ClaimDefect",
    "ClaimReadinessSummary",
    "ClaimIntakeRecord",
    "SubmissionAttempt",
    "SubmissionTimelineEvent",
    "DenialRecord",
    "DenialCluster",
    "DenialRootCauseSummary",
    "DenialRecoveryForecast",
    "FounderTenantFinancialSummary",
    "FounderBillingOverview",
    # Billing Transport
    "TransportReadinessRequest",
    "TransportReadinessResponse",
    "BillingReadinessGate",
    "TransportReadinessGateStatus",
    "ClaimArtifactAttachRequest",
    "ClaimArtifactAttachResponse",
    "BillingTransportLinkEvent",
    "ClaimReadinessResolvedEvent",
    # CAD
    "CadCaseCreatedEvent",
    "CadCaseStatusUpdatedEvent",
    "CadCaseContract",
    "CadUnitAssignedEvent",
    # CAD Transport
    "CadTransportLaneStatus",
    "ScheduledTransportLaneItem",
    "DispatchReadyItem",
    "CadTransportException",
    "CadTransportActivateRequest",
    "CadTransportActivateResponse",
    "CadTransportSyncPayload",
    "CadTransportSyncResponse",
    "TransportActivatedEvent",
    "TransportStatusSyncedEvent",
    # Communications
    "NotificationRequest",
    "NotificationDeliveredEvent",
    "NotificationFailedEvent",
    # Core
    "DomainEvent",
    "UserAuthContext",
    # CrewLink
    "CrewPageSentEvent",
    "CrewPageAcknowledgedEvent",
    "CrewMemberContract",
    "CrewRosterSyncContract",
    # ePCR
    "EpcrChartCreatedEvent",
    "EpcrChartFinalizedEvent",
    "EpcrChartContract",
    "EpcrNemsissComplianceContract",
    # Feature Flags
    "FeatureFlagStatus",
    "TargetType",
    "FeatureFlagRule",
    "FeatureFlagContract",
    "FeatureFlagResolutionRequest",
    "FeatureFlagResolutionResponse",
    "FeatureFlagUpdatedEvent",
    # Field
    "UnitStatusEvent",
    "UnitTelemetryEvent",
    # Fire
    "FireIncidentCreatedEvent",
    "FireIncidentStatusUpdatedEvent",
    "FireIncidentContract",
    "NerisReadinessContract",
    # Metrics
    "MetricSeverity",
    "ServiceHealthStatus",
    "QueueMetric",
    "LatencyMetric",
    "ErrorRateMetric",
    "ThroughputMetric",
    "ServiceHealthSummary",
    "ServiceHealthReportedEvent",
    # NEMSIS
    "ExportLifecycleStatus",
    "ExportFailureType",
    "ExportTriggerSource",
    "ExportReadinessSnapshot",
    "ExportArtifactMetadata",
    "ExportAttemptSummary",
    "ExportAttemptDetail",
    "GenerateExportRequest",
    "GenerateExportResponse",
    "ExportHistoryResponse",
    "ExportDetailResponse",
    "RetryExportRequest",
    "RetryExportResponse",
    # OCR
    "OcrSourceType",
    "OcrJobStatus",
    "OcrFieldConfidence",
    "OcrJobCreate",
    "OcrJobStatusResponse",
    "OcrJobDetailResponse",
    "OcrFieldCandidateResponse",
    "OcrFieldApproval",
    "OcrApprovalRequest",
    "OcrApprovalResponse",
    "OcrExtractionCompletedEvent",
    "OcrFieldsApprovedEvent",
    # Patient Portal
    "PatientVerificationMethod",
    "PaymentMethod",
    "DisputeReason",
    "PatientVerifyRequest",
    "PatientVerifyResponse",
    "PatientAccountSummary",
    "StatementSummaryResponse",
    "StatementDetailResponse",
    "StatementLineItem",
    "PaymentOptionResponse",
    "PaymentSubmitRequest",
    "PaymentSubmitResponse",
    "PaymentPlanRequest",
    "PaymentPlanResponse",
    "DisputeSubmitRequest",
    "DisputeSubmitResponse",
    "PatientDocumentResponse",
    "CommunicationEventResponse",
    "AiExplanationRequest",
    "AiExplanationResponse",
    "SupportEscalationRequest",
    "SupportEscalationResponse",
    # Search
    "SearchDomain",
    "SearchResultType",
    "SearchSortOrder",
    "SearchQueryRequest",
    "SearchResultItem",
    "SearchResponse",
    "IndexDocumentRequest",
    "IndexDocumentResponse",
    "DeleteIndexDocumentRequest",
    "DeleteIndexDocumentResponse",
    "SearchExecutedEvent",
    "DocumentIndexedEvent",
    "DocumentDeletedEvent",
    # Transport
    "TransportRequestTypeContract",
    "TransportRequestStatusContract",
    "RecurrencePatternContract",
    "TransportRequestCreate",
    "TransportRequestResponse",
    "TripScheduleRequest",
    "TripResponse",
    "RecurringSeriesCreate",
    "RecurringSeriesResponse",
    "CalendarEventResponse",
    "SlotSuggestionRequest",
    "SlotSuggestionResponse",
    "DocumentPackageResponse",
    "DocumentItemResponse",
    "SignatureStatusResponse",
    "SignerStatusResponse",
    "ReadinessStateResponse",
    "ReadinessGate",
    "FacilityResponse",
    "CadPushRequest",
    "CadPushResponse",
    "TransportRequestCreatedEvent",
    "TripScheduledEvent",
    "SignatureCompletedEvent",
    "CadPushRequestedEvent",
    # Voice
    "VoiceRoomCreatedEvent",
    "VoiceRoomClosedEvent",
    # Workflow
    "WorkflowStatus",
    "WorkflowStepStatus",
    "WorkflowStep",
    "WorkflowContext",
    "WorkflowExecution",
    "WorkflowStartRequest",
    "WorkflowStartResponse",
    "WorkflowStepCompletedEvent",
    "WorkflowFailedEvent",
    "WorkflowCompensationTriggeredEvent",
]
