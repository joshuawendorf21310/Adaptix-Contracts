"""Shared integration helpers for Inventory, Medications, and Narcotics services.

Provides canonical clients for publishing to Notifications, Search, Analytics, and
Audit services. These are used by all three domain services to maintain consistency.

Usage:
    from adaptix_contracts.supply_integrations import NotificationClient, SearchClient, AnalyticsClient, AuditClient

    # Publish low-stock notification
    await NotificationClient.send_low_stock_alert(
        tenant_id=tenant_id,
        recipient_user_id=user_id,
        item_name="Saline 0.9%",
        current_stock=5,
        par_level=20,
    )

    # Index item in search
    await SearchClient.index_inventory_item(
        tenant_id=tenant_id,
        item_id=item_id,
        item_name="Saline 0.9%",
        category="Fluids",
    )

    # Publish analytics event
    await AnalyticsClient.publish_stock_adjustment(
        tenant_id=tenant_id,
        quantity=10,
        cost=50.00,
    )

    # Log audit event
    await AuditClient.log_mutation(
        tenant_id=tenant_id,
        entity_type="inventory_item",
        entity_id=item_id,
        action="stock_adjusted",
        before_state={"stock": 15},
        after_state={"stock": 5},
    )
"""

from __future__ import annotations

import logging
import os
from typing import Optional, Any
from datetime import datetime, timezone
from uuid import UUID

import httpx

logger = logging.getLogger(__name__)


