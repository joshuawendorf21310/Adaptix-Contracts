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
    # EXPLICITLY LIST ALL EXPORTS FROM THAT FILE
)

# Billing
from .billing_contracts import (
    # EXPLICITLY LIST ALL EXPORTS
)

from .billing_auth_contracts import (
    # EXPLICIT EXPORTS
)

from .billing_portal_contracts import (
    # EXPLICIT EXPORTS
)

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
    # EXPLICIT EXPORTS
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

# Field
from .field_contracts import (
    # EXPLICIT EXPORTS
)

# Fire
from .fire_contracts import (
    FireIncidentCreatedEvent,
    FireIncidentStatusUpdatedEvent,
    FireIncidentContract,
    NerisReadinessContract,
)

# NEMSIS
from .nemsis_exports import (
    # EXPLICIT EXPORTS
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
    # EXPLICIT EXPORTS
)

# Explicit public surface
__all__ = [
    "AirMissionCreatedEvent",
    "AirMissionStatusUpdatedEvent",
    "AirMissionContract",
    "AirLandingZoneContract",
    "TransportReadinessRequest",
    "TransportReadinessResponse",
    "BillingReadinessGate",
    "TransportReadinessGateStatus",
    "ClaimArtifactAttachRequest",
    "ClaimArtifactAttachResponse",
    "BillingTransportLinkEvent",
    "ClaimReadinessResolvedEvent",
    "CadCaseCreatedEvent",
    "CadCaseStatusUpdatedEvent",
    "CadCaseContract",
    "CadUnitAssignedEvent",
    "NotificationRequest",
    "NotificationDeliveredEvent",
    "NotificationFailedEvent",
    "CrewPageSentEvent",
    "CrewPageAcknowledgedEvent",
    "CrewMemberContract",
    "CrewRosterSyncContract",
    "EpcrChartCreatedEvent",
    "EpcrChartFinalizedEvent",
    "EpcrChartContract",
    "EpcrNemsissComplianceContract",
    "FireIncidentCreatedEvent",
    "FireIncidentStatusUpdatedEvent",
    "FireIncidentContract",
    "NerisReadinessContract",
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
]
