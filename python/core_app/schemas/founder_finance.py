from __future__ import annotations

from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ApproveBusinessTransactionRequest(BaseModel):
    chosen_category: str = Field(min_length=2, max_length=64)
    chosen_account_code: str = Field(min_length=2, max_length=32)
    note: str | None = Field(default=None, max_length=1000)


class ExportPackageRequest(BaseModel):
    export_kind: Literal[
        "ledger_csv",
        "expense_csv",
        "summary_pdf",
        "json_review",
        "accountant_bundle",
        "source_bundle",
        "tax_workpaper",
    ]
    tax_year: int = Field(ge=2020, le=2100)


class BusinessTransactionResponse(BaseModel):
    id: UUID
    occurred_on: date | None = None
    vendor_name: str | None = None
    category: str | None = None
    amount_cents: int
    review_status: str
    confidence_score: float | None = None
    tax_deductible: bool
    document_id: UUID | None = None
    suggested_account_code: str | None = None
    suggestion_rationale: str | None = None


class PersonalTaxDocumentResponse(BaseModel):
    id: UUID
    tax_year: int
    document_type: str
    review_status: str
    ocr_status: str
    original_filename: str
    summary_text: str | None = None
    ai_confidence: float | None = None
    created_at: str
