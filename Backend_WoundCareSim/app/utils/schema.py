"""
Evaluator output format (informal specification).
This file contains helpers and dataclasses if needed later.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class EvidenceRef(BaseModel):
    doc_id: str
    chunk_index: Optional[int] = None
    excerpt: Optional[str] = None

class EvaluatorOutput(BaseModel):
    agent: str
    step: str
    score: float
    rationale: str
    confidence: float
    evidence_refs: List[EvidenceRef] = []
    suggested_actions: List[str] = []
    raw: Dict[str, Any] = {}
