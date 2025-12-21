from typing import Dict, Any, List

from app.services.scenario_loader import load_scenario
from app.rag.retriever import retrieve_with_rag
from app.core.coordinator import Coordinator
from app.utils.schema import EvaluatorResponse


class EvaluationService:
    """
    Week-4 Evaluation Service

    Responsibilities:
    - Load scenario metadata
    - Retrieve RAG context
    - Prepare agent context
    - Aggregate evaluator outputs (schema-driven)
    """

    def __init__(self, coordinator: Coordinator):
        self.coordinator = coordinator

    async def prepare_agent_context(
        self,
        transcript: str,
        scenario_id: str,
        step: str,
        system_instruction: str = ""
    ) -> Dict[str, Any]:
        """
        Prepares the full context passed to evaluator agents.
        """

        # Load scenario (sync)
        scenario_metadata = load_scenario(scenario_id)

        # Retrieve RAG context (async)
        rag_result = await retrieve_with_rag(
            query=transcript,
            scenario_id=scenario_id,
            system_instruction=system_instruction
        )

        return {
            "transcript": transcript,
            "step": step,
            "scenario_metadata": scenario_metadata,
            "rag_context": rag_result["text"],
            "rag_raw": rag_result["raw_response"],
        }

    async def aggregate_evaluations(
        self,
        evaluator_outputs: List[EvaluatorResponse],
        step: str
    ) -> Dict[str, Any]:
        """
        Aggregates evaluator agent outputs using the coordinator.

        NOTE:
        - evaluator_outputs MUST already be schema-validated
        """

        if not evaluator_outputs:
            raise ValueError("No evaluator outputs provided")

        if not all(isinstance(ev, EvaluatorResponse) for ev in evaluator_outputs):
            raise TypeError("All evaluator outputs must be EvaluatorResponse instances")

        return self.coordinator.aggregate(
            evaluations=evaluator_outputs,
            current_step=step
        )
