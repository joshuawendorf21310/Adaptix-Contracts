import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from adaptix_contracts.types.enums import (
    AssetStatus,
    CycleCountStatus,
    ItemCategory,
    ItemStatus,
    LocationType,
    MaintenanceType,
    PurchaseOrderStatus,
    InventoryTransactionType as TransactionType,
)


# InventoryItem Schemas
class InventoryItemCreateRequest(BaseModel):
    item_name: str = Field(max_length=255)
    item_category: ItemCategory
    sku: str = Field(max_length=64)
    unit_of_measure: str = Field(max_length=32)
    reorder_level: int = Field(ge=0, default=0)
    reorder_quantity: int = Field(ge=0, default=0)
    storage_location: str | None = Field(default=None, max_length=255)
    supplier_id: uuid.UUID | None = None
    cost_per_unit: float | None = Field(default=None, ge=0)
    current_stock: int = Field(ge=0, default=0)
    barcode: str | None = Field(default=None, max_length=128)
    expiration_date: date | None = None
    lot_number: str | None = Field(default=None, max_length=64)
    description: str | None = None


class InventoryItemUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    item_name: str | None = Field(default=None, max_length=255)
    item_category: ItemCategory | None = None
    reorder_level: int | None = Field(default=None, ge=0)
    reorder_quantity: int | None = Field(default=None, ge=0)
    storage_location: str | None = Field(default=None, max_length=255)
    supplier_id: uuid.UUID | None = None
    cost_per_unit: float | None = Field(default=None, ge=0)
    barcode: str | None = Field(default=None, max_length=128)
    status: ItemStatus | None = None
    expiration_date: date | None = None
    lot_number: str | None = Field(default=None, max_length=64)
    description: str | None = None


class InventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    item_name: str
    item_category: ItemCategory
    sku: str
    unit_of_measure: str
    reorder_level: int
    reorder_quantity: int
    storage_location: str | None
    supplier_id: uuid.UUID | None
    cost_per_unit: float | None
    status: ItemStatus
    current_stock: int
    barcode: str | None
    expiration_date: date | None
    lot_number: str | None
    last_counted_at: datetime | None
    description: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class InventoryItemListResponse(BaseModel):
    items: list[InventoryItemResponse]
    total: int


# InventoryLocation Schemas
class InventoryLocationCreateRequest(BaseModel):
    location_name: str = Field(max_length=255)
    location_type: LocationType
    parent_location_id: uuid.UUID | None = None
    capacity: int | None = Field(default=None, ge=0)
    address: str | None = Field(default=None, max_length=500)
    notes: str | None = None


class InventoryLocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    location_name: str
    location_type: LocationType
    parent_location_id: uuid.UUID | None
    capacity: int | None
    address: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class InventoryLocationListResponse(BaseModel):
    items: list[InventoryLocationResponse]
    total: int


# InventoryTransaction Schemas
class InventoryTransactionCreateRequest(BaseModel):
    item_id: uuid.UUID
    transaction_type: TransactionType
    quantity: int
    unit_id: uuid.UUID | None = None
    location_from: uuid.UUID | None = None
    location_to: uuid.UUID | None = None
    reference_incident_id: uuid.UUID | None = None
    reference_po_id: uuid.UUID | None = None
    unit_cost: float | None = Field(default=None, ge=0)
    notes: str | None = None


class InventoryTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    item_id: uuid.UUID
    transaction_type: TransactionType
    quantity: int
    unit_id: uuid.UUID | None
    user_id: uuid.UUID
    location_from: uuid.UUID | None
    location_to: uuid.UUID | None
    transaction_date: datetime
    reference_incident_id: uuid.UUID | None
    reference_po_id: uuid.UUID | None
    unit_cost: float | None
    notes: str | None
    created_at: datetime


class InventoryTransactionListResponse(BaseModel):
    items: list[InventoryTransactionResponse]
    total: int


class InventoryBarcodeLookupRequest(BaseModel):
    barcode: str = Field(min_length=1, max_length=128)


class InventoryBarcodeLookupResponse(BaseModel):
    matched: bool
    match_type: str | None = None
    item: InventoryItemResponse | None = None


