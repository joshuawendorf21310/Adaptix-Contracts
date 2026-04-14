"""AI domain events.

Registered in the EventCatalog on import so they are discoverable by the
event bus and observability tooling.
"""

from __future__ import annotations

from adaptix_contracts.events.domain_event import DomainEvent
from adaptix_contracts.events.event_catalog import EventCatalog

# ---------------------------------------------------------------------------
# Event classes
# ---------------------------------------------------------------------------

class AiAnalysisCompletedEvent(DomainEvent):
    event_type: str = "ai.analysis.completed"
    entity_type: str = "ai"

    analysis_id: str = ""
    findings: str = ""
    confidence_score: float = 0.0
    completed_at: str = ""

class AiAnalysisRequestedEvent(DomainEvent):
    event_type: str = "ai.analysis.requested"
    entity_type: str = "ai"

    analysis_id: str = ""
    source_type: str = ""
    source_id: str = ""
    analysis_type: str = ""
    requested_at: str = ""

class AiExplanationGeneratedEvent(DomainEvent):
    event_type: str = "ai.explanation.generated"
    entity_type: str = "ai"

    decision_id: str = ""
    explanation_text: str = ""
    factors: str = ""
    generated_at: str = ""

class AiHallucinationDetectedEvent(DomainEvent):
    event_type: str = "ai.hallucination.detected"
    entity_type: str = "ai"

    output_id: str = ""
    hallucination_type: str = ""
    confidence: str = ""
    detected_at: str = ""

class AiNarrativeGeneratedEvent(DomainEvent):
    event_type: str = "ai.narrative.generated"
    entity_type: str = "ai"

    epcr_id: str = ""
    narrative_text: str = ""
    confidence_score: float = 0.0
    generated_at: str = ""

class AiScoringCompletedEvent(DomainEvent):
    event_type: str = "ai.scoring.completed"
    entity_type: str = "ai"

    score_id: str = ""

    score_type: float = 0.0
    score_value: float = 0.0
    factors: str = ""

class AiSummaryGeneratedEvent(DomainEvent):
    event_type: str = "ai.summary.generated"
    entity_type: str = "ai"

    source_id: str = ""
    summary_text: str = ""
    key_points: str = ""
    generated_at: str = ""

# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------

_catalog = EventCatalog()
_catalog.register("ai.analysis.completed", AiAnalysisCompletedEvent)
_catalog.register("ai.analysis.requested", AiAnalysisRequestedEvent)
_catalog.register("ai.explanation.generated", AiExplanationGeneratedEvent)
_catalog.register("ai.hallucination.detected", AiHallucinationDetectedEvent)
_catalog.register("ai.narrative.generated", AiNarrativeGeneratedEvent)
_catalog.register("ai.scoring.completed", AiScoringCompletedEvent)
_catalog.register("ai.summary.generated", AiSummaryGeneratedEvent)
