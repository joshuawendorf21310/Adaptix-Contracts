"""Billing and payment domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class BillingClaimCreatedEvent(DomainEvent):
    event_type: str = "billing.claim.created"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    epcr_id: str = ""
    patient_id: str = ""
    payer: str = ""

class BillingClaimSubmittedEvent(DomainEvent):
    event_type: str = "billing.claim.submitted"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    payer: str = ""
    submitted_at: str = ""

class BillingClaimPaidEvent(DomainEvent):
    event_type: str = "billing.claim.paid"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    amount_paid: float = 0.0
    paid_at: str = ""

class BillingClaimDeniedEvent(DomainEvent):
    event_type: str = "billing.claim.denied"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    denial_code: str = ""
    denial_reason: str = ""

class PaymentPostedEvent(DomainEvent):
    event_type: str = "payment.posted"
    entity_type: str = "payment"

    payment_id: str = ""
    account_id: str = ""
    amount: float = 0.0

class PaymentFailedEvent(DomainEvent):
    event_type: str = "payment.failed"
    entity_type: str = "payment"

    payment_id: str = ""
    account_id: str = ""
    error_code: str = ""

class PaymentRefundedEvent(DomainEvent):
    event_type: str = "payment.refunded"
    entity_type: str = "payment"

    payment_id: str = ""
    account_id: str = ""
    refund_amount: float = 0.0

class PatientAccountUpdatedEvent(DomainEvent):
    event_type: str = "patient.account.updated"
    entity_type: str = "patient_account"

    account_id: str = ""
    patient_id: str = ""
    status: str = ""

class PatientFinancialDisputeCreatedEvent(DomainEvent):
    event_type: str = "patient.financial.dispute.created"
    entity_type: str = "patient_dispute"

    dispute_id: str = ""
    account_id: str = ""
    amount_disputed: float = 0.0

class BillingClaimValidatedEvent(DomainEvent):
    event_type: str = "billing.claim.validated"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    validation_passed: bool = False
    validation_errors: str = ""

class BillingClaimScrubbedEvent(DomainEvent):
    event_type: str = "billing.claim.scrubbed"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    scrubber_findings: str = ""
    scrubbed_by: str = ""

class BillingClaimResubmittedEvent(DomainEvent):
    event_type: str = "billing.claim.resubmitted"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    resubmission_reason: str = ""
    original_submission_id: str = ""

class BillingClaimAppealedEvent(DomainEvent):
    event_type: str = "billing.claim.appealed"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    appeal_reason: str = ""
    appeal_level: str = ""

class BillingClaimAppealWonEvent(DomainEvent):
    event_type: str = "billing.claim.appeal_won"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    appeal_id: str = ""
    awarded_amount: float = 0.0

class BillingClaimAppealLostEvent(DomainEvent):
    event_type: str = "billing.claim.appeal_lost"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    appeal_id: str = ""

class BillingRemittanceReceivedEvent(DomainEvent):
    event_type: str = "billing.remittance.received"
    entity_type: str = "billing_remittance"

    remittance_id: str = ""
    payer: str = ""
    received_at: str = ""

class BillingRemittancePostedEvent(DomainEvent):
    event_type: str = "billing.remittance.posted"
    entity_type: str = "billing_remittance"

    remittance_id: str = ""
    posted_at: str = ""
    posted_by: str = ""

class BillingChargeAddedEvent(DomainEvent):
    event_type: str = "billing.charge.added"
    entity_type: str = "billing_charge"

    charge_id: str = ""
    claim_id: str = ""
    charge_code: str = ""
    amount: float = 0.0

class PatientFinancialResponsibilityDeterminedEvent(DomainEvent):
    event_type: str = "patient.financial_responsibility.determined"
    entity_type: str = "patient_account"

    patient_id: str = ""
    claim_id: str = ""
    patient_responsibility: float = 0.0

class PatientPaymentPlanCreatedEvent(DomainEvent):
    event_type: str = "patient.payment_plan.created"
    entity_type: str = "payment_plan"

    plan_id: str = ""
    account_id: str = ""
    monthly_amount: float = 0.0

class PatientPaymentPlanPaymentMadeEvent(DomainEvent):
    event_type: str = "patient.payment_plan.payment_made"
    entity_type: str = "payment_plan"

    plan_id: str = ""
    payment_amount: float = 0.0
    payment_date: str = ""

class PatientPaymentPlanDefaultedEvent(DomainEvent):
    event_type: str = "patient.payment_plan.defaulted"
    entity_type: str = "payment_plan"

    plan_id: str = ""
    defaulted_at: str = ""

class PatientSentToCollectionsEvent(DomainEvent):
    event_type: str = "patient.sent_to_collections"
    entity_type: str = "patient_account"

    account_id: str = ""
    collections_agency: str = ""
    sent_at: str = ""

class PatientPortalInviteSentEvent(DomainEvent):
    event_type: str = "patient.portal.invite_sent"
    entity_type: str = "patient_portal"

    patient_id: str = ""
    sent_at: str = ""

class PatientPortalActivatedEvent(DomainEvent):
    event_type: str = "patient.portal.activated"
    entity_type: str = "patient_portal"

    patient_id: str = ""
    activated_at: str = ""

class PatientPortalPaymentMadeEvent(DomainEvent):
    event_type: str = "patient.portal.payment_made"
    entity_type: str = "patient_payment"

    patient_id: str = ""
    payment_id: str = ""
    amount: float = 0.0

class SmsBillingSentEvent(DomainEvent):
    event_type: str = "sms.billing.sent"
    entity_type: str = "sms_message"

    message_id: str = ""
    patient_id: str = ""
    account_id: str = ""

class BillingBatchCreatedEvent(DomainEvent):
    event_type: str = "billing.batch.created"
    entity_type: str = "billing_batch"

    batch_id: str = ""
    claim_count: int = 0
    created_by: str = ""

class BillingEligibilityVerifiedEvent(DomainEvent):
    event_type: str = "billing.eligibility.verified"
    entity_type: str = "insurance_eligibility"

    patient_id: str = ""
    payer_id: str = ""
    is_eligible: bool = False
    verified_at: str = ""

class BillingPriorAuthRequestedEvent(DomainEvent):
    event_type: str = "billing.prior_auth.requested"
    entity_type: str = "prior_authorization"

    auth_id: str = ""
    patient_id: str = ""
    payer_id: str = ""
    service_codes: str = ""
    requested_at: str = ""

class BillingPriorAuthApprovedEvent(DomainEvent):
    event_type: str = "billing.prior_auth.approved"
    entity_type: str = "prior_authorization"

    auth_id: str = ""
    approval_number: str = ""
    approved_at: str = ""
    valid_until: str = ""

class BillingPriorAuthDeniedEvent(DomainEvent):
    event_type: str = "billing.prior_auth.denied"
    entity_type: str = "prior_authorization"

    auth_id: str = ""
    denial_reason: str = ""

class BillingEobReceivedEvent(DomainEvent):
    event_type: str = "billing.eob.received"
    entity_type: str = "explanation_of_benefits"

    eob_id: str = ""
    claim_id: str = ""
    payer: str = ""
    received_at: str = ""

class BillingWriteoffCreatedEvent(DomainEvent):
    event_type: str = "billing.writeoff.created"
    entity_type: str = "billing_writeoff"

    writeoff_id: str = ""
    account_id: str = ""
    amount: float = 0.0
    reason: str = ""
    created_by: str = ""

class BillingBatchSubmittedEvent(DomainEvent):
    event_type: str = "billing.batch.submitted"
    entity_type: str = "billing_batch"

    batch_id: str = ""
    submission_method: str = ""
    submitted_at: str = ""

class BillingBatchAcknowledgedEvent(DomainEvent):
    event_type: str = "billing.batch.acknowledged"
    entity_type: str = "billing_batch"

    batch_id: str = ""
    acknowledgment_id: str = ""
    acknowledged_at: str = ""

class BillingClaimPendedEvent(DomainEvent):
    event_type: str = "billing.claim.pended"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    pend_reason: str = ""
    additional_info_required: str = ""

class BillingClaimAdjustedEvent(DomainEvent):
    event_type: str = "billing.claim.adjusted"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    adjustment_reason: str = ""
    adjustment_amount: float = 0.0
    adjusted_at: str = ""

class BillingClaimReversedEvent(DomainEvent):
    event_type: str = "billing.claim.reversed"
    entity_type: str = "billing_claim"

    claim_id: str = ""
    reversal_reason: str = ""
    reversed_by: str = ""
    reversed_at: str = ""

class BillingAgingBucketChangedEvent(DomainEvent):
    event_type: str = "billing.aging.bucket_changed"
    entity_type: str = "patient_account"

    account_id: str = ""
    previous_bucket: str = ""
    new_bucket: str = ""
    days_outstanding: int = 0

class BillingCollectionsLetterSentEvent(DomainEvent):
    event_type: str = "billing.collections.letter_sent"
    entity_type: str = "collections_letter"

    account_id: str = ""
    letter_type: str = ""
    letter_number: int = 0
    sent_at: str = ""

class BillingChargePostedEvent(DomainEvent):
    event_type: str = "billing.charge.posted"
    entity_type: str = "billing_charge"

    charge_id: str = ""
    encounter_id: str = ""
    charge_code: str = ""
    amount: float = 0.0
    posted_at: str = ""

class BillingChargeAdjustedEvent(DomainEvent):
    event_type: str = "billing.charge.adjusted"
    entity_type: str = "billing_charge"

    charge_id: str = ""
    adjustment_type: str = ""
    adjustment_amount: float = 0.0
    adjusted_by: str = ""

class BillingChargeReversedEvent(DomainEvent):
    event_type: str = "billing.charge.reversed"
    entity_type: str = "billing_charge"

    charge_id: str = ""
    reversal_reason: str = ""
    reversed_by: str = ""
    reversed_at: str = ""

class BillingPaymentPostedEvent(DomainEvent):
    event_type: str = "billing.payment.posted"
    entity_type: str = "billing_payment"

    payment_id: str = ""
    account_id: str = ""
    amount: float = 0.0
    payment_method: str = ""
    posted_at: str = ""

class BillingPaymentRefundedEvent(DomainEvent):
    event_type: str = "billing.payment.refunded"
    entity_type: str = "billing_payment"

    payment_id: str = ""
    refund_amount: float = 0.0
    refund_reason: str = ""
    refunded_at: str = ""

class BillingStatementGeneratedEvent(DomainEvent):
    event_type: str = "billing.statement.generated"
    entity_type: str = "billing_statement"

    statement_id: str = ""
    account_id: str = ""
    statement_date: str = ""
    balance: float = 0.0

class BillingStatementSentEvent(DomainEvent):
    event_type: str = "billing.statement.sent"
    entity_type: str = "billing_statement"

    statement_id: str = ""
    delivery_method: str = ""
    sent_at: str = ""

class BillingAccountFlaggedEvent(DomainEvent):
    event_type: str = "billing.account.flagged"
    entity_type: str = "patient_account"

    account_id: str = ""
    flag_type: str = ""
    flag_reason: str = ""
    flagged_by: str = ""

class BillingAccountUnflaggedEvent(DomainEvent):
    event_type: str = "billing.account.unflagged"
    entity_type: str = "patient_account"

    account_id: str = ""
    flag_type: str = ""
    unflagged_by: str = ""
    unflagged_at: str = ""

class PatientInsuranceVerifiedEvent(DomainEvent):
    event_type: str = "patient.insurance.verified"
    entity_type: str = "patient_insurance"

    patient_id: str = ""
    insurance_id: str = ""
    verified_at: str = ""
    coverage_active: bool = False

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("billing.claim.created", BillingClaimCreatedEvent)
_catalog.register("billing.claim.submitted", BillingClaimSubmittedEvent)
_catalog.register("billing.claim.paid", BillingClaimPaidEvent)
_catalog.register("billing.claim.denied", BillingClaimDeniedEvent)
_catalog.register("payment.posted", PaymentPostedEvent)
_catalog.register("payment.failed", PaymentFailedEvent)
_catalog.register("payment.refunded", PaymentRefundedEvent)
_catalog.register("patient.account.updated", PatientAccountUpdatedEvent)
_catalog.register("patient.financial.dispute.created", PatientFinancialDisputeCreatedEvent)
_catalog.register("billing.claim.validated", BillingClaimValidatedEvent)
_catalog.register("billing.claim.scrubbed", BillingClaimScrubbedEvent)
_catalog.register("billing.claim.resubmitted", BillingClaimResubmittedEvent)
_catalog.register("billing.claim.appealed", BillingClaimAppealedEvent)
_catalog.register("billing.claim.appeal_won", BillingClaimAppealWonEvent)
_catalog.register("billing.claim.appeal_lost", BillingClaimAppealLostEvent)
_catalog.register("billing.remittance.received", BillingRemittanceReceivedEvent)
_catalog.register("billing.remittance.posted", BillingRemittancePostedEvent)
_catalog.register("billing.charge.added", BillingChargeAddedEvent)
_catalog.register("patient.financial_responsibility.determined", PatientFinancialResponsibilityDeterminedEvent)
_catalog.register("patient.payment_plan.created", PatientPaymentPlanCreatedEvent)
_catalog.register("patient.payment_plan.payment_made", PatientPaymentPlanPaymentMadeEvent)
_catalog.register("patient.payment_plan.defaulted", PatientPaymentPlanDefaultedEvent)
_catalog.register("patient.sent_to_collections", PatientSentToCollectionsEvent)
_catalog.register("patient.portal.invite_sent", PatientPortalInviteSentEvent)
_catalog.register("patient.portal.activated", PatientPortalActivatedEvent)
_catalog.register("patient.portal.payment_made", PatientPortalPaymentMadeEvent)
_catalog.register("sms.billing.sent", SmsBillingSentEvent)
_catalog.register("billing.batch.created", BillingBatchCreatedEvent)
_catalog.register("billing.eligibility.verified", BillingEligibilityVerifiedEvent)
_catalog.register("billing.prior_auth.requested", BillingPriorAuthRequestedEvent)
_catalog.register("billing.prior_auth.approved", BillingPriorAuthApprovedEvent)
_catalog.register("billing.prior_auth.denied", BillingPriorAuthDeniedEvent)
_catalog.register("billing.eob.received", BillingEobReceivedEvent)
_catalog.register("billing.writeoff.created", BillingWriteoffCreatedEvent)
_catalog.register("billing.batch.submitted", BillingBatchSubmittedEvent)
_catalog.register("billing.batch.acknowledged", BillingBatchAcknowledgedEvent)
_catalog.register("billing.claim.pended", BillingClaimPendedEvent)
_catalog.register("billing.claim.adjusted", BillingClaimAdjustedEvent)
_catalog.register("billing.claim.reversed", BillingClaimReversedEvent)
_catalog.register("billing.aging.bucket_changed", BillingAgingBucketChangedEvent)
_catalog.register("billing.collections.letter_sent", BillingCollectionsLetterSentEvent)
_catalog.register("billing.charge.posted", BillingChargePostedEvent)
_catalog.register("billing.charge.adjusted", BillingChargeAdjustedEvent)
_catalog.register("billing.charge.reversed", BillingChargeReversedEvent)
_catalog.register("billing.payment.posted", BillingPaymentPostedEvent)
_catalog.register("billing.payment.refunded", BillingPaymentRefundedEvent)
_catalog.register("billing.statement.generated", BillingStatementGeneratedEvent)
_catalog.register("billing.statement.sent", BillingStatementSentEvent)
_catalog.register("billing.account.flagged", BillingAccountFlaggedEvent)
_catalog.register("billing.account.unflagged", BillingAccountUnflaggedEvent)
_catalog.register("patient.insurance.verified", PatientInsuranceVerifiedEvent)
