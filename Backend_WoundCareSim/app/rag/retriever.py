from typing import List
from app.rag.vector_client import VectorClient

class Retriever:
    """
    Retrieves context from vector store based on query + scenario + step.
    """

    def __init__(self, vector_client: VectorClient):
        self.vector_client = vector_client

    async def get_context(self, query: str, scenario_id: str, step: str) -> List[dict]:
        """
        Week 2: returns mocked vector data.
        Week 4: will integrate real OpenAI retrieval.
        """
        return await self.vector_client.query(query_text=query, scenario_id=scenario_id, step=step)
