from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from core_app.models.cad import CadSyncStatus, CadSystemType, CadUnitStatus


# CAD System Schemas
class CadSystemCreate(BaseModel):
    system_name: str = Field(..., min_length=1, max_length=255)
    system_type: CadSystemType
    api_endpoint: str | None = None
    api_key: str | None = None
    active: bool = True
    sync_enabled: bool = True
    adapter_config: dict[str, Any] = Field(default_factory=dict)


class CadSystemUpdate(BaseModel):
    system_name: str | None = Field(None, min_length=1, max_length=255)
    api_endpoint: str | None = None
    api_key: str | None = None
    active: bool | None = None
    sync_enabled: bool | None = None
    adapter_config: dict[str, Any] | None = None


class CadSystemResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    system_name: str
    system_type: CadSystemType
    api_endpoint: str | None
    active: bool
    sync_enabled: bool
    adapter_config_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CadSystemListResponse(BaseModel):
    items: list[CadSystemResponse]
    total: int


# CAD Incident Schemas
class CadIncidentCreate(BaseModel):
    cad_system_id: UUID
    external_incident_id: str
    incident_number: str
    call_type: str | None = None
    priority: str | None = None
    location: str | None = None
    coordinates: dict[str, Any] | None = None
    units_assigned: list[str] = Field(default_factory=list)
    status: str = "pending"
    timestamps_json: dict[str, Any] = Field(default_factory=dict)


class CadIncidentUpdate(BaseModel):
    call_type: str | None = None
    priority: str | None = None
    location: str | None = None
    coordinates: dict[str, Any] | None = None
    units_assigned: list[str] | None = None
    status: str | None = None
    timestamps_json: dict[str, Any] | None = None
    sync_status: CadSyncStatus | None = None
    version: int


class CadIncidentResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    cad_system_id: UUID
    external_incident_id: str
    incident_number: str
    call_type: str | None
    priority: str | None
    location: str | None
    coordinates: dict[str, Any] | None
    units_assigned: list[str]
    status: str
    timestamps_json: dict[str, Any]
    sync_status: CadSyncStatus
    last_sync_at: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CadIncidentListResponse(BaseModel):
    items: list[CadIncidentResponse]
    total: int


# CAD Unit Schemas
class CadUnitCreate(BaseModel):
    cad_system_id: UUID
    external_unit_id: str
    unit_name: str
    unit_type: str | None = None
    status: CadUnitStatus = CadUnitStatus.AVAILABLE
    current_location: dict[str, Any] | None = None
    personnel_assigned: list[dict[str, Any]] = Field(default_factory=list)


class CadUnitUpdate(BaseModel):
    unit_name: str | None = None
    unit_type: str | None = None
    status: CadUnitStatus | None = None
    current_location: dict[str, Any] | None = None
    personnel_assigned: list[dict[str, Any]] | None = None


class CadUnitResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    cad_system_id: UUID
    external_unit_id: str
    unit_name: str
    unit_type: str | None
    status: CadUnitStatus
    current_location: dict[str, Any] | None
    personnel_assigned: list[dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CadUnitListResponse(BaseModel):
    items: list[CadUnitResponse]
    total: int


class CadUnitStatusUpdate(BaseModel):
    status: CadUnitStatus
    location: dict[str, Any] | None = None


# CAD Event Schemas
class CadEventCreate(BaseModel):
    cad_incident_id: UUID
    event_type: str
    event_time: datetime
    details_json: dict[str, Any] = Field(default_factory=dict)


class CadEventResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    cad_incident_id: UUID
    event_type: str
    event_time: datetime
    details_json: dict[str, Any]
    sync_status: CadSyncStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CadEventListResponse(BaseModel):
    items: list[CadEventResponse]
    total: int


# CAD Sync Log Schemas
class CadSyncLogResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    cad_system_id: UUID
    sync_type: str
    direction: str
    status: CadSyncStatus
    records_processed: int
    error_message: str | None
    sync_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CadSyncLogListResponse(BaseModel):
    items: list[CadSyncLogResponse]
    total: int


# Webhook and Sync Schemas
class CadWebhookPayload(BaseModel):
    event_type: str
    timestamp: datetime | None = None
    data: dict[str, Any]


class CadSyncRequest(BaseModel):
    since: str | None = None
    limit: int = Field(default=100, ge=1, le=1000)


class CadSyncResponse(BaseModel):
    success: bool
    sync_log_id: UUID
    records_processed: int
    error_message: str | None = None


class CadPushIncidentRequest(BaseModel):
    incident_number: str
    call_type: str | None = None
    priority: str | None = None
    location: str | None = None
    coordinates: dict[str, Any] | None = None
    units_assigned: list[str] = Field(default_factory=list)


class CadPushIncidentResponse(BaseModel):
    success: bool
    external_incident_id: str
    error_message: str | None = None
