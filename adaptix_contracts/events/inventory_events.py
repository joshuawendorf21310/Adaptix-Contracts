"""Inventory domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------


class EquipmentInspectedEvent(DomainEvent):
    event_type: str = "equipment.inspected"
    entity_type: str = "equipment"

    equipment_id: str = ""
    inspection_type: str = ""
    inspection_result: str = ""
    inspected_by: str = ""
    inspected_at: str = ""


class EquipmentMaintenanceCompletedEvent(DomainEvent):
    event_type: str = "equipment.maintenance.completed"
    entity_type: str = "equipment"

    equipment_id: str = ""
    maintenance_type: str = ""
    completion_notes: str = ""
    completed_by: str = ""
    completed_at: str = ""


class EquipmentMaintenanceScheduledEvent(DomainEvent):
    event_type: str = "equipment.maintenance.scheduled"
    entity_type: str = "equipment"

    equipment_id: str = ""
    maintenance_type: str = ""
    scheduled_date: str = ""
    scheduled_by: str = ""


class InventoryItemAddedEvent(DomainEvent):
    event_type: str = "inventory.item.added"
    entity_type: str = "inventory"

    item_id: str = ""
    item_name: str = ""
    quantity: str = ""
    location_id: str = ""


class InventoryItemRemovedEvent(DomainEvent):
    event_type: str = "inventory.item.removed"
    entity_type: str = "inventory"

    item_id: str = ""
    quantity: str = ""
    reason: str = ""
    removed_by: str = ""


class InventoryLotExpiredEvent(DomainEvent):
    event_type: str = "inventory.lot.expired"
    entity_type: str = "inventory"

    lot_id: str = ""
    item_id: str = ""
    quantity: str = ""
    expired_at: str = ""


class InventoryLotReceivedEvent(DomainEvent):
    event_type: str = "inventory.lot.received"
    entity_type: str = "inventory"

    lot_id: str = ""
    item_id: str = ""
    quantity: str = ""
    expiration_date: str = ""
    received_at: str = ""


class InventoryOrderPlacedEvent(DomainEvent):
    event_type: str = "inventory.order.placed"
    entity_type: str = "inventory"

    order_id: str = ""
    supplier_id: str = ""
    items: str = ""
    total_cost: str = ""
    placed_at: str = ""


class InventoryOrderReceivedEvent(DomainEvent):
    event_type: str = "inventory.order.received"
    entity_type: str = "inventory"

    order_id: str = ""
    received_by: str = ""
    discrepancies: str = ""
    received_at: str = ""


class InventoryParLevelUpdatedEvent(DomainEvent):
    event_type: str = "inventory.par_level.updated"
    entity_type: str = "inventory"

    item_id: str = ""
    location_id: str = ""
    previous_par: str = ""
    new_par: str = ""
    updated_by: str = ""


class InventoryRecallInitiatedEvent(DomainEvent):
    event_type: str = "inventory.recall.initiated"
    entity_type: str = "inventory"

    recall_id: str = ""
    item_id: str = ""
    lot_numbers: str = ""
    reason: str = ""
    initiated_at: str = ""


class InventoryRecallItemRemovedEvent(DomainEvent):
    event_type: str = "inventory.recall.item_removed"
    entity_type: str = "inventory"

    recall_id: str = ""
    item_id: str = ""
    location_id: str = ""
    quantity: str = ""
    removed_by: str = ""


class InventoryReorderTriggeredEvent(DomainEvent):
    event_type: str = "inventory.reorder.triggered"
    entity_type: str = "inventory"

    item_id: str = ""
    current_quantity: str = ""
    reorder_point: str = ""
    triggered_at: str = ""


class InventoryTransactionRecordedEvent(DomainEvent):
    event_type: str = "inventory.transaction.recorded"
    entity_type: str = "inventory"

    transaction_id: str = ""
    item_id: str = ""
    quantity: str = ""
    transaction_type: str = ""
    actor_id: str = ""


class NarcoticAdministeredEvent(DomainEvent):
    event_type: str = "narcotic.administered"
    entity_type: str = "narcotic"

    narcotic_id: str = ""
    patient_id: str = ""
    dose: str = ""
    route: str = ""
    administered_by: str = ""
    witness_id: str = ""
    administered_at: str = ""


class NarcoticAuditCompletedEvent(DomainEvent):
    event_type: str = "narcotic.audit.completed"
    entity_type: str = "narcotic"

    audit_id: str = ""
    discrepancies_found: str = ""
    completed_at: str = ""


class NarcoticAuditInitiatedEvent(DomainEvent):
    event_type: str = "narcotic.audit.initiated"
    entity_type: str = "narcotic"

    audit_id: str = ""
    vault_id: str = ""
    initiated_by: str = ""
    initiated_at: str = ""


class NarcoticChainOfCustodyTransferredEvent(DomainEvent):
    event_type: str = "narcotic.chain_of_custody.transferred"
    entity_type: str = "narcotic"

    narcotic_id: str = ""
    from_custodian_id: str = ""
    to_custodian_id: str = ""
    transferred_at: str = ""


class NarcoticCountCompletedEvent(DomainEvent):
    event_type: str = "narcotic.count.completed"
    entity_type: str = "narcotic"

    count_id: str = ""
    location_id: str = ""
    expected_count: int = 0
    actual_count: int = 0
    counted_by: str = ""
    witness_id: str = ""


class NarcoticCountDiscrepancyEvent(DomainEvent):
    event_type: str = "narcotic.count.discrepancy"
    entity_type: str = "narcotic"

    count_id: str = ""
    narcotic_id: str = ""
    expected: str = ""
    actual: str = ""
    variance: str = ""


class NarcoticDiversionSuspectedEvent(DomainEvent):
    event_type: str = "narcotic.diversion.suspected"
    entity_type: str = "narcotic"

    alert_id: str = ""
    narcotic_id: str = ""
    suspected_user_id: str = ""
    evidence: str = ""
    detected_at: str = ""


class NarcoticVaultClosedEvent(DomainEvent):
    event_type: str = "narcotic.vault.closed"
    entity_type: str = "narcotic"

    vault_id: str = ""
    closed_by: str = ""
    witness_id: str = ""
    closed_at: str = ""


class NarcoticVaultOpenedEvent(DomainEvent):
    event_type: str = "narcotic.vault.opened"
    entity_type: str = "narcotic"

    vault_id: str = ""
    opened_by: str = ""
    witness_id: str = ""
    opened_at: str = ""


class NarcoticWastedEvent(DomainEvent):
    event_type: str = "narcotic.wasted"
    entity_type: str = "narcotic"

    narcotic_id: str = ""
    quantity: str = ""
    reason: str = ""
    wasted_by: str = ""
    witness_id: str = ""
    wasted_at: str = ""


class SupplyDistributionCompletedEvent(DomainEvent):
    event_type: str = "supply.distribution.completed"
    entity_type: str = "supply"

    distribution_id: str = ""
    items_transferred: str = ""
    completed_at: str = ""


class SupplyDistributionScheduledEvent(DomainEvent):
    event_type: str = "supply.distribution.scheduled"
    entity_type: str = "supply"

    distribution_id: str = ""
    source_location: str = ""
    destination_location: str = ""
    scheduled_date: str = ""


class SupplyLowStockAlertedEvent(DomainEvent):
    event_type: str = "supply.low_stock.alerted"
    entity_type: str = "supply"

    item_id: str = ""
    current_quantity: str = ""
    minimum_quantity: str = ""
    alerted_at: str = ""


class SupplyOutOfStockEvent(DomainEvent):
    event_type: str = "supply.out_of_stock"
    entity_type: str = "supply"

    item_id: str = ""
    location_id: str = ""
    reported_at: str = ""


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("equipment.inspected", EquipmentInspectedEvent)
_catalog.register("equipment.maintenance.completed", EquipmentMaintenanceCompletedEvent)
_catalog.register("equipment.maintenance.scheduled", EquipmentMaintenanceScheduledEvent)
_catalog.register("inventory.item.added", InventoryItemAddedEvent)
_catalog.register("inventory.item.removed", InventoryItemRemovedEvent)
_catalog.register("inventory.lot.expired", InventoryLotExpiredEvent)
_catalog.register("inventory.lot.received", InventoryLotReceivedEvent)
_catalog.register("inventory.order.placed", InventoryOrderPlacedEvent)
_catalog.register("inventory.order.received", InventoryOrderReceivedEvent)
_catalog.register("inventory.par_level.updated", InventoryParLevelUpdatedEvent)
_catalog.register("inventory.recall.initiated", InventoryRecallInitiatedEvent)
_catalog.register("inventory.recall.item_removed", InventoryRecallItemRemovedEvent)
_catalog.register("inventory.reorder.triggered", InventoryReorderTriggeredEvent)
_catalog.register("inventory.transaction.recorded", InventoryTransactionRecordedEvent)
_catalog.register("narcotic.administered", NarcoticAdministeredEvent)
_catalog.register("narcotic.audit.completed", NarcoticAuditCompletedEvent)
_catalog.register("narcotic.audit.initiated", NarcoticAuditInitiatedEvent)
_catalog.register("narcotic.chain_of_custody.transferred", NarcoticChainOfCustodyTransferredEvent)
_catalog.register("narcotic.count.completed", NarcoticCountCompletedEvent)
_catalog.register("narcotic.count.discrepancy", NarcoticCountDiscrepancyEvent)
_catalog.register("narcotic.diversion.suspected", NarcoticDiversionSuspectedEvent)
_catalog.register("narcotic.vault.closed", NarcoticVaultClosedEvent)
_catalog.register("narcotic.vault.opened", NarcoticVaultOpenedEvent)
_catalog.register("narcotic.wasted", NarcoticWastedEvent)
_catalog.register("supply.distribution.completed", SupplyDistributionCompletedEvent)
_catalog.register("supply.distribution.scheduled", SupplyDistributionScheduledEvent)
_catalog.register("supply.low_stock.alerted", SupplyLowStockAlertedEvent)
_catalog.register("supply.out_of_stock", SupplyOutOfStockEvent)
