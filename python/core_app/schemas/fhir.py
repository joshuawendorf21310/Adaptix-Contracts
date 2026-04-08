"""
FHIR Pydantic Schemas for Adaptix

Defines request/response models for FHIR API endpoints.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FhirExportRequest(BaseModel):
    """Request to export entity as FHIR resource"""

    entity_type: str = Field(pattern=r"^(patient|incident|call|fire_report)$")
    entity_id: str


class FhirExportResponse(BaseModel):
    """Response from FHIR export operation"""

    artifact_id: str
    resource_type: str
    resource: dict[str, Any]


class FHIRResourceResponse(BaseModel):
    """Generic FHIR resource response"""

    model_config = ConfigDict(extra="allow")

    resourceType: str
    id: str | None = None
    meta: dict[str, Any] | None = None


class FHIRPatientCreateRequest(BaseModel):
    """Request to create patient from FHIR resource"""

    resource: dict[str, Any] = Field(..., description="FHIR Patient resource")
    incident_id: str = Field(..., description="Incident ID to associate with")


class FHIRBundleRequest(BaseModel):
    """Request containing FHIR Bundle"""

    bundle: dict[str, Any] = Field(..., description="FHIR Bundle resource")


class BundleProcessResponse(BaseModel):
    """Response from bundle processing"""

    processed_resources: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)


class CapabilityStatementResponse(BaseModel):
    """FHIR CapabilityStatement response"""

    model_config = ConfigDict(extra="allow")

    resourceType: str = Field(default="CapabilityStatement")
    status: str
    date: str
    kind: str
    fhirVersion: str
    format: list[str]


class ObservationQueryParams(BaseModel):
    """Query parameters for Observation search"""

    patient: str | None = Field(None, description="Patient reference")
    encounter: str | None = Field(None, description="Encounter reference")
    category: str | None = Field(None, description="Observation category")
    code: str | None = Field(None, description="LOINC code")
    date: str | None = Field(None, description="Date filter")
    count: int = Field(50, description="Maximum results", le=100, alias="_count")


class DestinationNotificationRequest(BaseModel):
    """Request to send destination notification"""

    facility_id: str = Field(..., description="Destination facility identifier")
    eta_minutes: int | None = Field(None, description="Estimated time of arrival in minutes")


class HandoffBundleResponse(BaseModel):
    """Response containing patient handoff bundle"""

    model_config = ConfigDict(extra="allow")

    resourceType: str = Field(default="Bundle")
    type: str = Field(default="collection")
    identifier: dict[str, Any] | None = None
    entry: list[dict[str, Any]] = Field(default_factory=list)


class ValidationResponse(BaseModel):
    """Response from resource validation"""

    valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
