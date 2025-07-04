from fastapi import APIRouter, HTTPException
from uuid import uuid4
from app.services.db import sessions_collection, questions_collection
from typing import List, Dict, Any

router = APIRouter()

async def get_questions() -> List[str]:
    """
    Retrieve the list of questions from the database.
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
async def start_session() -> Dict[str, Any]:
    """
    Start a new session and return the first question.
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
async def get_next_question(session_id: str) -> Dict[str, Any]:
    """
    Get the next question for the given session.
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
async def reset_session(session_id: str) -> Dict[str, str]:
    """
    Reset the session's answers and question progress.
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