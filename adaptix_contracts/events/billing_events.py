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