class NotificationClient:
    """Client for publishing notifications to the Notifications Service.

    Publishes alerts via HTTP to the Notifications Service internal API.
    Best-effort delivery with retries.
    """

    _BASE_URL = os.environ.get("NOTIFICATIONS_SERVICE_URL", "http://notifications:8000").rstrip("/")
    _TOKEN = os.environ.get("NOTIFICATIONS_SERVICE_TOKEN", "")
    _TIMEOUT = float(os.environ.get("NOTIFICATIONS_TIMEOUT_SECONDS", "5"))

    @classmethod
    async def send_low_stock_alert(
        cls,
        *,
        tenant_id: UUID,
        recipient_user_id: str,
        item_name: str,
        current_stock: int,
        par_level: int,
        recommended_quantity: int,
        unit: str = "units",
        cost_estimate: Optional[float] = None,
    ) -> bool:
        """Send low-stock alert to Supply Officer.

        Args:
            tenant_id: Tenant context
            recipient_user_id: User to notify
            item_name: Item name
            current_stock: Current stock level
            par_level: Par/target level
            recommended_quantity: Recommended reorder amount
            unit: Unit of measure
            cost_estimate: Estimated reorder cost

        Returns:
            True if delivery succeeded, False otherwise.
        """
        payload = {
            "tenant_id": str(tenant_id),
            "recipient_user_id": recipient_user_id,
            "notification_type": "low_stock_alert",
            "title": f"Low Stock: {item_name}",
            "message": f"{item_name} is below par level ({current_stock}/{par_level} {unit})",
            "item_name": item_name,
            "current_stock": current_stock,
            "par_level": par_level,
            "recommended_quantity": recommended_quantity,
            "unit": unit,
            "cost_estimate": cost_estimate,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_notification(payload)

    @classmethod
    async def send_expiration_alert(
        cls,
        *,
        tenant_id: UUID,
        recipient_user_id: str,
        item_name: str,
        expiration_date: datetime,
        current_stock: int,
        waste_forecast: float,
    ) -> bool:
        """Send expiration alert."""
        payload = {
            "tenant_id": str(tenant_id),
            "recipient_user_id": recipient_user_id,
            "notification_type": "expiration_alert",
            "title": f"Expiring Soon: {item_name}",
            "message": f"{item_name} expires on {expiration_date.strftime('%Y-%m-%d')}",
            "item_name": item_name,
            "expiration_date": expiration_date.isoformat(),
            "current_stock": current_stock,
            "waste_forecast": waste_forecast,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_notification(payload)

    @classmethod
    async def send_recall_alert(
        cls,
        *,
        tenant_id: UUID,
        recipient_user_id: str,
        item_name: str,
        recall_id: str,
        affected_lots: list[str],
        recommended_action: str,
    ) -> bool:
        """Send medication/medication recall alert."""
        payload = {
            "tenant_id": str(tenant_id),
            "recipient_user_id": recipient_user_id,
            "notification_type": "recall_alert",
            "title": f"RECALL: {item_name}",
            "message": f"{item_name} has been recalled (ID: {recall_id})",
            "item_name": item_name,
            "recall_id": recall_id,
            "affected_lots": affected_lots,
            "recommended_action": recommended_action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_notification(payload)

    @classmethod
    async def send_discrepancy_alert(
        cls,
        *,
        tenant_id: UUID,
        recipient_user_id: str,
        substance_name: str,
        missing_quantity: int,
        unit: str,
        escalation_flag: bool = False,
    ) -> bool:
        """Send narcotics discrepancy alert."""
        severity = "CRITICAL" if escalation_flag else "WARNING"
        payload = {
            "tenant_id": str(tenant_id),
            "recipient_user_id": recipient_user_id,
            "notification_type": "discrepancy_alert",
            "title": f"{severity}: Narcotic Discrepancy - {substance_name}",
            "message": f"{substance_name} discrepancy: {missing_quantity} {unit} missing",
            "substance_name": substance_name,
            "missing_quantity": missing_quantity,
            "unit": unit,
            "escalation_flag": escalation_flag,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_notification(payload)

    @classmethod
    async def _post_notification(cls, payload: dict[str, Any]) -> bool:
        """POST notification to Notifications Service."""
        if not cls._BASE_URL or not cls._TOKEN:
            logger.warning("Notifications Service not configured")
            return False

        headers = {"Authorization": f"Bearer {cls._TOKEN}", "Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=cls._TIMEOUT) as client:
                resp = await client.post(
                    f"{cls._BASE_URL}/api/v1/notifications/send",
                    json=payload,
                    headers=headers,
                )
            resp.raise_for_status()
            logger.info("Notification sent: %s", payload.get("notification_type"))
            return True
        except Exception as exc:
            logger.warning("Failed to send notification: %s", exc)
            return False


class SearchClient:
    """Client for indexing items in the Search Service."""

    _BASE_URL = os.environ.get("SEARCH_SERVICE_URL", "http://search:8000").rstrip("/")
    _TOKEN = os.environ.get("SEARCH_SERVICE_TOKEN", "")
    _TIMEOUT = float(os.environ.get("SEARCH_TIMEOUT_SECONDS", "5"))

    @classmethod
    async def index_inventory_item(
        cls,
        *,
        tenant_id: UUID,
        item_id: str,
        item_name: str,
        category: str,
        location: str,
        current_stock: int,
        par_level: int,
        expiration_date: Optional[datetime] = None,
        cost: Optional[float] = None,
        status: str = "active",
    ) -> bool:
        """Index an inventory item in the Search Service."""
        payload = {
            "tenant_id": str(tenant_id),
            "item_id": item_id,
            "item_name": item_name,
            "category": category,
            "location": location,
            "current_stock": current_stock,
            "par_level": par_level,
            "expiration_date": expiration_date.isoformat() if expiration_date else None,
            "cost": cost,
            "status": status,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._index_document("inventory_items", payload)

    @classmethod
    async def index_medication_lot(
        cls,
        *,
        tenant_id: UUID,
        medication_id: str,
        medication_name: str,
        lot_id: str,
        expiration_date: datetime,
        current_stock: int,
        storage_location: str,
    ) -> bool:
        """Index a medication lot in the Search Service."""
        payload = {
            "tenant_id": str(tenant_id),
            "medication_id": medication_id,
            "medication_name": medication_name,
            "lot_id": lot_id,
            "expiration_date": expiration_date.isoformat(),
            "current_stock": current_stock,
            "storage_location": storage_location,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._index_document("medication_lots", payload)

    @classmethod
    async def index_narcotic_vial(
        cls,
        *,
        tenant_id: UUID,
        substance_id: str,
        substance_name: str,
        vial_id: str,
        lot_id: str,
        unit_id: str,
        seal_status: str,
        chain_of_custody_status: str,
    ) -> bool:
        """Index a narcotic vial in the Search Service."""
        payload = {
            "tenant_id": str(tenant_id),
            "substance_id": substance_id,
            "substance_name": substance_name,
            "vial_id": vial_id,
            "lot_id": lot_id,
            "unit_id": unit_id,
            "seal_status": seal_status,
            "chain_of_custody_status": chain_of_custody_status,
            "indexed_at": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._index_document("narcotic_vials", payload)

    @classmethod
    async def _index_document(cls, index: str, document: dict[str, Any]) -> bool:
        """POST document to Search Service for indexing."""
        if not cls._BASE_URL or not cls._TOKEN:
            logger.warning("Search Service not configured")
            return False

        headers = {"Authorization": f"Bearer {cls._TOKEN}", "Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=cls._TIMEOUT) as client:
                resp = await client.post(
                    f"{cls._BASE_URL}/api/v1/search/index/{index}",
                    json=document,
                    headers=headers,
                )
            resp.raise_for_status()
            logger.info("Document indexed in %s: %s", index, document.get("item_id") or document.get("vial_id"))
            return True
        except Exception as exc:
            logger.warning("Failed to index document: %s", exc)
            return False


class AnalyticsClient:
    """Client for publishing analytics events to the Analytics Service."""

    _BASE_URL = os.environ.get("ANALYTICS_SERVICE_URL", "http://analytics:8000").rstrip("/")
    _TOKEN = os.environ.get("ANALYTICS_SERVICE_TOKEN", "")
    _TIMEOUT = float(os.environ.get("ANALYTICS_TIMEOUT_SECONDS", "5"))

    @classmethod
    async def publish_usage_event(
        cls,
        *,
        tenant_id: UUID,
        unit_id: Optional[str],
        event_type: str,
        quantity: int,
        cost: Optional[float] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Publish usage event to Analytics Service."""
        payload = {
            "tenant_id": str(tenant_id),
            "unit_id": unit_id,
            "event_type": event_type,
            "quantity": quantity,
            "cost": cost,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        return await cls._post_event(payload)

    @classmethod
    async def publish_waste_event(
        cls,
        *,
        tenant_id: UUID,
        unit_id: Optional[str],
        waste_reason: str,
        quantity: int,
        cost: float,
    ) -> bool:
        """Publish waste event to Analytics Service."""
        payload = {
            "tenant_id": str(tenant_id),
            "unit_id": unit_id,
            "event_type": "waste_recorded",
            "waste_reason": waste_reason,
            "quantity": quantity,
            "cost": cost,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_event(payload)

    @classmethod
    async def publish_risk_event(
        cls,
        *,
        tenant_id: UUID,
        unit_id: str,
        risk_type: str,
        risk_score: float,
        risk_level: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> bool:
        """Publish risk event (expiration risk, diversion risk, etc)."""
        payload = {
            "tenant_id": str(tenant_id),
            "unit_id": unit_id,
            "event_type": "risk_recorded",
            "risk_type": risk_type,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        return await cls._post_event(payload)

    @classmethod
    async def _post_event(cls, payload: dict[str, Any]) -> bool:
        """POST event to Analytics Service."""
        if not cls._BASE_URL or not cls._TOKEN:
            logger.warning("Analytics Service not configured")
            return False

        headers = {"Authorization": f"Bearer {cls._TOKEN}", "Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=cls._TIMEOUT) as client:
                resp = await client.post(
                    f"{cls._BASE_URL}/api/v1/analytics/events",
                    json=payload,
                    headers=headers,
                )
            resp.raise_for_status()
            logger.info("Analytics event published: %s", payload.get("event_type"))
            return True
        except Exception as exc:
            logger.warning("Failed to publish analytics event: %s", exc)
            return False


class AuditClient:
    """Client for publishing immutable audit entries to the Audit Service."""

    _BASE_URL = os.environ.get("AUDIT_SERVICE_URL", "http://audit:8000").rstrip("/")
    _TOKEN = os.environ.get("AUDIT_SERVICE_TOKEN", "")
    _TIMEOUT = float(os.environ.get("AUDIT_TIMEOUT_SECONDS", "5"))

    @classmethod
    async def log_mutation(
        cls,
        *,
        tenant_id: UUID,
        entity_type: str,
        entity_id: str,
        action: str,
        actor_user_id: Optional[str] = None,
        before_state: Optional[dict[str, Any]] = None,
        after_state: Optional[dict[str, Any]] = None,
        reason: Optional[str] = None,
    ) -> bool:
        """Log an immutable audit entry for a mutation."""
        payload = {
            "tenant_id": str(tenant_id),
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": action,
            "actor_user_id": actor_user_id,
            "before_state": before_state,
            "after_state": after_state,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_audit(payload)

    @classmethod
    async def log_approval(
        cls,
        *,
        tenant_id: UUID,
        entity_type: str,
        entity_id: str,
        approver_user_id: str,
        approval_type: str,
        reason: Optional[str] = None,
    ) -> bool:
        """Log an approval/confirmation action."""
        payload = {
            "tenant_id": str(tenant_id),
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": f"approval_{approval_type}",
            "actor_user_id": approver_user_id,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return await cls._post_audit(payload)

    @classmethod
    async def _post_audit(cls, payload: dict[str, Any]) -> bool:
        """POST audit entry to Audit Service."""
        if not cls._BASE_URL or not cls._TOKEN:
            logger.warning("Audit Service not configured")
            return False

        headers = {"Authorization": f"Bearer {cls._TOKEN}", "Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(timeout=cls._TIMEOUT) as client:
                resp = await client.post(
                    f"{cls._BASE_URL}/api/v1/audit/entries",
                    json=payload,
                    headers=headers,
                )
            resp.raise_for_status()
            logger.info("Audit entry logged: %s/%s %s", payload.get("entity_type"), payload.get("entity_id"), payload.get("action"))
            return True
        except Exception as exc:
            logger.warning("Failed to log audit entry: %s", exc)
            return False


__all__ = [
    "NotificationClient",
    "SearchClient",
    "AnalyticsClient",
    "AuditClient",
]
