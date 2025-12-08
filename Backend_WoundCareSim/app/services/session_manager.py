from app.core.state_machine import Step, next_step

class SessionManager:
    """
    Tracks active sessions and their current step.
    Week 2: stores sessions in memory.
    Week 6: move to Firestore.
    """

    def __init__(self):
        self.sessions = {}

    def create_session(self, scenario_id: str, student_id: str):
        session_id = f"sess_{len(self.sessions)+1}"
        self.sessions[session_id] = {
            "scenario_id": scenario_id,
            "student_id": student_id,
            "current_step": Step.HISTORY.value,
            "logs": []
        }
        return session_id

    def get_session(self, session_id: str):
        return self.sessions.get(session_id)

    def advance_step(self, session_id: str):
        session = self.sessions.get(session_id)
        if not session:
            return None

        current_step = Step(session["current_step"])
        try:
            new_step = next_step(current_step)
            session["current_step"] = new_step.value
            return new_step.value
        except Exception:
            return None
