from enum import Enum

class Step(Enum):
    HISTORY = "history"
    ASSESSMENT = "assessment"
    CLEANING = "cleaning"
    DRESSING = "dressing"
    COMPLETED = "completed"

# valid forward transitions
_VALID_TRANSITIONS = {
    Step.HISTORY: Step.ASSESSMENT,
    Step.ASSESSMENT: Step.CLEANING,
    Step.CLEANING: Step.DRESSING,
    Step.DRESSING: Step.COMPLETED,
}

def next_step(current_step: Step):
    """Return the next step or raise ValueError if none."""
    if current_step not in _VALID_TRANSITIONS:
        raise ValueError(f"No next step for {current_step}")
    return _VALID_TRANSITIONS[current_step]

def validate_action(step: Step, event_type: str) -> bool:
    """
    Naive validator: return True if event_type is allowed for the given step.
    This is a simple scaffold; business rules will be added later.
    """
    mapping = {
        Step.HISTORY: {"voice_transcript", "question_asked"},
        Step.ASSESSMENT: {"mcq_answer", "visual_assessment"},
        Step.CLEANING: {"action_handwash", "action_clean", "pick_material"},
        Step.DRESSING: {"action_dress", "action_secure_dressing"},
        Step.COMPLETED: set(),
    }
    allowed = mapping.get(step, set())
    return event_type in allowed
