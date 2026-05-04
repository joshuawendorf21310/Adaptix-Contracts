"""CAD-to-ePCR NEMSIS handoff contract.

This contract defines the structured payload that CAD produces and ePCR consumes
to populate NEMSIS 3.5.1 dispatch, response, scene, destination, unit, crew,
and timeline elements.

CAD DOES NOT:
- Generate final NEMSIS XML
- Own NEMSIS validation
- Bypass ePCR chart review
- Invent clinical fields

ePCR OWNS:
- Final NEMSIS 3.5.1 mapping
- XML generation
- XSD validation
- Schematron validation
- Clinical chart review
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CadCrewMemberContext(BaseModel):
    """Crew member context from CAD dispatch."""

    crew_id: str
    role: Optional[str] = None
    certification_level: Optional[str] = None
    unit_id: Optional[str] = None


class CadFacilityContext(BaseModel):
    """Facility context captured at CAD intake."""

    facility_name: Optional[str] = None
    facility_address: Optional[str] = None
    facility_department: Optional[str] = None
    facility_room_bed: Optional[str] = None
    facility_phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CadPatientMinimumContext(BaseModel):
    """Minimum patient identifiers available at CAD intake.

    CAD does NOT own clinical patient data.
    These are dispatch-origin identifiers only.
    """

    patient_first_name: Optional[str] = None
    patient_last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    patient_id_external: Optional[str] = None
    mrn: Optional[str] = None


class CadPayerDocumentAwareness(BaseModel):
    """Payer and document dependency awareness from CAD intake.

    CAD does NOT own billing or document workflow.
    This is awareness only — ePCR/TransportLink own the actual documents.
    """

    payer_type: Optional[str] = None
    payer_name: Optional[str] = None
    authorization_number: Optional[str] = None
    pcs_likely_required: bool = False
    abn_awareness: bool = False
    aob_awareness: bool = False
    document_dependency_notes: Optional[str] = None


class CadDispatchTimeline(BaseModel):
    """Dispatch timeline timestamps from CAD.

    Maps to NEMSIS eTimes section elements.
    All timestamps are ISO 8601 UTC.
    """

    # NEMSIS eTimes.01 — PSAP Call Date/Time (if available)
    call_received_at: Optional[datetime] = None

    # NEMSIS eTimes.03 — Unit Notified by Dispatch Date/Time
    unit_notified_at: Optional[datetime] = None

    # NEMSIS eTimes.05 — Unit En Route Date/Time
    unit_enroute_at: Optional[datetime] = None

    # NEMSIS eTimes.06 — Unit Arrived on Scene Date/Time
    unit_arrived_origin_at: Optional[datetime] = None

    # NEMSIS eTimes.07 — Arrived at Patient Date/Time
    patient_contact_at: Optional[datetime] = None

    # NEMSIS eTimes.09 — Unit Left Scene Date/Time (loaded/transport begin)
    unit_loaded_at: Optional[datetime] = None
    transport_begin_at: Optional[datetime] = None

    # NEMSIS eTimes.11 — Patient Arrived at Destination Date/Time
    arrived_destination_at: Optional[datetime] = None

    # NEMSIS eTimes.12 — Destination Patient Transfer of Care Date/Time
    transfer_of_care_at: Optional[datetime] = None

    # NEMSIS eTimes.13 — Unit Back in Service Date/Time
    unit_clear_at: Optional[datetime] = None

    # CAD internal timestamps
    dispatch_created_at: Optional[datetime] = None
    dispatch_updated_at: Optional[datetime] = None
    unit_assigned_at: Optional[datetime] = None

    # Cancellation
    cancelled_at: Optional[datetime] = None
    cancellation_reason: Optional[str] = None


class CadNemsisHandoffPayload(BaseModel):
    """Structured CAD-to-ePCR handoff payload for NEMSIS 3.5.1 field population.

    This is the authoritative contract between CAD and ePCR for dispatch-origin
    data. ePCR ingests this payload to pre-populate NEMSIS fields where applicable.

    ePCR must:
    - Preserve CAD source attribution
    - Not overwrite clinician-entered data without explicit review
    - Map timestamps to correct NEMSIS eTimes elements
    - Mark missing required NEMSIS elements clearly
    - Return validation warnings to ePCR UI
    - Store handoff mapping audit
    """

    # Correlation identifiers
    handoff_id: str = Field(description="Unique handoff record ID")
    cad_dispatch_id: str = Field(description="CAD dispatch/case ID")
    cad_intake_id: Optional[str] = Field(default=None, description="CAD intake ID if separate")
    tenant_id: str
    correlation_id: Optional[str] = None

    # HEMS context (if applicable)
    hems_request_id: Optional[str] = None
    hems_eligibility_summary: Optional[str] = None
    ground_fallback_recommended: bool = False
    ground_fallback_reason: Optional[str] = None

    # Transport metadata
    # NEMSIS eResponse.05 — Type of Service Requested
    transport_type: str = Field(description="SCHEDULED|UNSCHEDULED|INTERFACILITY|HEMS|etc.")

    # NEMSIS eResponse.07 — Primary Role of the Unit
    level_of_care: str = Field(description="BLS|ALS|CCT|SCT|HEMS|WHEELCHAIR|STRETCHER|UNKNOWN")

    # NEMSIS eResponse.23 — Response Priority
    priority: Optional[str] = None

    # Unit and vehicle
    # NEMSIS eResponse.13 — EMS Unit Number
    unit_id: Optional[str] = None
    vehicle_id: Optional[str] = None

    # NEMSIS eCrew section
    crew_members: List[CadCrewMemberContext] = Field(default_factory=list)

    # Origin/scene facility
    # NEMSIS eScene section
    origin_facility: CadFacilityContext = Field(default_factory=CadFacilityContext)

    # Destination facility
    # NEMSIS eDisposition section
    destination_facility: CadFacilityContext = Field(default_factory=CadFacilityContext)

    # Routing/mileage
    # NEMSIS eDisposition.17 — Transport Distance
    mileage_estimate: Optional[float] = None
    route_eta_minutes: Optional[float] = None

    # Patient minimum context (dispatch-origin only)
    patient_context: Optional[CadPatientMinimumContext] = None

    # Payer/document awareness
    payer_document_awareness: Optional[CadPayerDocumentAwareness] = None

    # Medical necessity support text (CAD-generated, not clinical)
    medical_necessity_support_text: Optional[str] = None

    # Dispatch timeline
    timeline: CadDispatchTimeline = Field(default_factory=CadDispatchTimeline)

    # Notes and briefings
    cad_notes: Optional[str] = None
    crew_briefing: Optional[str] = None
    facility_handoff_notes: Optional[str] = None

    # Audit
    handoff_created_at: datetime
    handoff_source: str = "adaptix-cad"
    handoff_version: str = "1.0"

    class Config:
        json_schema_extra = {
            "example": {
                "handoff_id": "hndff-001",
                "cad_dispatch_id": "disp-001",
                "tenant_id": "tenant-001",
                "transport_type": "INTERFACILITY",
                "level_of_care": "ALS",
                "priority": "high",
                "unit_id": "UNIT-12",
                "vehicle_id": "VEH-12",
                "crew_members": [
                    {"crew_id": "crew-001", "role": "PARAMEDIC", "certification_level": "ALS"}
                ],
                "handoff_created_at": "2026-05-03T12:00:00Z",
            }
        }


class CadNemsisHandoffCreatedEvent(BaseModel):
    """Event emitted when CAD creates a NEMSIS handoff payload."""

    event_type: str = "cad.medical_transport.nemsis_handoff.generated"
    handoff_id: str
    cad_dispatch_id: str
    tenant_id: str
    transport_type: str
    level_of_care: str
    emitted_at: datetime
