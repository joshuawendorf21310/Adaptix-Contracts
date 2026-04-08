"""Fire Core Module (Module 1) - Base Schemas for Fire RMS

This module provides core Pydantic schemas for the Fire Records Management System.
Includes base fire incident models, status management, and common data structures.

Module 1: Core Fire Incident Management
- Fire incident creation and lifecycle
- Status transitions and state machine validation
- Location and timing information
- Basic incident classification
"""

import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator

from core_app.models.fire import (
    FireIncidentStatus,
    FireIncidentType,
    IncidentPriority,
    MutualAidType,
    allowed_fire_transition_targets,
)

# ============================================================================
# COMMON DATA STRUCTURES
# ============================================================================


class CoordinatesSchema(BaseModel):
    """Geographic coordinates with optional accuracy"""

    lat: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude in decimal degrees",
        examples=[42.1015],
    )
    lng: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude in decimal degrees",
        examples=[-72.5898],
    )
    accuracy: float | None = Field(
        None,
        ge=0.0,
        description="Accuracy in meters",
        examples=[10.0],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lat": 42.1015,
                "lng": -72.5898,
                "accuracy": 10.0,
            }
        }
    )


class CasualtyCountSchema(BaseModel):
    """Casualty counts for civilians and firefighters"""

    civilian: int = Field(
        default=0,
        ge=0,
        description="Number of civilian casualties",
        examples=[0],
    )
    firefighter: int = Field(
        default=0,
        ge=0,
        description="Number of firefighter casualties",
        examples=[0],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "civilian": 0,
                "firefighter": 0,
            }
        }
    )


# ============================================================================
# FIRE INCIDENT REQUESTS
# ============================================================================


class FireIncidentCreateRequest(BaseModel):
    """Request to create a new fire incident

    Creates a new fire incident record with initial dispatch information.
    All required NFIRS/NERIS-compliant fields should be provided.
    """

    incident_number: Annotated[
        str,
        Field(
            min_length=1,
            max_length=64,
            description="Unique incident number (e.g., F26-0001)",
            examples=["F26-0001"],
        ),
    ]

    incident_type: Annotated[
        FireIncidentType,
        Field(
            description="Type of fire incident",
            examples=["structure_fire"],
        ),
    ] = FireIncidentType.OTHER

    status: Annotated[
        FireIncidentStatus,
        Field(
            description="Initial incident status",
            examples=["dispatch"],
        ),
    ] = FireIncidentStatus.DISPATCH

    priority: Annotated[
        IncidentPriority | None,
        Field(
            None,
            description="Incident priority level",
            examples=["high"],
        ),
    ]

    alarm_level: Annotated[
        int | None,
        Field(
            None,
            ge=1,
            le=10,
            description="Alarm level (1-10)",
            examples=[2],
        ),
    ]

    mutual_aid: Annotated[
        MutualAidType,
        Field(
            description="Mutual aid status",
            examples=["none"],
        ),
    ] = MutualAidType.NONE

    # Timestamps
    dispatch_time: Annotated[
        datetime | None,
        Field(
            None,
            description="Dispatch timestamp",
            examples=["2026-03-25T14:30:00Z"],
        ),
    ]

    arrival_time: Annotated[
        datetime | None,
        Field(
            None,
            description="First unit arrival timestamp",
            examples=["2026-03-25T14:38:00Z"],
        ),
    ]

    controlled_time: Annotated[
        datetime | None,
        Field(
            None,
            description="Fire under control timestamp",
            examples=["2026-03-25T15:45:00Z"],
        ),
    ]

    cleared_time: Annotated[
        datetime | None,
        Field(
            None,
            description="Scene cleared timestamp",
            examples=["2026-03-25T16:30:00Z"],
        ),
    ]

    # Location
    address: Annotated[
        str | None,
        Field(
            None,
            max_length=500,
            description="Incident street address",
            examples=["123 Main St, Springfield, MA 01101"],
        ),
    ]

    coordinates: Annotated[
        CoordinatesSchema | None,
        Field(
            None,
            description="GPS coordinates of incident",
        ),
    ]

    # Basic fire information
    exposures: Annotated[
        int | None,
        Field(
            None,
            ge=0,
            description="Number of exposure properties at risk",
            examples=[2],
        ),
    ]

    property_use: Annotated[
        str | None,
        Field(
            None,
            max_length=128,
            description="NFIRS property use code",
            examples=["419"],
        ),
    ]

    actions_taken: Annotated[
        list[str] | None,
        Field(
            None,
            description="List of NFIRS action taken codes",
            examples=[["10", "31", "43"]],
        ),
    ]

    fire_spread: Annotated[
        str | None,
        Field(
            None,
            max_length=64,
            description="Fire spread classification",
            examples=["room_of_origin"],
        ),
    ]

    estimated_loss: Annotated[
        float | None,
        Field(
            None,
            ge=0.0,
            description="Estimated property loss in dollars",
            examples=[75000.00],
        ),
    ]

    casualties: Annotated[
        CasualtyCountSchema | None,
        Field(
            None,
            description="Casualty counts",
        ),
    ]

    # Notes
    notes: Annotated[
        str | None,
        Field(
            None,
            description="Additional incident notes",
            examples=["Large commercial structure fire with multiple engines"],
        ),
    ]

    @field_validator("dispatch_time", "arrival_time", "controlled_time", "cleared_time")
    @classmethod
    def validate_timezone_aware(cls, value: datetime | None) -> datetime | None:
        """Ensure all datetime values are timezone-aware"""
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Datetime values must be timezone-aware (include timezone)")
        return value

    @field_validator("incident_number")
    @classmethod
    def validate_incident_number(cls, value: str) -> str:
        """Validate and normalize incident number"""
        normalized = value.strip()
        if not normalized:
            raise ValueError("Incident number must not be empty")
        return normalized

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "incident_number": "F26-0001",
                "incident_type": "structure_fire",
                "status": "dispatch",
                "priority": "high",
                "alarm_level": 2,
                "mutual_aid": "none",
                "dispatch_time": "2026-03-25T14:30:00Z",
                "arrival_time": "2026-03-25T14:38:00Z",
                "address": "123 Main St, Springfield, MA 01101",
                "coordinates": {"lat": 42.1015, "lng": -72.5898},
                "exposures": 2,
                "property_use": "419",
                "actions_taken": ["10", "31", "43"],
                "fire_spread": "room_of_origin",
                "estimated_loss": 75000.00,
                "casualties": {"civilian": 0, "firefighter": 0},
                "notes": "Large commercial structure fire",
            }
        }
    )


