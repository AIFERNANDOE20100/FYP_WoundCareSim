from typing import List, Dict

class VectorClient:
    """
    Week-2 dummy vector client.
    This will be replaced with a real vector store client (e.g., Pinecone, ChromaDB).
    """
    async def query(self, query_text: str, scenario_id: str, step: str) -> List[Dict]:
        """
        Returns static fake chunks for testing.
        No external API calls. No embeddings.
        """
        # Minimal fake content chunk representing RAG output
        return [
            {
                "content": f"Dummy RAG context for query='{query_text}', scenario='{scenario_id}', step='{step}'.",
                "metadata": {
                    "scenario_id": scenario_id,
                    "step": step,
                    "source": "week2_stub"
                }
            }
        ]

query_vectorstore = VectorClient().query # for backward compatibility if needed
