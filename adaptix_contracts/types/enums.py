"""
Adaptix Contracts — Domain Enum Types v0.1.0

All shared enum/choice types extracted from the Adaptix monorepo models.
These are pure Python enums with no SQLAlchemy or other runtime dependencies.
Single source of truth for all domain enum values.
"""
from __future__ import annotations

import enum


# ─── CrewLink ───────────────────────────────────────────────────────────

class CrewStatus(str, enum.Enum):
    AVAILABLE = "available"
    ON_DUTY = "on_duty"
    OFF_DUTY = "off_duty"
    ON_CALL = "on_call"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"


class CrewAvailabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ON_CALL = "on_call"


class AvailabilityType(str, enum.Enum):
    SHIFT = "shift"
    CALLBACK = "callback"
    PTO = "pto"
    ON_LEAVE = "on_leave"
    ON_DUTY = "on_duty"
    ON_CALL = "on_call"


class AlertPriority(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    CREATED = "created"
    SENT = "sent"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    ESCALATED = "escalated"
    EXPIRED = "expired"


PageStatus = AlertStatus  # backward-compat alias


class AssignmentType(str, enum.Enum):
    DISPATCH = "dispatch"
    MUTUAL_AID = "mutual_aid"
    STANDBY = "standby"


class AssignmentStatus(str, enum.Enum):
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    AT_HOSPITAL = "at_hospital"
    AVAILABLE = "available"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class AssignmentAckStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    UNAVAILABLE = "unavailable"


class PageType(str, enum.Enum):
    ASSIGNMENT = "assignment"
    SHIFT_FILL = "shift_fill"
    BILLING_FOLLOWUP = "billing_followup"
    BROADCAST = "broadcast"
    CALLBACK = "callback"
    SUPERVISOR_ESCALATION = "supervisor_escalation"


class UrgencyLevel(str, enum.Enum):
    ROUTINE = "routine"
    URGENT = "urgent"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class DeliveryMethod(str, enum.Enum):
    SMS = "sms"
    PUSH = "push"
    VOICE = "voice"
    EMAIL = "email"


class DeliveryStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    ACKNOWLEDGED = "acknowledged"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    FAILED = "failed"


# ─── CAD ────────────────────────────────────────────────────────────────

class CallType(str, enum.Enum):
    MEDICAL = "medical"
    FIRE = "fire"
    TRAUMA = "trauma"
    CARDIAC = "cardiac"
    RESPIRATORY = "respiratory"
    MVC = "mvc"
    PSYCHIATRIC = "psychiatric"
    TRANSFER = "transfer"
    OTHER = "other"


class DispatchPriority(str, enum.Enum):
    ECHO = "echo"
    DELTA = "delta"
    CHARLIE = "charlie"
    BRAVO = "bravo"
    ALPHA = "alpha"
    OMEGA = "omega"  # Non-urgent


class CadSyncStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class CadUnitStatus(str, enum.Enum):
    AVAILABLE = "available"
    ASSIGNED = "assigned"
    OUT_OF_SERVICE = "out_of_service"


class CadSystemType(str, enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    ZOLL = "zoll"
    TYLER = "tyler"
    CENTRAL_SQUARE = "central_square"
    HEXAGON = "hexagon"
    MOTOROLA = "motorola"
    CUSTOM_API = "custom_api"


# ─── Incident ───────────────────────────────────────────────────────────

class IncidentStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DISPATCHED = "dispatched"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    TRANSPORTING = "transporting"
    AT_HOSPITAL = "at_hospital"
    READY_FOR_REVIEW = "ready_for_review"
    COMPLETED = "completed"
    LOCKED = "locked"
    CLEARED = "cleared"
    CANCELLED = "cancelled"


class IncidentPriority(str, enum.Enum):
    ALPHA = "alpha"
    BRAVO = "bravo"
    CHARLIE = "charlie"
    DELTA = "delta"
    ECHO = "echo"


# ─── Narcotics ──────────────────────────────────────────────────────────

class VaultType(enum.StrEnum):
    STATION_VAULT = "station_vault"
    AMBULANCE_KIT = "ambulance_kit"
    EMERGENCY_KIT = "emergency_kit"
    DISPOSAL_VAULT = "disposal_vault"


class VaultStatus(enum.StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"


class DEASchedule(enum.StrEnum):
    SCHEDULE_II = "schedule_ii"
    SCHEDULE_III = "schedule_iii"
    SCHEDULE_IV = "schedule_iv"
    SCHEDULE_V = "schedule_v"


class MedicationStatus(enum.StrEnum):
    AVAILABLE = "available"
    ISSUED = "issued"
    ADMINISTERED = "administered"
    WASTED = "wasted"
    EXPIRED = "expired"
    QUARANTINED = "quarantined"


class NarcoticTransactionType(enum.StrEnum):
    """Narcotic-specific transaction type (distinct from InventoryTransactionType)."""
    ISSUE = "issue"
    RETURN = "return"
    ADMINISTRATION = "administration"
    WASTE = "waste"
    AUDIT_ADJUSTMENT = "audit_adjustment"
    TRANSFER = "transfer"
    DISPOSAL = "disposal"


class AccessType(enum.StrEnum):
    AUTHORIZED_ACCESS = "authorized_access"
    AUDIT = "audit"
    MAINTENANCE = "maintenance"
    EMERGENCY_OVERRIDE = "emergency_override"


class InvestigationStatus(enum.StrEnum):
    PENDING = "pending"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


# ─── Fire ────────────────────────────────────────────────────────────────

class FireIncidentType(str, enum.Enum):
    STRUCTURE_FIRE = "structure_fire"
    VEHICLE_FIRE = "vehicle_fire"
    WILDLAND_FIRE = "wildland_fire"
    HAZMAT = "hazmat"
    RESCUE = "rescue"
    MEDICAL_ASSIST = "medical_assist"
    SERVICE_CALL = "service_call"
    FALSE_ALARM = "false_alarm"
    OTHER = "other"


class FireIncidentStatus(str, enum.Enum):
    DISPATCH = "dispatch"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    CONTROLLED = "controlled"
    CLEARED = "cleared"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


def allowed_fire_transition_targets(status: FireIncidentStatus) -> set:
    """Valid next states for a given fire incident status."""
    _TRANSITIONS: dict[FireIncidentStatus, set] = {
        FireIncidentStatus.DISPATCH: {FireIncidentStatus.EN_ROUTE, FireIncidentStatus.CANCELLED},
        FireIncidentStatus.EN_ROUTE: {FireIncidentStatus.ON_SCENE, FireIncidentStatus.CANCELLED},
        FireIncidentStatus.ON_SCENE: {FireIncidentStatus.CONTROLLED, FireIncidentStatus.CANCELLED},
        FireIncidentStatus.CONTROLLED: {FireIncidentStatus.CLEARED, FireIncidentStatus.COMPLETED},
        FireIncidentStatus.CLEARED: set(),
        FireIncidentStatus.COMPLETED: set(),
        FireIncidentStatus.CANCELLED: set(),
    }
    return _TRANSITIONS.get(status, set())


class ApparatusType(str, enum.Enum):
    ENGINE = "engine"
    LADDER = "ladder"
    RESCUE = "rescue"
    HAZMAT = "hazmat"
    BATTALION = "battalion"
    MEDIC = "medic"
    BRUSH = "brush"
    BOAT = "boat"
    TANKER = "tanker"
    OTHER = "other"


class ApparatusStatus(str, enum.Enum):
    AVAILABLE = "available"
    DISPATCHED = "dispatched"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    OUT_OF_SERVICE = "out_of_service"
    STAFFED = "staffed"
    UNSTAFFED = "unstaffed"


class MutualAidType(str, enum.Enum):
    """Mutual aid classification (defined in contracts — fixes pre-existing monorepo gap)."""
    NONE = "none"
    GIVEN = "given"
    RECEIVED = "received"
    AUTOMATIC = "automatic"
    REQUESTED = "requested"


class InspectionStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    VIOLATIONS_FOUND = "violations_found"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TrainingType(str, enum.Enum):
    DRILL = "drill"
    LIVE_BURN = "live_burn"
    CLASSROOM = "classroom"
    CERTIFICATION = "certification"
    FIREFIGHTER_I = "firefighter_i"
    FIREFIGHTER_II = "firefighter_ii"
    HAZMAT = "hazmat"
    VEHICLE_EXTRICATION = "vehicle_extrication"
    OTHER = "other"


# ─── MDT ────────────────────────────────────────────────────────────────

class UnitStatusCode(str, enum.Enum):
    ACTIVE = "active"
    LOGGED_OUT = "logged_out"
    AVAILABLE = "available"
    DISPATCHED = "dispatched"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    TRANSPORTING = "transporting"
    AT_HOSPITAL = "at_hospital"
    RETURNING = "returning"
    OUT_OF_SERVICE = "out_of_service"
    STAGED = "staged"


AvailabilityStatus = UnitStatusCode  # alias
MdtStatus = UnitStatusCode  # alias


class MessagePriority(str, enum.Enum):
    LOW = "low"
    ROUTINE = "routine"
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"
    HIGH = "high"
    CRITICAL = "critical"


class NoteType(str, enum.Enum):
    GENERAL = "general"
    CLINICAL = "clinical"
    SAFETY = "safety"
    SCENE_NOTE = "scene_note"


class ResourceRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DISPATCHED = "dispatched"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


# ─── Inventory ───────────────────────────────────────────────────────────

class ItemCategory(enum.StrEnum):
    MEDICAL_SUPPLY = "medical_supply"
    MEDICATION = "medication"
    EQUIPMENT = "equipment"
    VEHICLE_PART = "vehicle_part"
    SAFETY_GEAR = "safety_gear"
    OFFICE_SUPPLY = "office_supply"
    CONSUMABLE = "consumable"


class ItemStatus(enum.StrEnum):
    ACTIVE = "active"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"
    ON_ORDER = "on_order"


class LocationType(enum.StrEnum):
    STATION = "station"
    VEHICLE = "vehicle"
    WAREHOUSE = "warehouse"
    SUPPLY_ROOM = "supply_room"
    KIT = "kit"


class InventoryTransactionType(enum.StrEnum):
    """Inventory-specific transaction type (distinct from NarcoticTransactionType)."""
    PURCHASE = "purchase"
    USAGE = "usage"
    TRANSFER = "transfer"
    RESTOCK = "restock"
    ADJUSTMENT = "adjustment"
    EXPIRATION = "expiration"
    DISPOSAL = "disposal"


class AssetStatus(enum.StrEnum):
    ACTIVE = "active"
    IN_MAINTENANCE = "in_maintenance"
    OUT_OF_SERVICE = "out_of_service"
    RETIRED = "retired"


class MaintenanceType(enum.StrEnum):
    PREVENTIVE = "preventive"
    CORRECTIVE = "corrective"
    INSPECTION = "inspection"
    CALIBRATION = "calibration"
    REPAIR = "repair"


class PurchaseOrderStatus(enum.StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    PARTIAL = "partial"
    RECEIVED = "received"
    CANCELLED = "cancelled"


class CycleCountStatus(enum.StrEnum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"


# ─── TransportLink ───────────────────────────────────────────────────────

class TransportStatus(enum.StrEnum):
    REQUESTED = "requested"
    SCHEDULED = "scheduled"
    CAD_QUEUED = "cad_queued"
    DISPATCHED = "dispatched"
    EN_ROUTE = "en_route"
    PATIENT_CONTACT = "patient_contact"
    TRANSPORTING = "transporting"
    ARRIVED = "arrived"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TransportType(enum.StrEnum):
    EMERGENT = "emergent"
    URGENT = "urgent"
    SCHEDULED = "scheduled"
    RECURRING = "recurring"


class FacilityType(enum.StrEnum):
    HOSPITAL = "hospital"
    NURSING_HOME = "nursing_home"
    DIALYSIS_CENTER = "dialysis_center"
    REHAB_FACILITY = "rehab_facility"
    ASSISTED_LIVING = "assisted_living"
    PRIVATE_RESIDENCE = "private_residence"
    CLINIC = "clinic"
    OTHER = "other"


class PCSABNStatus(enum.StrEnum):
    NOT_REQUIRED = "not_required"
    REQUIRED_PENDING = "required_pending"
    ON_FILE = "on_file"
    ABN_SIGNED = "abn_signed"
    MISSING = "missing"


ALLOWED_TRANSPORT_TRANSITIONS: dict = {
    TransportStatus.REQUESTED: {TransportStatus.SCHEDULED, TransportStatus.CANCELLED},
    TransportStatus.SCHEDULED: {
        TransportStatus.CAD_QUEUED,
        TransportStatus.DISPATCHED,
        TransportStatus.CANCELLED,
    },
    TransportStatus.CAD_QUEUED: {TransportStatus.DISPATCHED, TransportStatus.CANCELLED},
    TransportStatus.DISPATCHED: {TransportStatus.EN_ROUTE, TransportStatus.CANCELLED},
    TransportStatus.EN_ROUTE: {
        TransportStatus.PATIENT_CONTACT,
        TransportStatus.CANCELLED,
    },
    TransportStatus.PATIENT_CONTACT: {
        TransportStatus.TRANSPORTING,
        TransportStatus.CANCELLED,
    },
    TransportStatus.TRANSPORTING: {TransportStatus.ARRIVED, TransportStatus.CANCELLED},
    TransportStatus.ARRIVED: {TransportStatus.COMPLETED, TransportStatus.CANCELLED},
    TransportStatus.COMPLETED: set(),  # Terminal state
    TransportStatus.CANCELLED: set(),  # Terminal state
}


def allowed_transport_transition_targets(from_status: "TransportStatus") -> set:
    """Get allowed transition targets for a given transport status."""
    return ALLOWED_TRANSPORT_TRANSITIONS.get(from_status, set())


# ─── Patient ─────────────────────────────────────────────────────────────

class PatientGender(enum.StrEnum):
    FEMALE = "female"
    MALE = "male"
    NON_BINARY = "non_binary"
    OTHER = "other"
    UNKNOWN = "unknown"


# ─── Patient Financial ───────────────────────────────────────────────────

class _ValueEnum(str, enum.Enum):
    """Base enum with explicit str — mirrors monorepo _ValueEnum mixin."""
    def __str__(self) -> str:
        return str(self.value)


class PatientAccountStatus(_ValueEnum):
    ACTIVE = "active"
    COLLECTIONS = "collections"
    SUSPENDED = "suspended"
    CLOSED = "closed"
    WRITE_OFF = "write_off"


class PaymentPlanFrequency(_ValueEnum):
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"


class PaymentPlanStatus(_ValueEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFAULTED = "defaulted"
    CANCELLED = "cancelled"


class PatientPaymentStatus(_ValueEnum):
    PENDING = "pending"
    POSTED = "posted"
    FAILED = "failed"
    REFUNDED = "refunded"


class PatientDisputeStatus(_ValueEnum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    RESOLVED_PATIENT_FAVOR = "resolved_patient_favor"
    RESOLVED_AGENCY_FAVOR = "resolved_agency_favor"
    WITHDRAWN = "withdrawn"
