from app.services.scenario_loader import ScenarioLoader
from app.rag.retriever import Retriever

class EvaluationService:
    """
    Creates agent input packages:
    - transcript
    - scenario metadata
    - RAG chunks
    - step
    """
    def __init__(self, retriever: Retriever, scenario_loader: ScenarioLoader):
        self.retriever = retriever
        self.scenario_loader = scenario_loader

    async def prepare_agent_context(self, transcript: str, scenario_id: str, step: str):
        scenario_meta = await self.scenario_loader.load_scenario(scenario_id)

        rag_chunks = await self.retriever.get_context(
            query=transcript,
            scenario_id=scenario_id,
            step=step
        )

        return {
            "transcript": transcript,
            "step": step,
            "rag_chunks": rag_chunks,
            "scenario_metadata": scenario_meta
        }