class FireIncidentUpdateRequest(BaseModel):
    """Request to update an existing fire incident

    Updates fire incident details. Uses optimistic locking via version field.
    All fields are optional; only provided fields will be updated.
    """

    version: Annotated[
        int,
        Field(
            ge=1,
            description="Expected version for optimistic locking",
            examples=[1],
        ),
    ]

    incident_type: Annotated[
        FireIncidentType | None,
        Field(
            None,
            description="Type of fire incident",
        ),
    ]

    priority: Annotated[
        IncidentPriority | None,
        Field(
            None,
            description="Incident priority level",
        ),
    ]

    alarm_level: Annotated[
        int | None,
        Field(
            None,
            ge=1,
            le=10,
            description="Alarm level (1-10)",
        ),
    ]

    mutual_aid: Annotated[
        MutualAidType | None,
        Field(
            None,
            description="Mutual aid status",
        ),
    ]

    # Timestamps
    arrival_time: Annotated[
        datetime | None,
        Field(
            None,
            description="First unit arrival timestamp",
        ),
    ]

    controlled_time: Annotated[
        datetime | None,
        Field(
            None,
            description="Fire under control timestamp",
        ),
    ]

    cleared_time: Annotated[
        datetime | None,
        Field(
            None,
            description="Scene cleared timestamp",
        ),
    ]

    # Location
    address: Annotated[
        str | None,
        Field(
            None,
            max_length=500,
            description="Incident street address",
        ),
    ]

    coordinates: Annotated[
        CoordinatesSchema | None,
        Field(
            None,
            description="GPS coordinates of incident",
        ),
    ]

    # Fire information
    exposures: Annotated[
        int | None,
        Field(
            None,
            ge=0,
            description="Number of exposure properties at risk",
        ),
    ]

    property_use: Annotated[
        str | None,
        Field(
            None,
            max_length=128,
            description="NFIRS property use code",
        ),
    ]

    actions_taken: Annotated[
        list[str] | None,
        Field(
            None,
            description="List of NFIRS action taken codes",
        ),
    ]

    fire_spread: Annotated[
        str | None,
        Field(
            None,
            max_length=64,
            description="Fire spread classification",
        ),
    ]

    estimated_loss: Annotated[
        float | None,
        Field(
            None,
            ge=0.0,
            description="Estimated property loss in dollars",
        ),
    ]

    casualties: Annotated[
        CasualtyCountSchema | None,
        Field(
            None,
            description="Casualty counts",
        ),
    ]

    notes: Annotated[
        str | None,
        Field(
            None,
            description="Additional incident notes",
        ),
    ]

    @field_validator("arrival_time", "controlled_time", "cleared_time")
    @classmethod
    def validate_timezone_aware(cls, value: datetime | None) -> datetime | None:
        """Ensure all datetime values are timezone-aware"""
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Datetime values must be timezone-aware (include timezone)")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "version": 1,
                "status": "controlled",
                "controlled_time": "2026-03-25T15:45:00Z",
                "estimated_loss": 85000.00,
                "fire_spread": "floor_of_origin",
            }
        }
    )


