"""Pydantic request/response schemas for Founder Studio."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# ── Workspace ──────────────────────────────────────────────
class StudioWorkspaceResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    name: str
    branding_json: dict | None = None
    settings_json: dict | None = None
    created_at: datetime


# ── Connections ────────────────────────────────────────────
class CreateConnectionRequest(BaseModel):
    provider_type: str = Field(min_length=1, max_length=64)
    display_name: str = Field(min_length=1, max_length=255)
    external_account_id: str | None = None
    scopes: list[str] | None = None
    encrypted_payload: str = Field(min_length=1, description="Encrypted credential material")


class UpdateConnectionRequest(BaseModel):
    display_name: str | None = None
    scopes: list[str] | None = None


class ConnectionResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    provider_type: str
    display_name: str
    external_account_id: str | None = None
    scopes: list[str] | None = None
    status: str
    expires_at: datetime | None = None
    last_validated_at: datetime | None = None
    last_success_at: datetime | None = None
    health_score: int
    created_at: datetime


# ── Assets ─────────────────────────────────────────────────
class CreateAssetRequest(BaseModel):
    asset_type: str = Field(min_length=1, max_length=64)
    source_type: str = "upload"
    title: str = Field(min_length=1, max_length=512)
    description: str | None = None
    storage_uri: str | None = None
    thumbnail_uri: str | None = None
    tenant_binding_id: UUID | None = None
    metadata_json: dict | None = None
    duration_ms: int | None = None


class UpdateAssetRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    approved_state: str | None = None
    metadata_json: dict | None = None


class AssetResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    asset_type: str
    source_type: str
    title: str
    description: str | None = None
    storage_uri: str | None = None
    thumbnail_uri: str | None = None
    approved_state: str
    tenant_binding_id: UUID | None = None
    metadata_json: dict | None = None
    duration_ms: int | None = None
    created_at: datetime


# ── Templates ──────────────────────────────────────────────
class CreateTemplateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    template_type: str = Field(min_length=1, max_length=64)
    description: str | None = None
    config_json: dict | None = None


class TemplateResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    template_type: str
    description: str | None = None
    config_json: dict | None = None
    created_at: datetime


# ── Campaigns ──────────────────────────────────────────────
class CreateCampaignRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    objective: str | None = None
    audience: str | None = None
    cta_type: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


class UpdateCampaignRequest(BaseModel):
    name: str | None = None
    objective: str | None = None
    audience: str | None = None
    status: str | None = None
    cta_type: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


class AttachAssetsRequest(BaseModel):
    asset_ids: list[UUID]


class CampaignResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    name: str
    objective: str | None = None
    audience: str | None = None
    status: str
    start_at: datetime | None = None
    end_at: datetime | None = None
    cta_type: str | None = None
    owner_id: UUID | None = None
    created_at: datetime


# ── Demo generation ────────────────────────────────────────
class GenerateDemoRequest(BaseModel):
    modules: list[str] = Field(min_length=1)
    audience: str = "investor"
    tone: str = "executive"
    duration_seconds: int = 90
    cta_objective: str | None = None
    source_asset_ids: list[UUID] | None = None


class DemoGenerationResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    request_type: str
    model_provider: str | None = None
    model_name: str | None = None
    confidence_score: float | None = None
    cost_estimate: float | None = None
    review_required: bool
    output_json: dict | None = None
    created_at: datetime


# ── Posts / publishing ─────────────────────────────────────
class GeneratePostRequest(BaseModel):
    channel: str = Field(min_length=1, max_length=64)
    campaign_id: UUID | None = None
    source_asset_id: UUID | None = None
    prompt: str | None = None


class SchedulePostRequest(BaseModel):
    scheduled_at: datetime


class PostResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    campaign_id: UUID | None = None
    channel: str
    caption_text: str | None = None
    media_asset_id: UUID | None = None
    scheduled_at: datetime | None = None
    published_at: datetime | None = None
    publish_status: str
    external_post_id: str | None = None
    created_at: datetime


# ── Review queue ───────────────────────────────────────────
class ReviewActionRequest(BaseModel):
    reason: str | None = None
    override_notes: str | None = None


class ReviewItemResponse(BaseModel):
    id: UUID
    generation_request_id: UUID | None = None
    item_type: str
    status: str
    reviewer_id: UUID | None = None
    reviewed_at: datetime | None = None
    reason: str | None = None
    override_notes: str | None = None
    workspace_id: UUID
    created_at: datetime


# ── Render queue ───────────────────────────────────────────
class RenderJobResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    source_asset_ids: list[str] | None = None
    template_id: UUID | None = None
    output_type: str | None = None
    target_aspect_ratios: list[str] | None = None
    status: str
    progress_pct: int
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


# ── Analytics ──────────────────────────────────────────────
class AnalyticsOverviewResponse(BaseModel):
    total_views: int = 0
    total_clicks: int = 0
    total_conversions: int = 0
    avg_engagement: float = 0.0
    videos_created_this_week: int = 0
    posts_published_this_week: int = 0
    demos_sent: int = 0
    active_campaigns: int = 0


class ChannelMetricsResponse(BaseModel):
    channel: str
    views: int = 0
    clicks: int = 0
    conversions: int = 0
    engagement_score: float = 0.0


# ── Studio home ────────────────────────────────────────────
class StudioHomeResponse(BaseModel):
    workspace: StudioWorkspaceResponse | None = None
    connections_count: int = 0
    healthy_connections: int = 0
    pending_reviews: int = 0
    active_renders: int = 0
    draft_posts: int = 0
    published_posts: int = 0
    active_campaigns: int = 0
    total_assets: int = 0
    analytics: AnalyticsOverviewResponse = AnalyticsOverviewResponse()


class StudioHealthResponse(BaseModel):
    credential_health: str = "unknown"
    channel_health: str = "unknown"
    render_queue_health: str = "unknown"
    posting_health: str = "unknown"
    model_availability: str = "unknown"


class StudioBriefResponse(BaseModel):
    date: str
    campaigns_active: int = 0
    posts_published_today: int = 0
    renders_in_progress: int = 0
    reviews_pending: int = 0
    ai_spend_today: float = 0.0
    suggested_actions: list[str] = []


# ── Event log ──────────────────────────────────────────────
class EventLogResponse(BaseModel):
    id: UUID
    workspace_id: UUID | None = None
    event_type: str
    actor_id: UUID | None = None
    entity_type: str | None = None
    entity_id: UUID | None = None
    payload: dict | None = None
    created_at: datetime
