"""Workforce, scheduling, and training domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class SchedulingShiftCreatedEvent(DomainEvent):
    event_type: str = "scheduling.shift.created"
    entity_type: str = "shift"

    shift_id: str = ""
    unit_id: str = ""
    start_time: str = ""
    end_time: str = ""


class SchedulingShiftFilledEvent(DomainEvent):
    event_type: str = "scheduling.shift.filled"
    entity_type: str = "shift"

    shift_id: str = ""
    user_id: str = ""


class SchedulingShiftMissedEvent(DomainEvent):
    event_type: str = "scheduling.shift.missed"
    entity_type: str = "shift"

    shift_id: str = ""


class PersonnelCreatedEvent(DomainEvent):
    event_type: str = "personnel.created"
    entity_type: str = "personnel"

    user_id: str = ""
    first_name: str = ""
    last_name: str = ""
    role: str = ""


class PersonnelDeactivatedEvent(DomainEvent):
    event_type: str = "personnel.deactivated"
    entity_type: str = "personnel"

    user_id: str = ""
    reason: str = ""


class TrainingCompletedEvent(DomainEvent):
    event_type: str = "training.completed"
    entity_type: str = "training"

    training_id: str = ""
    user_id: str = ""
    course_name: str = ""
    completed_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("scheduling.shift.created", SchedulingShiftCreatedEvent)
_catalog.register("scheduling.shift.filled", SchedulingShiftFilledEvent)
_catalog.register("scheduling.shift.missed", SchedulingShiftMissedEvent)
_catalog.register("personnel.created", PersonnelCreatedEvent)
_catalog.register("personnel.deactivated", PersonnelDeactivatedEvent)
_catalog.register("training.completed", TrainingCompletedEvent)
class CertificationExpiredEvent(DomainEvent):
    event_type: str = "certification.expired"
    entity_type: str = "certification"
    user_id: str = ""
    certification_type: str = ""
    expired_at: str = ""
class CertificationExpiringEvent(DomainEvent):
    event_type: str = "certification.expiring"
    entity_type: str = "certification"
    user_id: str = ""
    certification_type: str = ""
    expiration_date: str = ""
    days_until_expiration: str = ""
class CertificationRenewedEvent(DomainEvent):
    event_type: str = "certification.renewed"
    entity_type: str = "certification"
    user_id: str = ""
    certification_type: str = ""
    new_expiration_date: str = ""
    renewed_at: str = ""
class CrewCalloutInitiatedEvent(DomainEvent):
    event_type: str = "crew.callout.initiated"
    entity_type: str = "crew"
    callout_id: str = ""
    shift_id: str = ""
    reason: str = ""
    initiated_at: str = ""
class CrewCalloutResponseReceivedEvent(DomainEvent):
    event_type: str = "crew.callout.response_received"
    entity_type: str = "crew"
    callout_id: str = ""
    user_id: str = ""
    response: str = ""
    responded_at: str = ""
class CrewMinimumStaffingViolatedEvent(DomainEvent):
    event_type: str = "crew.minimum_staffing.violated"
    entity_type: str = "crew"
    unit_id: str = ""
    required_count: int = 0
    actual_count: int = 0
    violated_at: str = ""
class CrewQualificationVerifiedEvent(DomainEvent):
    event_type: str = "crew.qualification.verified"
    entity_type: str = "crew"
    user_id: str = ""
    qualification_type: str = ""
    verified_by: str = ""
    verified_at: str = ""
class CrewRosterUpdatedEvent(DomainEvent):
    event_type: str = "crew.roster.updated"
    entity_type: str = "crew"
    unit_id: str = ""
    shift_id: str = ""
    crew_members: str = ""
    updated_at: str = ""
class FatigueRiskAssessedEvent(DomainEvent):
    event_type: str = "fatigue.risk.assessed"
    entity_type: str = "fatigue"
    user_id: str = ""
    fatigue_score: float = 0.0
    hours_worked: str = ""
    rest_hours: str = ""
class PerformanceDegradationDetectedEvent(DomainEvent):
    event_type: str = "performance.degradation.detected"
    entity_type: str = "performance"
    service_name: str = ""
    metric_name: str = ""
    degradation_percent: float = 0.0
    detected_at: str = ""
class PerformanceReviewCompletedEvent(DomainEvent):
    event_type: str = "performance.review.completed"
    entity_type: str = "performance"
    review_id: str = ""
    user_id: str = ""
    overall_score: float = 0.0
    completed_at: str = ""
class PerformanceReviewScheduledEvent(DomainEvent):
    event_type: str = "performance.review.scheduled"
    entity_type: str = "performance"
    review_id: str = ""
    user_id: str = ""
    reviewer_id: str = ""
    scheduled_date: str = ""
class PerformanceThresholdExceededEvent(DomainEvent):
    event_type: str = "performance.threshold.exceeded"
    entity_type: str = "performance"
    metric_name: str = ""
    threshold: str = ""
    actual_value: str = ""
    exceeded_at: str = ""
class ShiftOvertimeApprovedEvent(DomainEvent):
    event_type: str = "shift.overtime.approved"
    entity_type: str = "shift"
    shift_id: str = ""
    user_id: str = ""
    overtime_hours: str = ""
    approved_by: str = ""
class ShiftRosteredEvent(DomainEvent):
    event_type: str = "shift.rostered"
    entity_type: str = "shift"
    shift_id: str = ""
    unit_id: str = ""
    position: str = ""
    start_time: str = ""
    end_time: str = ""
class ShiftSwappedEvent(DomainEvent):
    event_type: str = "shift.swapped"
    entity_type: str = "shift"
    original_shift_id: str = ""
    swap_shift_id: str = ""
    user_id: str = ""
    swapped_with_user_id: str = ""
class TimeoffApprovedEvent(DomainEvent):
    event_type: str = "timeoff.approved"
    entity_type: str = "timeoff"
    request_id: str = ""
    approved_by: str = ""
    approved_at: str = ""
class TimeoffDeniedEvent(DomainEvent):
    event_type: str = "timeoff.denied"
    entity_type: str = "timeoff"
    request_id: str = ""
    denied_by: str = ""
    denial_reason: str = ""
class TimeoffRequestedEvent(DomainEvent):
    event_type: str = "timeoff.requested"
    entity_type: str = "timeoff"
    request_id: str = ""
    user_id: str = ""
    start_date: str = ""
    end_date: str = ""
    timeoff_type: str = ""
class TrainingAssessmentFailedEvent(DomainEvent):
    event_type: str = "training.assessment.failed"
    entity_type: str = "training"
    session_id: str = ""
    user_id: str = ""
    score: float = 0.0
    failed_at: str = ""
class TrainingAssessmentPassedEvent(DomainEvent):
    event_type: str = "training.assessment.passed"
    entity_type: str = "training"
    session_id: str = ""
    user_id: str = ""
    score: float = 0.0
    passed_at: str = ""
class TrainingContinuingEducationRecordedEvent(DomainEvent):
    event_type: str = "training.continuing_education.recorded"
    entity_type: str = "training"
    user_id: str = ""
    ce_hours: str = ""
    course_name: str = ""
    completion_date: str = ""
class TrainingCourseCompletedEvent(DomainEvent):
    event_type: str = "training.course.completed"
    entity_type: str = "training"
    user_id: str = ""
    course_id: str = ""
    completed_at: str = ""
    score: float = 0.0
class TrainingCourseEnrolledEvent(DomainEvent):
    event_type: str = "training.course.enrolled"
    entity_type: str = "training"
    user_id: str = ""
    course_id: str = ""
    enrolled_at: str = ""
class TrainingCourseFailedEvent(DomainEvent):
    event_type: str = "training.course.failed"
    entity_type: str = "training"
    user_id: str = ""
    course_id: str = ""
    failed_at: str = ""
    score: float = 0.0
class TrainingCourseStartedEvent(DomainEvent):
    event_type: str = "training.course.started"
    entity_type: str = "training"
    user_id: str = ""
    course_id: str = ""
    started_at: str = ""
class TrainingModuleCompletedEvent(DomainEvent):
    event_type: str = "training.module.completed"
    entity_type: str = "training"
    user_id: str = ""
    course_id: str = ""
    module_id: str = ""
    completed_at: str = ""
class TrainingParticipantEnrolledEvent(DomainEvent):
    event_type: str = "training.participant.enrolled"
    entity_type: str = "training"
    session_id: str = ""
    user_id: str = ""
    enrolled_at: str = ""
class TrainingParticipantWithdrewEvent(DomainEvent):
    event_type: str = "training.participant.withdrew"
    entity_type: str = "training"
    session_id: str = ""
    user_id: str = ""
    withdrawal_reason: str = ""
class TrainingSessionCompletedEvent(DomainEvent):
    event_type: str = "training.session.completed"
    entity_type: str = "training"
    session_id: str = ""
    participant_count: int = 0
    completed_at: str = ""
class TrainingSessionScheduledEvent(DomainEvent):
    event_type: str = "training.session.scheduled"
    entity_type: str = "training"
    session_id: str = ""
    course_name: str = ""
    instructor_id: str = ""
    scheduled_date: str = ""
    max_participants: str = ""
class TrainingSessionStartedEvent(DomainEvent):
    event_type: str = "training.session.started"
    entity_type: str = "training"
    session_id: str = ""
    started_at: str = ""
class TrainingSkillVerifiedEvent(DomainEvent):
    event_type: str = "training.skill.verified"
    entity_type: str = "training"
    user_id: str = ""
    skill_id: str = ""
    verified_by: str = ""
    verified_at: str = ""
class VehicleAssignedEvent(DomainEvent):
    event_type: str = "vehicle.assigned"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    unit_id: str = ""
    assigned_at: str = ""
class VehicleInspectionCompletedEvent(DomainEvent):
    event_type: str = "vehicle.inspection.completed"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    inspection_type: str = ""
    completed_by: str = ""
    completed_at: str = ""
    passed: bool = False
class VehicleInspectionDueEvent(DomainEvent):
    event_type: str = "vehicle.inspection.due"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    inspection_type: str = ""
    due_date: str = ""
class VehicleMaintenanceCompletedEvent(DomainEvent):
    event_type: str = "vehicle.maintenance.completed"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    maintenance_type: str = ""
    completed_at: str = ""
    performed_by: str = ""
class VehicleMaintenanceDueEvent(DomainEvent):
    event_type: str = "vehicle.maintenance.due"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    maintenance_type: str = ""
    due_date: str = ""
    due_mileage: str = ""
class VehicleOutOfServiceEvent(DomainEvent):
    event_type: str = "vehicle.out_of_service"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    reason: str = ""
    estimated_return: str = ""
    oos_at: str = ""
class VehicleReturnedToServiceEvent(DomainEvent):
    event_type: str = "vehicle.returned_to_service"
    entity_type: str = "vehicle"
    vehicle_id: str = ""
    returned_by: str = ""
    returned_at: str = ""
_catalog.register("certification.expired", CertificationExpiredEvent)
_catalog.register("certification.expiring", CertificationExpiringEvent)
_catalog.register("certification.renewed", CertificationRenewedEvent)
_catalog.register("crew.callout.initiated", CrewCalloutInitiatedEvent)
_catalog.register("crew.callout.response_received", CrewCalloutResponseReceivedEvent)
_catalog.register("crew.minimum_staffing.violated", CrewMinimumStaffingViolatedEvent)
_catalog.register("crew.qualification.verified", CrewQualificationVerifiedEvent)
_catalog.register("crew.roster.updated", CrewRosterUpdatedEvent)
_catalog.register("fatigue.risk.assessed", FatigueRiskAssessedEvent)
_catalog.register("performance.degradation.detected", PerformanceDegradationDetectedEvent)
_catalog.register("performance.review.completed", PerformanceReviewCompletedEvent)
_catalog.register("performance.review.scheduled", PerformanceReviewScheduledEvent)
_catalog.register("performance.threshold.exceeded", PerformanceThresholdExceededEvent)
_catalog.register("shift.overtime.approved", ShiftOvertimeApprovedEvent)
_catalog.register("shift.rostered", ShiftRosteredEvent)
_catalog.register("shift.swapped", ShiftSwappedEvent)
_catalog.register("timeoff.approved", TimeoffApprovedEvent)
_catalog.register("timeoff.denied", TimeoffDeniedEvent)
_catalog.register("timeoff.requested", TimeoffRequestedEvent)
_catalog.register("training.assessment.failed", TrainingAssessmentFailedEvent)
_catalog.register("training.assessment.passed", TrainingAssessmentPassedEvent)
_catalog.register("training.continuing_education.recorded", TrainingContinuingEducationRecordedEvent)
_catalog.register("training.course.completed", TrainingCourseCompletedEvent)
_catalog.register("training.course.enrolled", TrainingCourseEnrolledEvent)
_catalog.register("training.course.failed", TrainingCourseFailedEvent)
_catalog.register("training.course.started", TrainingCourseStartedEvent)
_catalog.register("training.module.completed", TrainingModuleCompletedEvent)
_catalog.register("training.participant.enrolled", TrainingParticipantEnrolledEvent)
_catalog.register("training.participant.withdrew", TrainingParticipantWithdrewEvent)
_catalog.register("training.session.completed", TrainingSessionCompletedEvent)
_catalog.register("training.session.scheduled", TrainingSessionScheduledEvent)
_catalog.register("training.session.started", TrainingSessionStartedEvent)
_catalog.register("training.skill.verified", TrainingSkillVerifiedEvent)
_catalog.register("vehicle.assigned", VehicleAssignedEvent)
_catalog.register("vehicle.inspection.completed", VehicleInspectionCompletedEvent)
_catalog.register("vehicle.inspection.due", VehicleInspectionDueEvent)
_catalog.register("vehicle.maintenance.completed", VehicleMaintenanceCompletedEvent)
_catalog.register("vehicle.maintenance.due", VehicleMaintenanceDueEvent)
_catalog.register("vehicle.out_of_service", VehicleOutOfServiceEvent)
_catalog.register("vehicle.returned_to_service", VehicleReturnedToServiceEvent)
