"""CAD AI assessment contracts.

AI guardrails are enforced here:
- AI may NOT dispatch units automatically.
- AI may NOT request HEMS automatically.
- AI may NOT create ePCR automatically.
- AI may NOT create billing handoff automatically.
- AI may NOT invent patient facts, times, or clinical data.
- Human review is always required for dispatch-impacting recommendations.
"""
from __future__ import annotations
from adaptix_contracts.cad.models import CadAIAssessment

__all__ = ["CadAIAssessment"]
