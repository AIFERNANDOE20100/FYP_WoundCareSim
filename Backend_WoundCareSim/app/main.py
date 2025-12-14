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
    try:
        # Load scenario from Firestore
        scenario = load_scenario(req.scenario_id)
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
        
        # Create session with scenario metadata
        session_id = session_manager.create_session(
            scenario_id=req.scenario_id,
            student_id=req.student_id,
            scenario_metadata=scenario
        )
        
        # Prepare scenario summary for frontend
        scenario_summary = {
            "scenario_id": scenario.get("scenario_id"),
            "title": scenario.get("scenario_title"),
            "patient_history": scenario.get("patient_history"),
            "wound_details": scenario.get("wound_details")
        }
        
        return {
            "session_id": session_id,
            "current_step": Step.HISTORY.value,
            "scenario_summary": scenario_summary
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")

class EvalInput(BaseModel):
    session_id: str
    step: str
    # Minimal: front-end/stubs will provide a list of evaluator responses
    evaluator_outputs: List[Dict] = []

@app.post("/session/step")
def session_step(payload: EvalInput):
    sid = payload.session_id
    session = session_manager.get_session(sid)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    cur_step = session["current_step"]
    scenario_id = session["scenario_id"]
    
    # Retrieve RAG context if user input is provided
    rag_context = None
    if payload.user_input:
        try:
            rag_context = retrieve_context(
                query=payload.user_input,
                scenario_id=scenario_id,
                top_k=5
            )
            
            # Store RAG results for debugging
            session_manager.add_rag_result(sid, {
                "step": cur_step,
                "query": payload.user_input,
                "results": rag_context
            })
        except Exception as e:
            print(f"RAG retrieval warning: {str(e)}")
            rag_context = []
    
    # Call coordinator with evaluator outputs
    try:
        agg = coordinate(payload.evaluator_outputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
    
    # Log the evaluation
    session_manager.add_log(sid, {
        "step": cur_step,
        "user_input": payload.user_input,
        "evaluation": agg,
        "rag_used": rag_context is not None
    })
    
    # Determine if we can move to next step
    try:
        next_s = next_step(Step(cur_step))
    except Exception:
        next_s = None
    
    # Log evaluation in events for backward compatibility
    session["events"].append({"step": cur_step, "evaluation": agg})
    
    # Prepare response
    res = {
        "session_id": sid,
        "current_step": cur_step,
        "evaluation": agg
    }
    
    if next_s:
        session["current_step"] = next_s.value
        res["next_step"] = next_s.value
    
    if rag_context:
        res["rag_context"] = rag_context
    
    return res

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