class InventoryBatchTransactionRequest(BaseModel):
    transactions: list[InventoryTransactionCreateRequest] = Field(min_length=1, max_length=100)


class InventoryBatchTransactionResponse(BaseModel):
    items: list[InventoryTransactionResponse]
    total: int


# Transfer Request
class InventoryTransferRequest(BaseModel):
    item_id: uuid.UUID
    from_location: uuid.UUID
    to_location: uuid.UUID
    quantity: int = Field(gt=0)
    notes: str | None = None


# Usage Request
class InventoryUsageItem(BaseModel):
    item_id: uuid.UUID
    quantity: int = Field(gt=0)
    location_id: uuid.UUID | None = None


class InventoryUsageRequest(BaseModel):
    incident_id: uuid.UUID
    items: list[InventoryUsageItem]
    notes: str | None = None


# EquipmentAsset Schemas
class EquipmentAssetCreateRequest(BaseModel):
    asset_name: str = Field(max_length=255)
    asset_type: str = Field(max_length=128)
    serial_number: str = Field(max_length=128)
    purchase_date: date | None = None
    warranty_expiration: date | None = None
    maintenance_schedule: str | None = Field(default=None, max_length=128)
    assigned_location_id: uuid.UUID | None = None
    manufacturer: str | None = Field(default=None, max_length=255)
    model: str | None = Field(default=None, max_length=255)
    purchase_price: float | None = Field(default=None, ge=0)
    description: str | None = None


class EquipmentAssetUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    asset_name: str | None = Field(default=None, max_length=255)
    asset_type: str | None = Field(default=None, max_length=128)
    warranty_expiration: date | None = None
    maintenance_schedule: str | None = Field(default=None, max_length=128)
    assigned_location_id: uuid.UUID | None = None
    status: AssetStatus | None = None
    description: str | None = None


class EquipmentAssetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    asset_name: str
    asset_type: str
    serial_number: str
    purchase_date: date | None
    warranty_expiration: date | None
    maintenance_schedule: str | None
    assigned_location_id: uuid.UUID | None
    status: AssetStatus
    manufacturer: str | None
    model: str | None
    purchase_price: float | None
    description: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class EquipmentAssetListResponse(BaseModel):
    items: list[EquipmentAssetResponse]
    total: int


# MaintenanceRecord Schemas
class MaintenanceRecordCreateRequest(BaseModel):
    asset_id: uuid.UUID
    maintenance_type: MaintenanceType
    maintenance_date: datetime
    next_due_date: date | None = None
    cost: float | None = Field(default=None, ge=0)
    notes: str | None = None
    work_performed: str | None = None
    parts_used: dict = Field(default_factory=dict)


class MaintenanceRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    asset_id: uuid.UUID
    maintenance_type: MaintenanceType
    performed_by: uuid.UUID
    maintenance_date: datetime
    next_due_date: date | None
    cost: float | None
    notes: str | None
    work_performed: str | None
    parts_used: dict
    created_at: datetime


class MaintenanceRecordListResponse(BaseModel):
    items: list[MaintenanceRecordResponse]
    total: int


# Supplier Schemas
class SupplierCreateRequest(BaseModel):
    supplier_name: str = Field(max_length=255)
    contact_name: str | None = Field(default=None, max_length=255)
    contact_email: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=32)
    address: str | None = Field(default=None, max_length=500)
    payment_terms: str | None = Field(default=None, max_length=128)
    lead_time_days: int | None = Field(default=None, ge=0)
    notes: str | None = None


class SupplierResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    supplier_name: str
    contact_name: str | None
    contact_email: str | None
    contact_phone: str | None
    address: str | None
    payment_terms: str | None
    lead_time_days: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class SupplierListResponse(BaseModel):
    items: list[SupplierResponse]
    total: int


# PurchaseOrder Schemas
class PurchaseOrderItem(BaseModel):
    item_id: uuid.UUID
    quantity: int = Field(gt=0)
    unit_cost: float = Field(ge=0)


class PurchaseOrderCreateRequest(BaseModel):
    supplier_id: uuid.UUID
    expected_delivery: date | None = None
    items: list[PurchaseOrderItem]
    notes: str | None = None


