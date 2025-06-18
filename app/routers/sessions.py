from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter()

# Placeholder questions
questions = [
    "What are your favorite subjects or activities?", 
    "Which skills do you excel at or enjoy developing?",
    # Add more questions as needed
]

sessions = {}

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@router.post("/session")
async def start_session():
    session_id = str(uuid4())
    sessions[session_id] = {"answers": [], "current_question": 0}
    return {
        "session_id": session_id,
        "question_number": 1,
        "question": questions[0]
    }

@router.get("/question")
async def get_next_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sess = sessions[session_id]
    idx = sess["current_question"] + 1
    if idx >= len(questions):
        return {"message": "Interview Complete."}
    sess["current_question"] = idx
    return {"question_number": idx + 1, "question": questions[idx]}

@router.post("/answer")
async def submit_answer(req: AnswerRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sess = sessions[req.session_id]
    sess["answers"].append(req.answer)
    return {"status": "Answer recorded"}

@router.post("/reset")
async def reset_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sessions[session_id] = {"answers": [], "current_question": 0}
    return {"status": "Session reset."}