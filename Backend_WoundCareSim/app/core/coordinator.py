from typing import List, Dict
from statistics import mean

def coordinate(evaluations: List[Dict]) -> Dict:
    """
    Lightweight aggregation stub for Week 2.
    """
    if not evaluations:
        return {"final_score": 0.0, "final_feedback": "No evaluations provided", "actions": []}

    scores = []
    actions = []
    rationales = []
    confidences = {}

    for ev in evaluations:
        score = float(ev.get("score", 0.0))
        scores.append(score)

        agent = ev.get("agent", "unknown")
        confidences[agent] = ev.get("confidence", 0.0)

        if ev.get("suggested_actions"):
            actions.extend(ev["suggested_actions"])

        rationale = ev.get("rationale")
        if rationale:
            rationales.append(f"[{agent}] {rationale}")

    final_score = mean(scores) if scores else 0.0
    final_feedback = " | ".join(rationales) if rationales else "No feedback"

    return {
        "final_score": round(final_score, 2),
        "final_feedback": final_feedback,
        "actions": actions,
        "confidences": confidences
    }