class FireIncidentStatusTransitionRequest(BaseModel):
    """Request to transition fire incident status

    Changes incident status with state machine validation.
    Validates that the transition is allowed based on current status.
    """

    version: Annotated[
        int,
        Field(
            ge=1,
            description="Expected version for optimistic locking",
            examples=[2],
        ),
    ]

    target_status: Annotated[
        FireIncidentStatus,
        Field(
            description="Target status to transition to",
            examples=["en_route"],
        ),
    ]

    reason: Annotated[
        str | None,
        Field(
            None,
            max_length=500,
            description="Reason for status change",
            examples=["Units responding to scene"],
        ),
    ]

    timestamp: Annotated[
        datetime | None,
        Field(
            None,
            description="Timestamp of status change (defaults to now)",
            examples=["2026-03-25T14:35:00Z"],
        ),
    ]

    @field_validator("timestamp")
    @classmethod
    def validate_timezone_aware(cls, value: datetime | None) -> datetime | None:
        """Ensure timestamp is timezone-aware"""
        if value is None:
            return value
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("Timestamp must be timezone-aware (include timezone)")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "version": 2,
                "target_status": "en_route",
                "reason": "Engine 1 and Ladder 1 responding",
                "timestamp": "2026-03-25T14:35:00Z",
            }
        }
    )


# ============================================================================
# FIRE INCIDENT RESPONSES
# ============================================================================


class FireIncidentResponse(BaseModel):
    """Complete fire incident response

    Returns full fire incident details including all timestamps,
    resource assignments, and calculated fields.
    """

    model_config = ConfigDict(from_attributes=True)

    # Core identification
    id: uuid.UUID = Field(description="Unique incident identifier")
    tenant_id: uuid.UUID = Field(description="Tenant identifier")
    incident_number: str = Field(description="Human-readable incident number")

    # Classification
    incident_type: FireIncidentType = Field(description="Type of fire incident")
    status: FireIncidentStatus = Field(description="Current incident status")
    priority: IncidentPriority | None = Field(None, description="Priority level")
    alarm_level: int | None = Field(None, description="Alarm level")
    mutual_aid: MutualAidType | None = Field(None, description="Mutual aid status")

    # Timestamps
    dispatch_time: datetime | None = Field(None, description="Dispatch timestamp")
    arrival_time: datetime | None = Field(None, description="Arrival timestamp")
    controlled_time: datetime | None = Field(None, description="Fire controlled timestamp")
    cleared_time: datetime | None = Field(None, description="Scene cleared timestamp")

    # Location
    address: str | None = Field(None, description="Street address")
    coordinates: dict | None = Field(None, description="GPS coordinates")

    # Fire details
    exposures: int | None = Field(None, description="Number of exposures")
    property_use: str | None = Field(None, description="NFIRS property use code")
    actions_taken: list | None = Field(None, description="Actions taken codes")
    fire_spread: str | None = Field(None, description="Fire spread classification")
    estimated_loss: float | None = Field(None, description="Estimated property loss")
    casualties: dict | None = Field(None, description="Casualty counts")

    # Resources
    apparatus_ids: list | None = Field(None, description="Assigned apparatus UUIDs")
    personnel_ids: list | None = Field(None, description="Assigned personnel UUIDs")

    # NERIS
    neris_payload_json: dict | None = Field(None, description="Cached NERIS export payload")

    # Notes
    notes: str | None = Field(None, description="Additional notes")

    # Metadata
    version: int = Field(description="Version for optimistic locking")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    deleted_at: datetime | None = Field(None, description="Soft delete timestamp")

    @computed_field  # type: ignore[misc]
    @property
    def apparatus_count(self) -> int:
        """Number of assigned apparatus"""
        return len(self.apparatus_ids) if self.apparatus_ids else 0

    @computed_field  # type: ignore[misc]
    @property
    def personnel_count(self) -> int:
        """Number of assigned personnel"""
        return len(self.personnel_ids) if self.personnel_ids else 0

    @computed_field  # type: ignore[misc]
    @property
    def response_time_seconds(self) -> int | None:
        """Response time in seconds (dispatch to arrival)"""
        if self.dispatch_time and self.arrival_time:
            return int((self.arrival_time - self.dispatch_time).total_seconds())
        return None

    @computed_field  # type: ignore[misc]
    @property
    def duration_minutes(self) -> int | None:
        """Incident duration in minutes (dispatch to cleared)"""
        if self.dispatch_time and self.cleared_time:
            return int((self.cleared_time - self.dispatch_time).total_seconds() / 60)
        return None

    @computed_field  # type: ignore[misc]
    @property
    def is_active(self) -> bool:
        """Whether incident is currently active"""
        return self.status not in [
            FireIncidentStatus.CLEARED,
            FireIncidentStatus.COMPLETED,
            FireIncidentStatus.CANCELLED,
        ]

    @computed_field  # type: ignore[misc]
    @property
    def allowed_transitions(self) -> list[str]:
        """List of allowed status transitions from current status"""
        allowed = allowed_fire_transition_targets(self.status)
        return [s.value for s in allowed]


