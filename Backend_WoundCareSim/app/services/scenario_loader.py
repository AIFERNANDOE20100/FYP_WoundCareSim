# app/services/scenario_loader.py
class ScenarioLoader:
    """
    Handles loading scenario metadata.
    Week 2: Static dummy data.
    Week 5: Firestore integration.
    """

    async def load_scenario(self, scenario_id: str) -> dict:
        """
        Returns mocked scenario metadata.
        """
        return {
            "scenario_id": scenario_id,
            "patient_name": "John Doe",
            "patient_age": 45,
            "condition": "Left forearm surgical wound",
            "notes": "Mock scenario metadata (Week 2)."
        }
