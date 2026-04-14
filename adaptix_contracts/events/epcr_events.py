"""ePCR domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class EpcrCreatedEvent(DomainEvent):
    event_type: str = "epcr.created"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""
    patient_id: str = ""


class EpcrSignedEvent(DomainEvent):
    event_type: str = "epcr.signed"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""
    patient_id: str = ""
    signed_by: str = ""
    signed_at: str = ""


class EpcrLockedEvent(DomainEvent):
    event_type: str = "epcr.locked"
    entity_type: str = "epcr"

    epcr_id: str = ""
    incident_id: str = ""


class EpcrNemsisExportedEvent(DomainEvent):
    event_type: str = "epcr.nemsis.exported"
    entity_type: str = "epcr"

    export_id: str = ""
    epcr_id: str = ""
    state_code: str = ""
    export_status: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("epcr.created", EpcrCreatedEvent)
_catalog.register("epcr.signed", EpcrSignedEvent)
_catalog.register("epcr.locked", EpcrLockedEvent)
_catalog.register("epcr.nemsis.exported", EpcrNemsisExportedEvent)
class EpcrAddendumAddedEvent(DomainEvent):
    event_type: str = "epcr.addendum_added"
    entity_type: str = "epcr"
    epcr_id: str = ""
    addendum_id: str = ""
    added_by: str = ""
    added_at: str = ""
class EpcrAssessmentRecordedEvent(DomainEvent):
    event_type: str = "epcr.assessment.recorded"
    entity_type: str = "epcr"
    epcr_id: str = ""
    assessment_type: str = ""
    findings: str = ""
    recorded_by: str = ""
    recorded_at: str = ""
class EpcrCompletenessScoredEvent(DomainEvent):
    event_type: str = "epcr.completeness_scored"
    entity_type: str = "epcr"
    epcr_id: str = ""
    completeness_score: float = 0.0
    missing_fields: str = ""
class EpcrCorrectedEvent(DomainEvent):
    event_type: str = "epcr.corrected"
    entity_type: str = "epcr"
    epcr_id: str = ""
    correction_type: str = ""
    corrected_by: str = ""
    corrected_at: str = ""
class EpcrImpressionRecordedEvent(DomainEvent):
    event_type: str = "epcr.impression.recorded"
    entity_type: str = "epcr"
    epcr_id: str = ""
    impression_code: str = ""
    impression_text: str = ""
    recorded_by: str = ""
class EpcrInterventionPerformedEvent(DomainEvent):
    event_type: str = "epcr.intervention_performed"
    entity_type: str = "epcr"
    epcr_id: str = ""
    intervention_code: str = ""
    performed_by: str = ""
    performed_at: str = ""
class EpcrMedicationAdministeredEvent(DomainEvent):
    event_type: str = "epcr.medication_administered"
    entity_type: str = "epcr"
    epcr_id: str = ""
    medication_code: str = ""
    dose: str = ""
    route: str = ""
    administered_by: str = ""
    administered_at: str = ""
class EpcrNarrativeUpdatedEvent(DomainEvent):
    event_type: str = "epcr.narrative_updated"
    entity_type: str = "epcr"
    epcr_id: str = ""
    narrative_section: str = ""
    updated_by: str = ""
class EpcrOutcomeRecordedEvent(DomainEvent):
    event_type: str = "epcr.outcome.recorded"
    entity_type: str = "epcr"
    epcr_id: str = ""
    outcome_type: str = ""
    destination: str = ""
    recorded_by: str = ""
class EpcrPatientAddedEvent(DomainEvent):
    event_type: str = "epcr.patient_added"
    entity_type: str = "epcr"
    epcr_id: str = ""
    patient_id: str = ""
    incident_id: str = ""
class EpcrPhiAccessedEvent(DomainEvent):
    event_type: str = "epcr.phi_accessed"
    entity_type: str = "epcr"
    epcr_id: str = ""
    accessor_id: str = ""
    access_reason: str = ""
    accessed_at: str = ""
class EpcrProtocolAppliedEvent(DomainEvent):
    event_type: str = "epcr.protocol.applied"
    entity_type: str = "epcr"
    epcr_id: str = ""
    protocol_id: str = ""
    protocol_name: str = ""
    applied_by: str = ""
    applied_at: str = ""
class EpcrProtocolDeviatedEvent(DomainEvent):
    event_type: str = "epcr.protocol.deviated"
    entity_type: str = "epcr"
    epcr_id: str = ""
    protocol_id: str = ""
    deviation_reason: str = ""
    documented_by: str = ""
class EpcrQaReviewCompletedEvent(DomainEvent):
    event_type: str = "epcr.qa_review_completed"
    entity_type: str = "epcr"
    epcr_id: str = ""
    reviewer_id: str = ""
    review_result: str = ""
    findings: str = ""
class EpcrQaReviewRequestedEvent(DomainEvent):
    event_type: str = "epcr.qa_review_requested"
    entity_type: str = "epcr"
    epcr_id: str = ""
    requested_by: str = ""
    review_reason: str = ""
class EpcrRefusalDocumentedEvent(DomainEvent):
    event_type: str = "epcr.refusal.documented"
    entity_type: str = "epcr"
    epcr_id: str = ""
    refusal_type: str = ""
    patient_signature: str = ""
    witness_signature: str = ""
    documented_at: str = ""
class EpcrSignatureAddedEvent(DomainEvent):
    event_type: str = "epcr.signature_added"
    entity_type: str = "epcr"
    epcr_id: str = ""
    signature_type: str = ""
    signed_by: str = ""
    signed_at: str = ""
class EpcrTimeRecordedEvent(DomainEvent):
    event_type: str = "epcr.time.recorded"
    entity_type: str = "epcr"
    epcr_id: str = ""
    time_type: str = ""
    timestamp: str = ""
    recorded_by: str = ""
class EpcrTransferOfCareDocumentedEvent(DomainEvent):
    event_type: str = "epcr.transfer_of_care.documented"
    entity_type: str = "epcr"
    epcr_id: str = ""
    receiving_facility: str = ""
    receiving_provider: str = ""
    transferred_at: str = ""
class EpcrUnlockedEvent(DomainEvent):
    event_type: str = "epcr.unlocked"
    entity_type: str = "epcr"
    epcr_id: str = ""
    unlocked_by: str = ""
    unlock_reason: str = ""
class EpcrVitalRecordedEvent(DomainEvent):
    event_type: str = "epcr.vital_recorded"
    entity_type: str = "epcr"
    epcr_id: str = ""
    vital_type: str = ""
    value: str = ""
    recorded_at: str = ""
class MedicationAdverseReactionReportedEvent(DomainEvent):
    event_type: str = "medication.adverse_reaction.reported"
    entity_type: str = "medication"
    epcr_id: str = ""
    medication_name: str = ""
    reaction_type: str = ""
    severity: int = 0
    reported_at: str = ""
class MedicationAllergyCheckPerformedEvent(DomainEvent):
    event_type: str = "medication.allergy_check.performed"
    entity_type: str = "medication"
    patient_id: str = ""
    medication_name: str = ""
    has_allergy: bool = False
    checked_at: str = ""
class MedicationDoseVerificationRequiredEvent(DomainEvent):
    event_type: str = "medication.dose_verification.required"
    entity_type: str = "medication"
    order_id: str = ""
    medication_name: str = ""
    calculated_dose: str = ""
    requires_override: str = ""
class MedicationEffectivenessAssessedEvent(DomainEvent):
    event_type: str = "medication.effectiveness.assessed"
    entity_type: str = "medication"
    epcr_id: str = ""
    medication_name: str = ""
    effectiveness: str = ""
    assessed_by: str = ""
    assessed_at: str = ""
class MedicationInteractionCheckPerformedEvent(DomainEvent):
    event_type: str = "medication.interaction_check.performed"
    entity_type: str = "medication"
    patient_id: str = ""
    medication_name: str = ""
    has_interaction: bool = False
    interactions: str = ""
    checked_at: str = ""
class MedicationOrderCreatedEvent(DomainEvent):
    event_type: str = "medication.order.created"
    entity_type: str = "medication"
    order_id: str = ""
    patient_id: str = ""
    medication_name: str = ""
    dose: str = ""
    route: str = ""
    ordered_by: str = ""
class MedicationOrderVerifiedEvent(DomainEvent):
    event_type: str = "medication.order.verified"
    entity_type: str = "medication"
    order_id: str = ""
    verified_by: str = ""
    verified_at: str = ""
class MedicationProtocolOverrideDocumentedEvent(DomainEvent):
    event_type: str = "medication.protocol_override.documented"
    entity_type: str = "medication"
    epcr_id: str = ""
    medication_name: str = ""
    override_reason: str = ""
    authorized_by: str = ""
class MedicationRefusalDocumentedEvent(DomainEvent):
    event_type: str = "medication.refusal.documented"
    entity_type: str = "medication"
    epcr_id: str = ""
    medication_name: str = ""
    refusal_reason: str = ""
    documented_by: str = ""
    documented_at: str = ""
class PatientAdvanceDirectiveRecordedEvent(DomainEvent):
    event_type: str = "patient.advance_directive.recorded"
    entity_type: str = "patient"
    patient_id: str = ""
    directive_type: str = ""
    recorded_by: str = ""
    recorded_at: str = ""
class PatientAllergyAddedEvent(DomainEvent):
    event_type: str = "patient.allergy.added"
    entity_type: str = "patient"
    patient_id: str = ""
    allergy_type: str = ""
    severity: int = 0
    added_by: str = ""
class PatientAllergyRemovedEvent(DomainEvent):
    event_type: str = "patient.allergy.removed"
    entity_type: str = "patient"
    patient_id: str = ""
    allergy_type: str = ""
    removed_by: str = ""
    removed_at: str = ""
class PatientComplaintFiledEvent(DomainEvent):
    event_type: str = "patient.complaint.filed"
    entity_type: str = "patient"
    complaint_id: str = ""
    patient_id: str = ""
    complaint_type: str = ""
    description: str = ""
    filed_at: str = ""
class PatientComplaintResolvedEvent(DomainEvent):
    event_type: str = "patient.complaint.resolved"
    entity_type: str = "patient"
    complaint_id: str = ""
    resolution: str = ""
    resolved_by: str = ""
    resolved_at: str = ""
class PatientConsentObtainedEvent(DomainEvent):
    event_type: str = "patient.consent.obtained"
    entity_type: str = "patient"
    patient_id: str = ""
    consent_type: str = ""
    obtained_by: str = ""
    obtained_at: str = ""
class PatientConsentRecordedEvent(DomainEvent):
    event_type: str = "patient.consent.recorded"
    entity_type: str = "patient"
    patient_id: str = ""
    consent_type: str = ""
    granted: str = ""
    recorded_by: str = ""
    recorded_at: str = ""
class PatientConsentRevokedEvent(DomainEvent):
    event_type: str = "patient.consent.revoked"
    entity_type: str = "patient"
    patient_id: str = ""
    consent_type: str = ""
    revoked_by: str = ""
    revoked_at: str = ""
class PatientCreatedEvent(DomainEvent):
    event_type: str = "patient.created"
    entity_type: str = "patient"
    patient_id: str = ""
    demographics: str = ""
    created_at: str = ""
class PatientDemographicsUpdatedEvent(DomainEvent):
    event_type: str = "patient.demographics.updated"
    entity_type: str = "patient"
    patient_id: str = ""
    updated_fields: str = ""
    updated_by: str = ""
    updated_at: str = ""
class PatientEncounterClosedEvent(DomainEvent):
    event_type: str = "patient.encounter.closed"
    entity_type: str = "patient"
    encounter_id: str = ""
    closed_by: str = ""
    closed_at: str = ""
    outcome: str = ""
class PatientEncounterCreatedEvent(DomainEvent):
    event_type: str = "patient.encounter.created"
    entity_type: str = "patient"
    encounter_id: str = ""
    patient_id: str = ""
    encounter_type: str = ""
    created_at: str = ""
class PatientMergeCompletedEvent(DomainEvent):
    event_type: str = "patient.merge.completed"
    entity_type: str = "patient"
    master_patient_id: str = ""
    merged_patient_ids: str = ""
    merged_by: str = ""
    merged_at: str = ""
class PatientMergedEvent(DomainEvent):
    event_type: str = "patient.merged"
    entity_type: str = "patient"
    source_patient_id: str = ""
    target_patient_id: str = ""
    merged_by: str = ""
    merged_at: str = ""
class PatientSurveyCompletedEvent(DomainEvent):
    event_type: str = "patient.survey.completed"
    entity_type: str = "patient"
    survey_id: str = ""
    patient_id: str = ""
    responses: str = ""
    completed_at: str = ""
class PatientSurveySentEvent(DomainEvent):
    event_type: str = "patient.survey.sent"
    entity_type: str = "patient"
    survey_id: str = ""
    patient_id: str = ""
    survey_type: str = ""
    sent_at: str = ""
class QaCaseAssignedEvent(DomainEvent):
    event_type: str = "qa.case.assigned"
    entity_type: str = "qa"
    case_id: str = ""
    assigned_to: str = ""
    assigned_by: str = ""
    assigned_at: str = ""
class QaCaseFlaggedEvent(DomainEvent):
    event_type: str = "qa.case.flagged"
    entity_type: str = "qa"
    case_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    flag_reason: str = ""
    flagged_by: str = ""
class QaCaseReviewedEvent(DomainEvent):
    event_type: str = "qa.case.reviewed"
    entity_type: str = "qa"
    case_id: str = ""
    reviewer_id: str = ""
    outcome: str = ""
    findings: str = ""
    reviewed_at: str = ""
class QaCorrectiveActionCompletedEvent(DomainEvent):
    event_type: str = "qa.corrective_action.completed"
    entity_type: str = "qa"
    action_id: str = ""
    completion_notes: str = ""
    completed_at: str = ""
class QaCorrectiveActionInitiatedEvent(DomainEvent):
    event_type: str = "qa.corrective_action.initiated"
    entity_type: str = "qa"
    action_id: str = ""
    user_id: str = ""
    action_type: str = ""
    initiated_by: str = ""
    initiated_at: str = ""
class QaEducationRequiredEvent(DomainEvent):
    event_type: str = "qa.education.required"
    entity_type: str = "qa"
    case_id: str = ""
    user_id: str = ""
    education_topic: str = ""
    required_by: str = ""
class QualityReviewClosedEvent(DomainEvent):
    event_type: str = "quality.review.closed"
    entity_type: str = "quality"
    review_id: str = ""
    outcome: str = ""
    closed_by: str = ""
    closed_at: str = ""
class QualityReviewFindingAddedEvent(DomainEvent):
    event_type: str = "quality.review.finding_added"
    entity_type: str = "quality"
    review_id: str = ""
    finding_type: str = ""
    severity: int = 0
    description: str = ""
class QualityReviewInitiatedEvent(DomainEvent):
    event_type: str = "quality.review.initiated"
    entity_type: str = "quality"
    review_id: str = ""
    entity_type: str = ""
    entity_id: str = ""
    review_type: str = ""
    initiated_by: str = ""


class ComplianceNemsisExportGeneratedEvent(DomainEvent):
    event_type: str = "compliance.nemsis.export.generated"
    entity_type: str = "compliance"
    export_id: str = ""
    dataset_version: str = ""
    record_count: int = 0
    generated_at: str = ""


class ComplianceNemsisExportSubmittedEvent(DomainEvent):
    event_type: str = "compliance.nemsis.export.submitted"
    entity_type: str = "compliance"
    export_id: str = ""
    submission_id: str = ""
    state_agency: str = ""
    submitted_at: str = ""


class ComplianceNemsisExportValidatedEvent(DomainEvent):
    event_type: str = "compliance.nemsis.export.validated"
    entity_type: str = "compliance"
    export_id: str = ""
    is_valid: bool = False
    error_count: int = 0
    validated_at: str = ""


_catalog.register("epcr.addendum_added", EpcrAddendumAddedEvent)
_catalog.register("epcr.assessment.recorded", EpcrAssessmentRecordedEvent)
_catalog.register("epcr.completeness_scored", EpcrCompletenessScoredEvent)
_catalog.register("epcr.corrected", EpcrCorrectedEvent)
_catalog.register("epcr.impression.recorded", EpcrImpressionRecordedEvent)
_catalog.register("epcr.intervention_performed", EpcrInterventionPerformedEvent)
_catalog.register("epcr.medication_administered", EpcrMedicationAdministeredEvent)
_catalog.register("epcr.narrative_updated", EpcrNarrativeUpdatedEvent)
_catalog.register("epcr.outcome.recorded", EpcrOutcomeRecordedEvent)
_catalog.register("epcr.patient_added", EpcrPatientAddedEvent)
_catalog.register("epcr.phi_accessed", EpcrPhiAccessedEvent)
_catalog.register("epcr.protocol.applied", EpcrProtocolAppliedEvent)
_catalog.register("epcr.protocol.deviated", EpcrProtocolDeviatedEvent)
_catalog.register("epcr.qa_review_completed", EpcrQaReviewCompletedEvent)
_catalog.register("epcr.qa_review_requested", EpcrQaReviewRequestedEvent)
_catalog.register("epcr.refusal.documented", EpcrRefusalDocumentedEvent)
_catalog.register("epcr.signature_added", EpcrSignatureAddedEvent)
_catalog.register("epcr.time.recorded", EpcrTimeRecordedEvent)
_catalog.register("epcr.transfer_of_care.documented", EpcrTransferOfCareDocumentedEvent)
_catalog.register("epcr.unlocked", EpcrUnlockedEvent)
_catalog.register("epcr.vital_recorded", EpcrVitalRecordedEvent)
_catalog.register("medication.adverse_reaction.reported", MedicationAdverseReactionReportedEvent)
_catalog.register("medication.allergy_check.performed", MedicationAllergyCheckPerformedEvent)
_catalog.register("medication.dose_verification.required", MedicationDoseVerificationRequiredEvent)
_catalog.register("medication.effectiveness.assessed", MedicationEffectivenessAssessedEvent)
_catalog.register("medication.interaction_check.performed", MedicationInteractionCheckPerformedEvent)
_catalog.register("medication.order.created", MedicationOrderCreatedEvent)
_catalog.register("medication.order.verified", MedicationOrderVerifiedEvent)
_catalog.register("medication.protocol_override.documented", MedicationProtocolOverrideDocumentedEvent)
_catalog.register("medication.refusal.documented", MedicationRefusalDocumentedEvent)
_catalog.register("patient.advance_directive.recorded", PatientAdvanceDirectiveRecordedEvent)
_catalog.register("patient.allergy.added", PatientAllergyAddedEvent)
_catalog.register("patient.allergy.removed", PatientAllergyRemovedEvent)
_catalog.register("patient.complaint.filed", PatientComplaintFiledEvent)
_catalog.register("patient.complaint.resolved", PatientComplaintResolvedEvent)
_catalog.register("patient.consent.obtained", PatientConsentObtainedEvent)
_catalog.register("patient.consent.recorded", PatientConsentRecordedEvent)
_catalog.register("patient.consent.revoked", PatientConsentRevokedEvent)
_catalog.register("patient.created", PatientCreatedEvent)
_catalog.register("patient.demographics.updated", PatientDemographicsUpdatedEvent)
_catalog.register("patient.encounter.closed", PatientEncounterClosedEvent)
_catalog.register("patient.encounter.created", PatientEncounterCreatedEvent)
_catalog.register("patient.merge.completed", PatientMergeCompletedEvent)
_catalog.register("patient.merged", PatientMergedEvent)
_catalog.register("patient.survey.completed", PatientSurveyCompletedEvent)
_catalog.register("patient.survey.sent", PatientSurveySentEvent)
_catalog.register("qa.case.assigned", QaCaseAssignedEvent)
_catalog.register("qa.case.flagged", QaCaseFlaggedEvent)
_catalog.register("qa.case.reviewed", QaCaseReviewedEvent)
_catalog.register("qa.corrective_action.completed", QaCorrectiveActionCompletedEvent)
_catalog.register("qa.corrective_action.initiated", QaCorrectiveActionInitiatedEvent)
_catalog.register("qa.education.required", QaEducationRequiredEvent)
_catalog.register("quality.review.closed", QualityReviewClosedEvent)
_catalog.register("quality.review.finding_added", QualityReviewFindingAddedEvent)
_catalog.register("quality.review.initiated", QualityReviewInitiatedEvent)
_catalog.register("compliance.nemsis.export.generated", ComplianceNemsisExportGeneratedEvent)
_catalog.register("compliance.nemsis.export.submitted", ComplianceNemsisExportSubmittedEvent)
_catalog.register("compliance.nemsis.export.validated", ComplianceNemsisExportValidatedEvent)
