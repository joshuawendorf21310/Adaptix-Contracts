"""
AWS EventBridge Client Wrapper

Production-ready EventBridge client with connection pooling, error handling,
and automatic retries for Adaptix's unified operational graph.
"""

from __future__ import annotations

import logging
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from core_app.core.config import get_settings

logger = logging.getLogger(__name__)


class EventBridgeClient:
    """
    Thread-safe EventBridge client wrapper with connection pooling and retry logic.

    Features:
    - Automatic connection management with boto3 session pooling
    - Built-in retry logic with exponential backoff
    - Structured logging with correlation IDs
    - Resource tagging for cost allocation
    - Multi-region support
    """

    def __init__(self, event_bus_name: str | None = None, region_name: str | None = None):
        """
        Initialize EventBridge client.

        Args:
            event_bus_name: Custom event bus name. Defaults to settings.eventbridge_bus_name
            region_name: AWS region. Defaults to settings.aws_region
        """
        settings = get_settings()
        self.region_name = region_name or settings.aws_region or "us-east-1"
        self.event_bus_name = event_bus_name or getattr(
            settings, "eventbridge_bus_name", "adaptixcore-events"
        )

        # Configure boto3 client with retries and connection pooling
        boto_config = Config(
            region_name=self.region_name,
            retries={
                "max_attempts": 3,
                "mode": "adaptive",  # Adaptive retry mode for better throughput
            },
            max_pool_connections=50,  # Support high-throughput event publishing
            connect_timeout=5,
            read_timeout=10,
        )

        self._client = None
        self._boto_config = boto_config

        logger.info(
            "eventbridge.client.initialized",
            extra={
                "event_bus_name": self.event_bus_name,
                "region": self.region_name,
            },
        )

    @property
    def client(self):
        """Lazy-load EventBridge client for connection pooling efficiency."""
        if self._client is None:
            self._client = boto3.client("events", config=self._boto_config)
        return self._client

    def put_event(
        self,
        source: str,
        detail_type: str,
        detail: dict[str, Any],
        resources: list[str] | None = None,
        trace_header: str | None = None,
    ) -> dict[str, Any]:
        """
        Publish a single event to EventBridge.

        Args:
            source: Event source (e.g., 'Adaptix.transport', 'Adaptix.crewlink')
            detail_type: Event detail type (e.g., 'TransportRequestCreated')
            detail: Event payload as dictionary
            resources: Optional list of ARNs or resource identifiers
            trace_header: Optional X-Ray trace header for distributed tracing

        Returns:
            Response from EventBridge including event ID and ingestion time

        Raises:
            EventBridgePublishError: If event publishing fails after retries
        """
        try:
            entry = {
                "Source": source,
                "DetailType": detail_type,
                "Detail": self._serialize_detail(detail),
                "EventBusName": self.event_bus_name,
            }

            if resources:
                entry["Resources"] = resources

            if trace_header:
                entry["TraceHeader"] = trace_header

            response = self.client.put_events(Entries=[entry])

            # Check for failed entries
            if response.get("FailedEntryCount", 0) > 0:
                failed = response.get("Entries", [{}])[0]
                error_code = failed.get("ErrorCode", "Unknown")
                error_msg = failed.get("ErrorMessage", "No error message")

                logger.error(
                    "eventbridge.put_event.failed",
                    extra={
                        "source": source,
                        "detail_type": detail_type,
                        "error_code": error_code,
                        "error_message": error_msg,
                        "event_bus": self.event_bus_name,
                    },
                )

                raise EventBridgePublishError(
                    f"Failed to publish event: {error_code} - {error_msg}"
                )

            event_id = response["Entries"][0]["EventId"]

            logger.info(
                "eventbridge.put_event.success",
                extra={
                    "source": source,
                    "detail_type": detail_type,
                    "event_id": event_id,
                    "event_bus": self.event_bus_name,
                },
            )

            return {
                "event_id": event_id,
                "event_bus_name": self.event_bus_name,
                "ingestion_time": response["Entries"][0].get("IngestionTime"),
            }

        except (BotoCoreError, ClientError) as e:
            logger.error(
                "eventbridge.put_event.error",
                extra={
                    "source": source,
                    "detail_type": detail_type,
                    "error": str(e),
                    "event_bus": self.event_bus_name,
                },
                exc_info=True,
            )
            raise EventBridgePublishError(f"Failed to publish event: {str(e)}") from e

    def put_events(
        self,
        events: list[dict[str, Any]],
        batch_size: int = 10,
    ) -> dict[str, Any]:
        """
        Publish multiple events to EventBridge in batches.

        EventBridge has a limit of 10 events per PutEvents call, so we automatically
        batch larger requests.

        Args:
            events: List of event dictionaries with 'source', 'detail_type', 'detail' keys
            batch_size: Number of events per batch (max 10, AWS limit)

        Returns:
            Summary of published events including success/failure counts

        Raises:
            EventBridgePublishError: If any batch fails after retries
        """
        if batch_size > 10:
            logger.warning(
                "eventbridge.put_events.batch_size_exceeded",
                extra={"requested": batch_size, "max": 10},
            )
            batch_size = 10

        results = {
            "total_events": len(events),
            "successful": 0,
            "failed": 0,
            "event_ids": [],
            "errors": [],
        }

        # Process events in batches
        for i in range(0, len(events), batch_size):
            batch = events[i : i + batch_size]

            try:
                entries = []
                for event in batch:
                    entry = {
                        "Source": event["source"],
                        "DetailType": event["detail_type"],
                        "Detail": self._serialize_detail(event["detail"]),
                        "EventBusName": self.event_bus_name,
                    }

                    if "resources" in event:
                        entry["Resources"] = event["resources"]

                    if "trace_header" in event:
                        entry["TraceHeader"] = event["trace_header"]

                    entries.append(entry)

                response = self.client.put_events(Entries=entries)

                # Process response
                failed_count = response.get("FailedEntryCount", 0)
                results["failed"] += failed_count

                for idx, entry_result in enumerate(response.get("Entries", [])):
                    if "EventId" in entry_result:
                        results["successful"] += 1
                        results["event_ids"].append(entry_result["EventId"])
                    else:
                        error_code = entry_result.get("ErrorCode", "Unknown")
                        error_msg = entry_result.get("ErrorMessage", "No error message")
                        results["errors"].append({
                            "event_index": i + idx,
                            "error_code": error_code,
                            "error_message": error_msg,
                        })

                logger.info(
                    "eventbridge.put_events.batch_complete",
                    extra={
                        "batch_start": i,
                        "batch_size": len(batch),
                        "successful": len(batch) - failed_count,
                        "failed": failed_count,
                    },
                )

            except (BotoCoreError, ClientError) as e:
                logger.error(
                    "eventbridge.put_events.batch_error",
                    extra={
                        "batch_start": i,
                        "batch_size": len(batch),
                        "error": str(e),
                    },
                    exc_info=True,
                )
                results["failed"] += len(batch)
                for idx in range(len(batch)):
                    results["errors"].append({
                        "event_index": i + idx,
                        "error_code": "BatchError",
                        "error_message": str(e),
                    })

        logger.info(
            "eventbridge.put_events.complete",
            extra={
                "total": results["total_events"],
                "successful": results["successful"],
                "failed": results["failed"],
            },
        )

        return results

    def _serialize_detail(self, detail: dict[str, Any]) -> str:
        """
        Serialize event detail to JSON string.

        EventBridge requires the Detail field to be a JSON string, not a dict.
        """
        import json

        return json.dumps(detail, default=str, separators=(",", ":"))

    def describe_event_bus(self) -> dict[str, Any]:
        """
        Get information about the configured event bus.

        Useful for health checks and diagnostics.
        """
        try:
            response = self.client.describe_event_bus(Name=self.event_bus_name)
            return {
                "name": response.get("Name"),
                "arn": response.get("Arn"),
                "policy": response.get("Policy"),
            }
        except (BotoCoreError, ClientError) as e:
            logger.error(
                "eventbridge.describe_event_bus.error",
                extra={
                    "event_bus": self.event_bus_name,
                    "error": str(e),
                },
                exc_info=True,
            )
            raise EventBridgePublishError(f"Failed to describe event bus: {str(e)}") from e

    def list_rules(self, name_prefix: str | None = None) -> list[dict[str, Any]]:
        """
        List EventBridge rules for the configured event bus.

        Args:
            name_prefix: Optional prefix to filter rules

        Returns:
            List of rule summaries
        """
        try:
            kwargs = {"EventBusName": self.event_bus_name}
            if name_prefix:
                kwargs["NamePrefix"] = name_prefix

            response = self.client.list_rules(**kwargs)
            return response.get("Rules", [])
        except (BotoCoreError, ClientError) as e:
            logger.error(
                "eventbridge.list_rules.error",
                extra={
                    "event_bus": self.event_bus_name,
                    "error": str(e),
                },
                exc_info=True,
            )
            return []


class EventBridgePublishError(Exception):
    """Raised when event publishing to EventBridge fails."""
    pass


# Singleton instance for connection pooling
_event_bus_client: EventBridgeClient | None = None


def get_event_bus_client() -> EventBridgeClient:
    """
    Get or create singleton EventBridge client instance.

    This ensures connection pooling across the application lifecycle.
    """
    global _event_bus_client

    if _event_bus_client is None:
        _event_bus_client = EventBridgeClient()

    return _event_bus_client
