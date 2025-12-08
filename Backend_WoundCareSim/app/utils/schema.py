"""
Evaluator output format (informal specification).
This file contains helpers and dataclasses if needed later.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class EvidenceRef:
    doc_id: str
    chunk_index: Optional[int] = None
    excerpt: Optional[str] = None

@dataclass
class EvaluatorOutput:
    agent: str                 # "communication" | "knowledge" | "clinical"
    step: str                  # e.g., "history"
    score: float               # 0.0 - 100.0
    rationale: str
    confidence: float          # 0.0 - 1.0
    evidence_refs: List[EvidenceRef]
    suggested_actions: List[str]