class FireIncidentSummaryResponse(BaseModel):
    """Summary fire incident response for list views

    Lighter-weight response for lists, excluding detailed fields.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    incident_number: str
    incident_type: FireIncidentType
    status: FireIncidentStatus
    priority: IncidentPriority | None
    alarm_level: int | None
    dispatch_time: datetime | None
    arrival_time: datetime | None
    controlled_time: datetime | None
    cleared_time: datetime | None
    address: str | None
    estimated_loss: float | None
    version: int
    created_at: datetime
    updated_at: datetime

    @computed_field  # type: ignore[misc]
    @property
    def apparatus_count(self) -> int:
        """Number of assigned apparatus"""
        # Note: This will be computed from the full model if available
        return 0

    @computed_field  # type: ignore[misc]
    @property
    def personnel_count(self) -> int:
        """Number of assigned personnel"""
        return 0


class FireIncidentListResponse(BaseModel):
    """Paginated list of fire incidents"""

    items: list[FireIncidentSummaryResponse] = Field(
        description="List of fire incident summaries"
    )
    total: int = Field(description="Total number of incidents matching filters")
    limit: int = Field(description="Maximum items per page")
    offset: int = Field(description="Offset for pagination")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "tenant_id": "660e8400-e29b-41d4-a716-446655440000",
                        "incident_number": "F26-0001",
                        "incident_type": "structure_fire",
                        "status": "controlled",
                        "priority": "high",
                        "alarm_level": 2,
                        "dispatch_time": "2026-03-25T14:30:00Z",
                        "arrival_time": "2026-03-25T14:38:00Z",
                        "controlled_time": "2026-03-25T15:45:00Z",
                        "address": "123 Main St",
                        "estimated_loss": 75000.00,
                        "version": 3,
                        "created_at": "2026-03-25T14:30:05Z",
                        "updated_at": "2026-03-25T15:45:10Z",
                    }
                ],
                "total": 1,
                "limit": 50,
                "offset": 0,
            }
        }
    )


class FireIncidentStatusResponse(BaseModel):
    """Response after status transition"""

    id: uuid.UUID = Field(description="Incident identifier")
    incident_number: str = Field(description="Incident number")
    previous_status: FireIncidentStatus = Field(description="Previous status")
    current_status: FireIncidentStatus = Field(description="New current status")
    version: int = Field(description="New version number")
    updated_at: datetime = Field(description="Update timestamp")
    allowed_transitions: list[str] = Field(
        description="Allowed next status transitions"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "incident_number": "F26-0001",
                "previous_status": "dispatch",
                "current_status": "en_route",
                "version": 3,
                "updated_at": "2026-03-25T14:35:00Z",
                "allowed_transitions": ["on_scene", "cancelled"],
            }
        }
    )
