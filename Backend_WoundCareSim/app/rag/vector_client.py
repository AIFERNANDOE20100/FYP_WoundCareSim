from typing import List, Dict

class VectorClient:
    """
    Placeholder vector store client for Week 2.
    Real OpenAI Vector Store integration will be added in Week 4.
    """

    def __init__(self, vector_store_id: str):
        self.vector_store_id = vector_store_id

    async def query(self, query_text: str, scenario_id: str, step: str, top_k: int = 5) -> List[Dict]:
        """
        Returns dummy chunks now.
        Week 4 will replace with real vector store search.
        """
        return [
            {
                "chunk": f"Mock RAG chunk for '{query_text}' (scenario: {scenario_id}, step: {step})",
                "score": 0.9,
                "metadata": {
                    "scenario_id": scenario_id,
                    "step": step,
                }
            }
        ]
