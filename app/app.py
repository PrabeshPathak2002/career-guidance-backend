"""
Main FastAPI application for the Career Guidance API.
Sets up the app, includes routers, and defines top-level endpoints.
"""

from fastapi import FastAPI, HTTPException
from app.routers.sessions import router as sessions_router
from app.routers.answers import router as answers_router
from app.services.ai_service import generate_career_recommendation
from app.services.db import sessions_collection

# Create the FastAPI app instance
app = FastAPI()

# Include routers for session and answer management
app.include_router(sessions_router)
app.include_router(answers_router)

@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {"message": "Career Guidance API"}

@app.get("/recommend")
async def give_recommendation(session_id: str):
    """
    Generate career recommendations based on the answers in a session.
    Fetches the session by ID, retrieves answers, and calls the AI service.
    """
    session = await sessions_collection.find_one({"_id": session_id})
    if not session:
        raise HTTPException(404, "Session not found.")
    answers = session["answers"]
    try:
        result = generate_career_recommendation(answers)
        return {"recommendations": result}
    except Exception as e:
        raise HTTPException(500, f"AI request failed: {str(e)}")