from app.core.state_machine import Step, next_step, validate_action

def test_next_step():
    assert next_step(Step.HISTORY) == Step.ASSESSMENT
    assert next_step(Step.ASSESSMENT) == Step.CLEANING

def test_validate_action():
    assert validate_action(Step.HISTORY, "voice_transcript") is True
    assert validate_action(Step.CLEANING, "mcq_answer") is False
