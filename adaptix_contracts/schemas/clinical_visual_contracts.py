"""Clinical visual assessment contracts for CPAE, VAS, and ARCOS.

These contracts define the cross-domain, review-safe structures used to capture
structured physical findings, anatomically realistic visual overlays, and AR
assessment interactions. They preserve the authority chain:

- CPAE owns structured physical findings.
- VAS owns governed clinical visualization state.
- ARCOS owns AR session/input context only.
- CareGraph remains the clinical truth graph.
- Vision may suggest but never authoritatively writes chart truth.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class PatientModelVariant(str, Enum):
    """Supported anatomical model variants for visualization and AR alignment."""

    ADULT = "adult"
    PEDIATRIC = "pediatric"
    NEONATAL = "neonatal"


class AnatomicalView(str, Enum):
    """Supported anatomical viewpoints for VAS and ARCOS surfaces."""

    FRONT = "front"
    POSTERIOR = "posterior"
    LEFT_LATERAL = "left_lateral"
    RIGHT_LATERAL = "right_lateral"
    REGIONAL = "regional"


class AnatomicalRegion(str, Enum):
    """Canonical anatomical regions shared across CPAE, VAS, and ARCOS."""

    HEAD = "head"
    FACE = "face"
    NECK = "neck"
    CHEST_ANTERIOR = "chest_anterior"
    CHEST_POSTERIOR = "chest_posterior"
    ABDOMEN = "abdomen"
    PELVIS = "pelvis"
    BACK_SPINE = "back_spine"
    LEFT_UPPER_EXTREMITY = "left_upper_extremity"
    RIGHT_UPPER_EXTREMITY = "right_upper_extremity"
    LEFT_LOWER_EXTREMITY = "left_lower_extremity"
    RIGHT_LOWER_EXTREMITY = "right_lower_extremity"
    GENERALIZED_SKIN = "generalized_skin"
    GENERALIZED_GLOBAL = "generalized_global"


class PhysiologicalSystem(str, Enum):
    """Physiological systems for structured findings and protocol guidance."""

    NEUROLOGICAL = "neurological"
    RESPIRATORY = "respiratory"
    CARDIOVASCULAR = "cardiovascular"
    MUSCULOSKELETAL = "musculoskeletal"
    INTEGUMENTARY = "integumentary"
    GASTROINTESTINAL = "gastrointestinal"
    GENITOURINARY = "genitourinary"
    ENDOCRINE = "endocrine"
    TRAUMA = "trauma"


class ClinicalFindingType(str, Enum):
    """Structured finding classes supported by CPAE-backed visual workflows."""

    INSPECTION = "inspection"
    PALPATION = "palpation"
    AUSCULTATION = "auscultation"
    NEUROLOGICAL_EXAM = "neurological_exam"
    PAIN = "pain"
    INJURY = "injury"
    DEFORMITY = "deformity"
    SWELLING = "swelling"
    BLEEDING = "bleeding"
    BURN = "burn"
    BRUISING = "bruising"
    PULSE = "pulse"
    CAP_REFILL = "cap_refill"
    TENDERNESS = "tenderness"
    RIGIDITY = "rigidity"
    CREPITUS = "crepitus"
    DEVICE_ASSOCIATED = "device_associated"
    PERFUSION = "perfusion"
    RESPIRATORY_EFFORT = "respiratory_effort"
    PUPILLARY = "pupillary"
    FACIAL_ASYMMETRY = "facial_asymmetry"


class VisualOverlayType(str, Enum):
    """Overlay rendering categories for VAS and ARCOS."""

    BRUISING = "bruising"
    SWELLING = "swelling"
    DEFORMITY = "deformity"
    BURN = "burn"
    BLEEDING = "bleeding"
    PERFUSION = "perfusion"
    RESPIRATORY_EFFORT = "respiratory_effort"
    NEURO_ASYMMETRY = "neuro_asymmetry"
    PUPILLARY = "pupillary"
    PAIN_MAP = "pain_map"
    DEVICE_PLACEMENT = "device_placement"
    REASSESSMENT_DELTA = "reassessment_delta"


class FindingSeverity(str, Enum):
    """Severity classification for structured findings and overlays."""

    MINIMAL = "minimal"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


class FindingEvolution(str, Enum):
    """Time-evolution state between reassessments."""

    NEW = "new"
    IMPROVING = "improving"
    WORSENING = "worsening"
    UNCHANGED = "unchanged"
    RESOLVED = "resolved"


class ReviewState(str, Enum):
    """Reviewer disposition for Vision-assisted or AR-assisted outputs."""

    DIRECT_CONFIRMED = "direct_confirmed"
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EDITED_AND_ACCEPTED = "edited_and_accepted"


class DetectionMethod(str, Enum):
    """How a finding was produced or confirmed."""

    DIRECT_VISUAL_OBSERVATION = "direct_visual_observation"
    PALPATION_GUIDED_ENTRY = "palpation_guided_entry"
    TOUCH_BODY_ENTRY = "touch_body_entry"
    AR_ASSISTED_PLACEMENT = "ar_assisted_placement"
    VISION_SUGGESTION_ACCEPTED = "vision_suggestion_accepted"
    REASSESSMENT_COMPARISON = "reassessment_comparison"


class ProtocolContext(str, Enum):
    """Active protocol emphasis modes that tune prompts and overlays."""

    TRAUMA = "trauma"
    RESPIRATORY_DISTRESS = "respiratory_distress"
    STROKE_NEURO = "stroke_neuro"
    PEDIATRIC_RESPIRATORY = "pediatric_respiratory"
    NEONATAL = "neonatal"
    ACLS = "acls"
    PALS = "pals"
    NRP = "nrp"


class ArcosMode(str, Enum):
    """AR workflow modes available in ARCOS."""

    LIVE_PATIENT = "live_patient"
    GUIDED_EXAM = "guided_exam"
    DEVICE_PLACEMENT = "device_placement"
    REASSESSMENT = "reassessment"
    TRAINING_REPLAY = "training_replay"
    SUPERVISOR_REVIEW = "supervisor_review"
    RAPID = "rapid"
    DETAILED = "detailed"


class ArcosQualityFlag(str, Enum):
    """Explicit AR failure/degraded-state flags."""

    ANATOMY_NOT_CONFIDENTLY_ANCHORED = "anatomy_not_confidently_anchored"
    INSUFFICIENT_LIGHTING = "insufficient_lighting"
    MOTION_BLUR = "motion_blur"
    OCCLUSION = "occlusion"
    PEDIATRIC_MODEL_MISMATCH = "pediatric_model_mismatch"
    NEONATAL_MODEL_MISMATCH = "neonatal_model_mismatch"
    LOW_CONFIDENCE_PROJECTION = "low_confidence_projection"
    UNSUPPORTED_SCENE_GEOMETRY = "unsupported_scene_geometry"
    OFFLINE_CAPTURE_UNRESOLVED = "offline_capture_unresolved"
    VISION_SERVICE_UNAVAILABLE = "vision_service_unavailable"


class Laterality(str, Enum):
    """Standard laterality for findings and projected overlays."""

    LEFT = "left"
    RIGHT = "right"
    BILATERAL = "bilateral"
    MIDLINE = "midline"
    GENERALIZED = "generalized"


class CareGraphEvidenceLinkContract(BaseModel):
    """References to CareGraph evidence nodes and derived edges."""

    evidence_node_id: str
    state_node_id: str | None = None
    supporting_edge_ids: list[str] = Field(default_factory=list)
    intervention_edge_ids: list[str] = Field(default_factory=list)
    response_edge_ids: list[str] = Field(default_factory=list)


class StructuredPhysicalFindingContract(BaseModel):
    """Authoritative structured physical finding owned by CPAE."""

    finding_id: str
    chart_id: str
    tenant_id: str

    anatomy: AnatomicalRegion
    system: PhysiologicalSystem
    finding_type: ClinicalFindingType
    severity: FindingSeverity
    evolution: FindingEvolution = FindingEvolution.NEW
    laterality: Laterality | None = None

    characteristics: list[str] = Field(default_factory=list)
    observation_method: DetectionMethod
    provider_id: str
    observed_at: datetime
    review_state: ReviewState = ReviewState.DIRECT_CONFIRMED

    evidence_artifact_ids: list[str] = Field(default_factory=list)
    intervention_ids: list[str] = Field(default_factory=list)
    response_ids: list[str] = Field(default_factory=list)
    caregraph: CareGraphEvidenceLinkContract | None = None


class VasOverlayContract(BaseModel):
    """Governed visual overlay rendered on a VAS anatomical surface."""

    overlay_id: str
    finding_id: str
    chart_id: str

    patient_model: PatientModelVariant
    view: AnatomicalView
    overlay_type: VisualOverlayType
    anchor_region: AnatomicalRegion
    severity: FindingSeverity
    evolution: FindingEvolution = FindingEvolution.NEW

    geometry_reference: str
    rendered_at: datetime
    provider_id: str
    review_state: ReviewState = ReviewState.DIRECT_CONFIRMED
    evidence_artifact_ids: list[str] = Field(default_factory=list)


class ArcosBodyAnchorContract(BaseModel):
    """Spatial anatomy anchor for an ARCOS session."""

    anchor_id: str
    session_id: str
    chart_id: str

    patient_model: PatientModelVariant
    view: AnatomicalView
    anatomy: AnatomicalRegion
    confidence: float = Field(ge=0.0, le=1.0)
    anchored_at: datetime
    provider_id: str


class ArcosOverlayCaptureContract(BaseModel):
    """AR overlay capture that must resolve back to structured CPAE and VAS state."""

    capture_id: str
    session_id: str
    chart_id: str
    finding_id: str
    overlay_id: str
    anchor_id: str

    mode: ArcosMode
    protocol_context: ProtocolContext | None = None
    quality_flags: list[ArcosQualityFlag] = Field(default_factory=list)
    review_state: ReviewState = ReviewState.DIRECT_CONFIRMED
    vision_assisted: bool = False

    provider_id: str
    captured_at: datetime


class ArcosSessionStartedEvent(BaseModel):
    """Published when an ARCOS session begins for a chart."""

    event_type: str = "ar.session.started"

    session_id: str
    chart_id: str
    tenant_id: str
    patient_model: PatientModelVariant
    mode: ArcosMode
    started_at: datetime


class ArcosAnatomyAnchoredEvent(BaseModel):
    """Published when anatomy is successfully anchored in AR space."""

    event_type: str = "ar.anatomy.anchored"

    session_id: str
    chart_id: str
    tenant_id: str
    anchor: ArcosBodyAnchorContract


class ArcosOverlayCreatedEvent(BaseModel):
    """Published when an AR overlay is created and linked to VAS/CPAE state."""

    event_type: str = "ar.overlay.created"

    session_id: str
    chart_id: str
    tenant_id: str
    capture: ArcosOverlayCaptureContract


class ArcosFindingAcceptedEvent(BaseModel):
    """Published when an AR-assisted finding is accepted into chart truth."""

    event_type: str = "ar.finding.accepted"

    session_id: str
    chart_id: str
    tenant_id: str
    finding: StructuredPhysicalFindingContract
    overlay: VasOverlayContract
    accepted_at: datetime


class ArcosQualityInsufficientEvent(BaseModel):
    """Published when AR input quality prevents governed capture."""

    event_type: str = "ar.quality.insufficient"

    session_id: str
    chart_id: str
    tenant_id: str
    quality_flags: list[ArcosQualityFlag] = Field(default_factory=list)
    detected_at: datetime