class PurchaseOrderUpdateRequest(BaseModel):
    version: int = Field(ge=1)
    expected_delivery: date | None = None
    status: PurchaseOrderStatus | None = None
    notes: str | None = None


class ReceivingLineItem(BaseModel):
    item_id: uuid.UUID
    quantity_received: int = Field(gt=0)
    quantity_expected: int | None = Field(default=None, gt=0)


class ReceivingVarianceEntry(BaseModel):
    item_id: uuid.UUID
    item_name: str
    sku: str
    quantity_ordered: int
    quantity_received: int
    variance: int
    variance_pct: float


class PurchaseOrderReceiveRequest(BaseModel):
    version: int = Field(ge=1)
    items_received: list[ReceivingLineItem]
    actual_delivery: date


class PurchaseOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    po_number: str
    supplier_id: uuid.UUID
    order_date: datetime
    expected_delivery: date | None
    actual_delivery: date | None
    status: PurchaseOrderStatus
    total_cost: float
    items_json: dict
    notes: str | None
    created_by: uuid.UUID
    approved_by: uuid.UUID | None
    approved_at: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime


class PurchaseOrderListResponse(BaseModel):
    items: list[PurchaseOrderResponse]
    total: int


class AutoDraftPoSummaryEntry(BaseModel):
    supplier_id: uuid.UUID
    supplier_name: str
    po_id: uuid.UUID
    po_number: str
    item_count: int
    total_cost: float


class AutoDraftPoSummaryResponse(BaseModel):
    total_pos_created: int
    skipped_no_supplier: int
    skipped_no_reorder_quantity: int
    purchase_orders: list[AutoDraftPoSummaryEntry]


class IncidentCostLineItem(BaseModel):
    transaction_id: uuid.UUID
    item_id: uuid.UUID
    item_name: str
    sku: str
    quantity: int
    unit_cost: float
    total_cost: float
    transaction_date: datetime


class IncidentCostReportResponse(BaseModel):
    incident_id: uuid.UUID
    total_cost: float
    transaction_count: int
    line_items: list[IncidentCostLineItem]


# Report Schemas
class StockLevelReport(BaseModel):
    item_id: uuid.UUID
    item_name: str
    sku: str
    current_stock: int
    reorder_level: int
    status: ItemStatus


class StockLevelReportResponse(BaseModel):
    items: list[StockLevelReport]
    total: int


class ExpiringItemReport(BaseModel):
    item_id: uuid.UUID
    item_name: str
    sku: str
    current_stock: int
    expiration_date: date
    days_until_expiration: int


class ExpiringItemReportResponse(BaseModel):
    items: list[ExpiringItemReport]
    total: int


class InventoryStatsByTypeEntry(BaseModel):
    count: int
    value: float


class InventoryMonthlyUsageEntry(BaseModel):
    month: str
    total_transactions: int
    total_cost: float


class InventoryStatsResponse(BaseModel):
    total_items: int
    total_value: float
    low_stock_count: int
    out_of_stock_count: int
    expiring_soon_count: int
    cycle_counts_open: int
    discrepancies_open: int
    by_type: dict[str, InventoryStatsByTypeEntry]
    by_location: dict[str, InventoryStatsByTypeEntry]
    monthly_usage_trend: list[InventoryMonthlyUsageEntry]


class InventoryAlertResponse(BaseModel):
    id: str
    item_name: str
    current_quantity: int
    min_quantity: int
    unit: str
    location: str
    severity: str
    category: str
    expiring_soon: bool = False


class NarcoticDiscrepancyResponse(BaseModel):
    id: str
    medication_name: str
    expected_count: int
    actual_count: int
    difference: int
    last_audit: str
    unit_id: str
    status: str


class InventoryAlertMetricsResponse(BaseModel):
    low_stock_alerts: int
    critical_stock_items: int
    narcotic_discrepancies: int
    items_expiring_30_days: int


class InventoryAlertsDashboardResponse(BaseModel):
    alerts: list[InventoryAlertResponse]
    narcotic_discrepancies: list[NarcoticDiscrepancyResponse]
    metrics: InventoryAlertMetricsResponse


