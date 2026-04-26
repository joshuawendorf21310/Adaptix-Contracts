"""Medication operations contracts shared across Adaptix services."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class MedicationRouteOfAdmin(str, enum.Enum):
    ORAL = "oral"
    INTRAVENOUS = "intravenous"
    INTRAMUSCULAR = "intramuscular"
    SUBCUTANEOUS = "subcutaneous"
    INHALATION = "inhalation"
    TOPICAL = "topical"
    SUBLINGUAL = "sublingual"
    RECTAL = "rectal"
    INTRANASAL = "intranasal"
    INTRAOSSEOUS = "intraosseous"
    ENDOTRACHEAL = "endotracheal"
    NEBULIZED = "nebulized"
    OPHTHALMIC = "ophthalmic"
    OTIC = "otic"
    OTHER = "other"


class DoseSafetyStatus(str, enum.Enum):
    SAFE = "safe"
    WARNING = "warning"
    CONTRAINDICATED = "contraindicated"
    REQUIRES_OVERRIDE = "requires_override"


class MedicationCatalogContract(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    generic_name: Optional[str] = None
    rxcui: Optional[str] = None
    ndc: Optional[str] = None
    drug_class: Optional[str] = None
    controlled_substance: bool = False
    dea_schedule: Optional[str] = None
    default_dose: Optional[str] = None
    default_unit: Optional[str] = None
    default_route: Optional[MedicationRouteOfAdmin] = None
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None


class MedicationAdministrationContract(BaseModel):
    id: UUID
    tenant_id: UUID
    medication_id: UUID
    patient_id: Optional[UUID] = None
    incident_id: Optional[UUID] = None
    chart_id: Optional[UUID] = None
    administered_by: UUID
    dose: str
    unit: str
    route: MedicationRouteOfAdmin
    administered_at: datetime
    site: Optional[str] = None
    response: Optional[str] = None
    notes: Optional[str] = None
    lot_number: Optional[str] = None
    expiration_date: Optional[datetime] = None
    created_at: datetime


class MedicationProtocolRuleContract(BaseModel):
    id: UUID
    tenant_id: UUID
    medication_id: UUID
    protocol_name: str
    indication: str
    min_dose: Optional[str] = None
    max_dose: Optional[str] = None
    allowed_routes: list[MedicationRouteOfAdmin] = Field(default_factory=list)
    contraindications: list[str] = Field(default_factory=list)
    requires_medical_control: bool = False
    age_restriction_min: Optional[int] = None
    age_restriction_max: Optional[int] = None
    weight_based: bool = False
    is_active: bool = True


class DoseSafetyCheckRequest(BaseModel):
    medication_id: UUID
    patient_id: Optional[UUID] = None
    dose: str
    unit: str
    route: MedicationRouteOfAdmin
    patient_weight_kg: Optional[float] = None
    patient_age_years: Optional[int] = None


class DoseSafetyCheckResponse(BaseModel):
    status: DoseSafetyStatus
    warnings: list[str] = Field(default_factory=list)
    max_dose_exceeded: bool = False
    contraindications_found: list[str] = Field(default_factory=list)
    requires_medical_control: bool = False


class MedicationExpirationAlertContract(BaseModel):
    id: UUID
    tenant_id: UUID
    medication_id: UUID
    lot_number: str
    expiration_date: datetime
    days_until_expiration: int
    location: Optional[str] = None
    unit_id: Optional[UUID] = None


class UnitMedicationReadinessContract(BaseModel):
    tenant_id: UUID
    unit_id: UUID
    total_medications: int
    expired_count: int
    expiring_soon_count: int
    missing_count: int
    readiness_percentage: float
    snapshot_at: datetime


class MedicationAdministeredEvent(BaseModel):
    administration_id: UUID
    tenant_id: UUID
    medication_id: UUID
    patient_id: Optional[UUID] = None
    administered_by: UUID
    administered_at: datetime


class MedicationExpirationWarningEvent(BaseModel):
    tenant_id: UUID
    medication_id: UUID
    lot_number: str
    expiration_date: datetime
    days_until_expiration: int
