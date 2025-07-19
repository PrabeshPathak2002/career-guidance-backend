"""
Router for managing user sessions and questions in the Career Guidance API.
Handles session creation, question progression, and session reset.
"""

from fastapi import APIRouter, HTTPException, Request
from uuid import uuid4
from app.services.db import sessions_collection, questions_collection
from app.rate_limiter import limiter
from typing import List, Dict, Any

router = APIRouter()

async def get_questions() -> List[str]:
    """
    Retrieve the list of questions from the database.
    Returns a list of question strings, or an empty list if not found.
    """
    try:
        doc = await questions_collection.find_one({})
        print("DEBUG: questions_collection.find_one({}) returned:", doc)
        if not doc or "questions" not in doc:
            return []
        return doc["questions"]
    except Exception as e:
        print("DEBUG: Exception in get_questions():", e)  # Debug print for exceptions
        return []

@router.post("/session")
@limiter.limit("20/minute")  # Limit session creation
async def start_session(request: Request) -> Dict[str, Any]:
    """
    Start a new user session and return the first question.
    Creates a new session document in the DB and returns the session ID and first question.
    Rate limited to 20 sessions per minute per IP.
    """
    questions = await get_questions()
    if not questions:
        raise HTTPException(500, "Questions not found in database.")
    session_id = str(uuid4())
    try:
        await sessions_collection.insert_one({
            "_id": session_id,
            "answers": [],
            "current_question": 0
        })
    except Exception as e:
        raise HTTPException(500, "Failed to create session.")
    return {
        "session_id": session_id,
        "question_number": 1,
        "question": questions[0]
    }

@router.get("/question")
@limiter.limit("60/minute")  # Higher limit for getting questions
async def get_next_question(session_id: str, request: Request) -> Dict[str, Any]:
    """
    Get the next question for the given session.
    Increments the current question index and returns the next question.
    If all questions are answered, returns a completion message.
    Rate limited to 60 requests per minute per IP.
    """
    questions = await get_questions()
    try:
        session = await sessions_collection.find_one({"_id": session_id})
    except Exception as e:
        raise HTTPException(500, "Database error.")
    if not session:
        raise HTTPException(404, "Session not found.")
    idx = session["current_question"] + 1
    if idx >= len(questions):
        return {"message": "Interview Complete.", "status": "complete"}
    question = questions[idx]
    try:
        await sessions_collection.update_one(
            {"_id": session_id},
            {"$set": {"current_question": idx}}
        )
    except Exception as e:
        raise HTTPException(500, "Failed to update session.")
    return {"question_number": idx + 1, "question": question}

@router.post("/reset")
@limiter.limit("10/minute")  # Limit session resets
async def reset_session(session_id: str, request: Request) -> Dict[str, str]:
    """
    Reset the session's answers and question progress.
    Sets the current question index and answers array back to the start.
    Rate limited to 10 resets per minute per IP.
    """
    try:
        session = await sessions_collection.find_one({"_id": session_id})
    except Exception as e:
        raise HTTPException(500, "Database error.")
    if not session:
        raise HTTPException(404, "Session not found.")
    try:
        await sessions_collection.update_one(
            {"_id": session_id},
            {"$set": {"answers": [], "current_question": 0}}
        )
    except Exception as e:
        raise HTTPException(500, "Failed to reset session.")
    return {"status": "Session reset."}