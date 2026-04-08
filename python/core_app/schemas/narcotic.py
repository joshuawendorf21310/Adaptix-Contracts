import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from core_app.models.narcotic import (
    AccessType,
    DEASchedule,
    InvestigationStatus,
    MedicationStatus,
    TransactionType,
    VaultStatus,
    VaultType,
)


# Vault Schemas
class VaultCreateRequest(BaseModel):
    vault_name: str = Field(min_length=1, max_length=128)
    location: str = Field(min_length=1, max_length=255)
    vault_type: VaultType


class VaultUpdateRequest(BaseModel):
    vault_name: str | None = Field(default=None, min_length=1, max_length=128)
    location: str | None = Field(default=None, min_length=1, max_length=255)
    status: VaultStatus | None = None
    next_audit_date: datetime | None = None
    version: int = Field(ge=1)


class VaultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    vault_name: str
    location: str
    vault_type: VaultType
    status: VaultStatus
    last_audit_date: datetime | None
    next_audit_date: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime


class VaultListResponse(BaseModel):
    items: list[VaultResponse]
    total: int


# Medication Schemas
class MedicationCreateRequest(BaseModel):
    drug_name: str = Field(min_length=1, max_length=255)
    dea_schedule: DEASchedule
    strength: str = Field(min_length=1, max_length=64)
    form: str = Field(min_length=1, max_length=64)
    vault_id: uuid.UUID
    quantity: float = Field(ge=0)
    lot_number: str = Field(min_length=1, max_length=128)
    expiration_date: datetime


class MedicationUpdateRequest(BaseModel):
    quantity: float | None = Field(default=None, ge=0)
    status: MedicationStatus | None = None
    version: int = Field(ge=1)


class MedicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    drug_name: str
    dea_schedule: DEASchedule
    strength: str
    form: str
    vault_id: uuid.UUID
    quantity: float
    lot_number: str
    expiration_date: datetime
    status: MedicationStatus
    version: int
    created_at: datetime
    updated_at: datetime


class MedicationListResponse(BaseModel):
    items: list[MedicationResponse]
    total: int


# Transaction Schemas
class IssueNarcoticRequest(BaseModel):
    medication_id: uuid.UUID
    quantity: float = Field(gt=0)
    issued_to_user_id: uuid.UUID
    witnessed_by: uuid.UUID | None = None
    kit_id: str | None = Field(default=None, max_length=128)
    notes: str | None = Field(default=None, max_length=5000)


class ReturnNarcoticRequest(BaseModel):
    medication_id: uuid.UUID
    quantity: float = Field(gt=0)
    returned_by_user_id: uuid.UUID
    witnessed_by: uuid.UUID | None = None
    reason: str = Field(min_length=1, max_length=5000)


class AdministerNarcoticRequest(BaseModel):
    medication_id: uuid.UUID
    patient_incident_id: uuid.UUID
    dose: float = Field(gt=0)
    administered_by: uuid.UUID
    witnessed_by: uuid.UUID | None = None
    waste_amount: float | None = Field(default=None, ge=0)
    waste_witnessed_by: uuid.UUID | None = None
    notes: str | None = Field(default=None, max_length=5000)


class WasteNarcoticRequest(BaseModel):
    medication_id: uuid.UUID
    waste_amount: float = Field(gt=0)
    wasted_by: uuid.UUID
    witnessed_by: uuid.UUID | None = None
    reason: str = Field(min_length=1, max_length=5000)


class TransferNarcoticRequest(BaseModel):
    medication_id: uuid.UUID
    from_vault_id: uuid.UUID
    to_vault_id: uuid.UUID
    quantity: float = Field(gt=0)
    authorized_by: uuid.UUID
    transferred_by: uuid.UUID
    witnessed_by: uuid.UUID | None = None
    notes: str | None = Field(default=None, max_length=5000)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    medication_id: uuid.UUID
    transaction_type: TransactionType
    quantity: float
    administered_by: uuid.UUID
    witnessed_by: uuid.UUID | None
    patient_incident_id: uuid.UUID | None
    transaction_time: datetime
    pre_count: float
    post_count: float
    waste_amount: float | None
    waste_witnessed_by: uuid.UUID | None
    signature_required: bool
    signature_captured: bool
    notes: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class TransactionListResponse(BaseModel):
    items: list[TransactionResponse]
    total: int


# Audit Schemas
class ConductAuditRequest(BaseModel):
    vault_id: uuid.UUID
    auditor_id: uuid.UUID
    witness_id: uuid.UUID
    medication_counts: dict[str, float]  # medication_id -> actual_count
    notes: str | None = Field(default=None, max_length=5000)


class AuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    vault_id: uuid.UUID
    audit_date: datetime
    auditor_id: uuid.UUID
    witness_id: uuid.UUID
    discrepancies_found: bool
    discrepancy_details_json: dict
    resolved: bool
    resolution_notes: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class AuditListResponse(BaseModel):
    items: list[AuditResponse]
    total: int


# Discrepancy Schemas
class RecordDiscrepancyRequest(BaseModel):
    audit_id: uuid.UUID
    medication_id: uuid.UUID
    expected_count: float
    actual_count: float
    variance: float


class ResolveDiscrepancyRequest(BaseModel):
    resolution_notes: str = Field(min_length=1, max_length=5000)
    resolved_by: uuid.UUID
    version: int = Field(ge=1)


class DiscrepancyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    audit_id: uuid.UUID
    medication_id: uuid.UUID
    expected_count: float
    actual_count: float
    variance: float
    investigation_status: InvestigationStatus
    resolved_by: uuid.UUID | None
    resolution_date: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime


class DiscrepancyListResponse(BaseModel):
    items: list[DiscrepancyResponse]
    total: int


# Access Log Schemas
class AccessLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    vault_id: uuid.UUID
    user_id: uuid.UUID
    access_time: datetime
    access_type: AccessType
    authorized_by: uuid.UUID | None
    notes: str | None
    version: int
    created_at: datetime
    updated_at: datetime


class AccessLogListResponse(BaseModel):
    items: list[AccessLogResponse]
    total: int


# DEA Report Schemas
class DEAReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    dea_schedule: DEASchedule | None = None


class DEAReportResponse(BaseModel):
    report_period_start: datetime
    report_period_end: datetime
    generated_at: datetime
    tenant_id: uuid.UUID
    medications: list[dict]  # Detailed medication transaction summary
    total_transactions: int
    transactions_by_type: dict[str, int]
    discrepancies: list[dict]
    compliance_notes: list[str]


# Expiring Medication Schemas
class ExpiringMedicationsRequest(BaseModel):
    days_ahead: int = Field(ge=1, le=365, default=30)


class ExpiringMedicationResponse(BaseModel):
    medication: MedicationResponse
    days_until_expiration: int
    recommended_action: str