class InventoryCycleCountCreateRequest(BaseModel):
    count_name: str = Field(min_length=1, max_length=255)
    location_id: uuid.UUID | None = None
    item_category: ItemCategory | None = None
    is_controlled_substance: bool = False
    notes: str | None = None


class InventoryCycleCountLineUpsertRequest(BaseModel):
    item_id: uuid.UUID
    counted_quantity: int = Field(ge=0)
    scanned_barcode: str | None = Field(default=None, max_length=128)
    notes: str | None = None


class InventoryCycleCountCompleteRequest(BaseModel):
    auto_reconcile: bool = False


class CycleCountWitnessAffirmRequest(BaseModel):
    witness_user_id: uuid.UUID


class InventoryCycleCountLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    cycle_count_id: uuid.UUID
    item_id: uuid.UUID
    expected_quantity: int
    counted_quantity: int
    variance_quantity: int
    counted_by: uuid.UUID
    counted_at: datetime
    scanned_barcode: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime


class InventoryCycleCountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    count_name: str
    status: CycleCountStatus
    location_id: uuid.UUID | None
    scope_snapshot: dict
    started_by: uuid.UUID
    started_at: datetime
    completed_by: uuid.UUID | None
    completed_at: datetime | None
    total_items: int
    counted_items: int
    discrepancy_count: int
    notes: str | None
    is_controlled_substance: bool
    witness_user_id: uuid.UUID | None
    witness_affirmed_at: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime


class InventoryCycleCountListResponse(BaseModel):
    items: list[InventoryCycleCountResponse]
    total: int


class InventoryLocationReadinessSummary(BaseModel):
    location_id: uuid.UUID | None = None
    location_name: str | None = None
    location_type: str | None = None
    item_count: int = 0
    low_stock_count: int = 0
    out_of_stock_count: int = 0
    expiring_soon_count: int = 0
    active_asset_count: int = 0
    maintenance_asset_count: int = 0
    readiness_score: float = 0.0
    readiness_status: str | None = None
    readiness_issues: list[str] = Field(default_factory=list)


class InventoryReadinessSummaryResponse(BaseModel):
    generated_at: datetime | None = None
    total_locations: int = 0
    degraded_locations: int = 0
    critical_locations: int = 0
    locations: list[InventoryLocationReadinessSummary] = Field(default_factory=list)


class InventoryEventFeedEntry(BaseModel):
    event_type: str | None = None
    severity: str | None = None
    occurred_at: datetime | None = None
    title: str | None = None
    detail: str | None = None
    item_id: uuid.UUID | None = None
    item_name: str | None = None
    location_name: str | None = None
    incident_id: uuid.UUID | None = None
    unit_id: uuid.UUID | None = None
    reference_id: uuid.UUID | None = None


class InventoryEventFeedResponse(BaseModel):
    items: list[InventoryEventFeedEntry] = Field(default_factory=list)
    total: int = 0


class InventoryLocationReadinessSummary(BaseModel):
    location_id: uuid.UUID | None = None
    location_name: str | None = None
    location_type: str | None = None
    item_count: int = 0
    low_stock_count: int = 0
    out_of_stock_count: int = 0
    expiring_soon_count: int = 0
    active_asset_count: int = 0
    maintenance_asset_count: int = 0
    readiness_score: float = 0.0
    readiness_status: str | None = None
    readiness_issues: list[str] = Field(default_factory=list)


class InventoryReadinessSummaryResponse(BaseModel):
    generated_at: datetime | None = None
    total_locations: int = 0
    degraded_locations: int = 0
    critical_locations: int = 0
    locations: list[InventoryLocationReadinessSummary] = Field(default_factory=list)


class InventoryEventFeedEntry(BaseModel):
    event_type: str | None = None
    severity: str | None = None
    occurred_at: datetime | None = None
    title: str | None = None
    detail: str | None = None
    item_id: uuid.UUID | None = None
    item_name: str | None = None
    location_name: str | None = None
    incident_id: uuid.UUID | None = None
    unit_id: uuid.UUID | None = None
    reference_id: uuid.UUID | None = None


class InventoryEventFeedResponse(BaseModel):
    items: list[InventoryEventFeedEntry] = Field(default_factory=list)
    total: int = 0
