from fastapi import APIRouter, HTTPException
from app.models.answer import AnswerRequest
from app.services.db import sessions_collection

router = APIRouter()

@router.post("/answer")
async def submit_answer(req: AnswerRequest):
    """Record an answer for a specific session."""
    session = await sessions_collection.find_one({"_id": req.session_id})
    if not session:
        raise HTTPException(404, "Session not found.")
    await sessions_collection.update_one(
        {"_id": req.session_id},
        {"$push": {"answers": req.answer}}
    )
    return {"status": "Answer recorded"}