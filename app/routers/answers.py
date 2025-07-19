"""
Router for handling answer submissions in the Career Guidance API.
Allows users to submit answers to questions during a session.
"""

from fastapi import APIRouter, HTTPException, Request
from app.models.answer import AnswerRequest
from app.services.db import sessions_collection
from app.rate_limiter import limiter

router = APIRouter()

@router.post("/answer")
@limiter.limit("30/minute")  # Limit answer submissions
async def submit_answer(req: AnswerRequest, request: Request):
    """
    Endpoint to submit an answer for a given session.
    - Finds the session by ID
    - Appends the answer to the session's 'answers' array
    Rate limited to 30 answers per minute per IP.
    """
    session = await sessions_collection.find_one({"_id": req.session_id})
    if not session:
        raise HTTPException(404, "Session not found.")
    await sessions_collection.update_one(
        {"_id": req.session_id},
        {"$push": {"answers": req.answer}}
    )
    return {"status": "Answer recorded"}