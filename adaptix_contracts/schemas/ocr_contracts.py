"""OCR extraction contract schemas for cross-domain communication.

Defines all typed contracts for the OCR job lifecycle: submission,
field candidate extraction, confidence scoring, human review, approval,
and structured field promotion into transport and care records.

These contracts are consumed by care (primary), transportlink, and billing.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class OcrSourceType(str, Enum):
    """Source document type submitted for OCR extraction."""

    PCS = "pcs"
    AOB = "aob"
    PHYSICIAN_CERTIFICATION = "physician_certification"
    TRANSPORT_CONSENT = "transport_consent"
    FACE_SHEET = "face_sheet"
    PRIOR_AUTHORIZATION = "prior_authorization"
    OTHER = "other"


class OcrJobStatus(str, Enum):
    """Processing lifecycle status for an OCR job."""

    QUEUED = "queued"
    PROCESSING = "processing"
    EXTRACTION_COMPLETE = "extraction_complete"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class OcrFieldConfidence(str, Enum):
    """Confidence tier for an extracted field candidate."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNRESOLVED = "unresolved"


class OcrJobCreate(BaseModel):
    """Contract for submitting a document for OCR extraction."""

    source_type: OcrSourceType
    document_id: str = Field(..., description="ID of the transport document or signed artifact")
    transport_request_id: Optional[str] = None
    chart_id: Optional[str] = None
    s3_key: str = Field(..., description="S3 object key for the source PDF")
    tenant_id: str
    requested_by_user_id: str


class OcrJobStatusResponse(BaseModel):
    """Read contract for an OCR job status check."""

    id: str
    tenant_id: str
    source_type: str
    document_id: str
    transport_request_id: Optional[str]
    chart_id: Optional[str]
    status: OcrJobStatus
    field_candidates_count: int
    review_required_count: int
    approved_count: int
    submitted_at: datetime
    extraction_completed_at: Optional[datetime]
    reviewed_at: Optional[datetime]
    reviewer_user_id: Optional[str]
    failure_reason: Optional[str]


class OcrFieldCandidateResponse(BaseModel):
    """Read contract for a single extracted field candidate.

    Returned as part of OcrJobDetailResponse for human review.
    The operator must approve or correct each candidate before promotion.
    """

    id: str
    job_id: str
    field_name: str
    extracted_value: str
    normalized_value: Optional[str]
    confidence: OcrFieldConfidence
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    page_number: Optional[int]
    bounding_box: Optional[dict]
    alternative_values: list[str] = Field(default_factory=list)
    review_status: str
    reviewer_note: Optional[str]


class OcrJobDetailResponse(BaseModel):
    """Full read contract for an OCR job including all field candidates."""

    id: str
    tenant_id: str
    source_type: str
    document_id: str
    transport_request_id: Optional[str]
    chart_id: Optional[str]
    status: OcrJobStatus
    submitted_at: datetime
    extraction_completed_at: Optional[datetime]
    field_candidates: list[OcrFieldCandidateResponse]
    failure_reason: Optional[str]


class OcrFieldApproval(BaseModel):
    """Operator approval or correction for a single field candidate."""

    field_candidate_id: str
    approved: bool
    corrected_value: Optional[str] = Field(None, description="Required when approved=True and value is corrected")
    reviewer_note: Optional[str] = Field(None, max_length=500)


class OcrApprovalRequest(BaseModel):
    """Contract for submitting operator review decisions for an OCR job."""

    job_id: str
    reviewer_user_id: str
    field_approvals: list[OcrFieldApproval]
    overall_approved: bool
    rejection_reason: Optional[str] = Field(None, description="Required when overall_approved=False")


class OcrApprovalResponse(BaseModel):
    """Response contract after an OCR review decision is processed."""

    job_id: str
    status: OcrJobStatus
    approved_fields: int
    rejected_fields: int
    promoted_to_structured: bool
    reviewed_at: datetime


class OcrExtractionCompletedEvent(BaseModel):
    """Published when OCR extraction finishes and review is required."""

    event_type: str = "care.ocr.extraction_completed"
    job_id: str
    tenant_id: str
    source_type: str
    document_id: str
    transport_request_id: Optional[str]
    chart_id: Optional[str]
    field_candidates_count: int
    review_required: bool
    completed_at: datetime


class OcrFieldsApprovedEvent(BaseModel):
    """Published when an operator approves OCR fields for structured promotion."""

    event_type: str = "care.ocr.fields_approved"
    job_id: str
    tenant_id: str
    transport_request_id: Optional[str]
    chart_id: Optional[str]
    approved_fields_count: int
    promoted_at: datetime
