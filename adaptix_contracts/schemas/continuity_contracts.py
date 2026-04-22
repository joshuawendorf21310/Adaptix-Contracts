"""Shared continuity contracts for collaborative workspace sync across Adaptix domains."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AttachmentSyncState(str, Enum):
    STAGED = "staged"
    UPLOADING = "uploading"
    SYNCED = "synced"
    FAILED = "failed"
    CONFLICT = "conflict"
    DELETED = "deleted"


class DraftStatus(str, Enum):
    DRAFT = "draft"
    SYNCED = "synced"
    CONFLICTED = "conflicted"


class ResumeState(str, Enum):
    AVAILABLE = "available"
    FINALIZED = "finalized"
    LOCKED = "locked"


class SyncState(str, Enum):
    SYNCED = "synced"
    CONFLICTED = "conflicted"
    PENDING = "pending"


class ClientDeviceIdentity(BaseModel):
    device_id: str
    device_type: str
    platform: str
    app_version: str | None = None
    session_token: str | None = None


class AttachmentSyncStatus(BaseModel):
    attachment_id: str
    file_name: str
    mime_type: str | None = None
    size_bytes: int | None = None
    storage_key: str | None = None
    checksum_sha256: str | None = None
    sync_state: AttachmentSyncState
    updated_at: datetime


class ResumeStateResponse(BaseModel):
    workspace: dict[str, Any]
    resume_state: ResumeState
    draft_status: DraftStatus
    sync_state: SyncState
    sync_version: int
    last_saved_at: datetime | None = None
    last_saved_by_user_id: str | None = None
    workflow_step: str | None = None
    validation_errors: list[Any] = Field(default_factory=list)
    unresolved_warnings: list[Any] = Field(default_factory=list)
    attachments: list[AttachmentSyncStatus] = Field(default_factory=list)
    state: dict[str, Any] = Field(default_factory=dict)


class ConflictResponse(BaseModel):
    tenant_id: str
    domain: str
    object_type: str
    object_id: str
    expected_sync_version: int
    actual_sync_version: int
    server_state: dict[str, Any]
    conflict_fields: list[str] = Field(default_factory=list)
    message: str = "Conflict detected: server state has been modified."
