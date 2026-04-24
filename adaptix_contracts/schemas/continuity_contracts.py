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


class LockState(str, Enum):
    """Truthful lock state for shared continuity workspaces."""

    HELD = "held"
    TAKEOVER_AVAILABLE = "takeover_available"
    UNLOCKED = "unlocked"


class ContinuityAuditAction(str, Enum):
    """Canonical audit actions emitted by continuity workflows."""

    LOCK_ACQUIRED = "lock_acquired"
    LOCK_RENEWED = "lock_renewed"
    LOCK_TAKEN_OVER = "lock_taken_over"
    LOCK_RELEASED = "lock_released"
    OPERATION_RECORDED = "operation_recorded"


class ClientDeviceIdentity(BaseModel):
    device_id: str
    device_type: str
    platform: str
    app_version: str | None = None
    session_token: str | None = None


class ContinuityLockSnapshot(BaseModel):
    """Current lock state for a shared mutable workspace."""

    state: LockState
    locked_by_user_id: str | None = None
    locked_by_device_id: str | None = None
    locked_at: datetime | None = None
    expires_at: datetime | None = None
    takeover_available: bool = False


class OperationEnvelope(BaseModel):
    """Canonical device-originated write envelope for continuity replay."""

    operation_id: str
    operation_type: str
    domain: str
    object_type: str
    object_id: str
    base_sync_version: int = Field(ge=0)
    payload: dict[str, Any] = Field(default_factory=dict)
    device: ClientDeviceIdentity
    client_created_at: datetime | None = None
    client_sequence: int | None = Field(default=None, ge=0)


class ContinuityAuditEvent(BaseModel):
    """Structured audit payload for continuity activity."""

    workspace: dict[str, Any]
    action: ContinuityAuditAction
    status: str
    actor_user_id: str | None = None
    device: ClientDeviceIdentity | None = None
    sync_version: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime


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
