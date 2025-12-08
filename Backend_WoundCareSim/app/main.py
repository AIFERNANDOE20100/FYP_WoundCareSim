from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.core.state_machine import Step, next_step
from app.core.coordinator import coordinate
import uvicorn

app = FastAPI(title="VR Nursing Education System Backend (Week 2 Skeleton)")

class StartSessionRequest(BaseModel):
    scenario_id: str
    student_id: str

# in-memory session store for Week 2
_sessions = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/session/start")
def start_session(req: StartSessionRequest):
    session_id = f"sess_{len(_sessions)+1}"
    _sessions[session_id] = {
        "scenario_id": req.scenario_id,
        "student_id": req.student_id,
        "current_step": Step.HISTORY.value,
        "events": []
    }
    return {"session_id": session_id, "current_step": Step.HISTORY.value}

class EvalInput(BaseModel):
    session_id: str
    step: str
    # Minimal: front-end/stubs will provide a list of evaluator responses
    evaluator_outputs: List[Dict] = []

@app.post("/session/step")
def session_step(payload: EvalInput):
    sid = payload.session_id
    if sid not in _sessions:
        raise HTTPException(status_code=404, detail="session not found")
    session = _sessions[sid]
    cur_step = session["current_step"]
    # call coordinator with provided evaluator_outputs (stubs from agents)
    agg = coordinate(payload.evaluator_outputs)
    # decide if we can move to next step - for now, assume front-end requests transition
    try:
        next_s = next_step(Step(cur_step))
    except Exception:
        next_s = None
    # log evaluation
    session["events"].append({"step": cur_step, "evaluation": agg})
    res = {"session_id": sid, "current_step": cur_step, "evaluation": agg}
    if next_s:
        session["current_step"] = next_s.value
        res["next_step"] = next_s.value
    return res

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
