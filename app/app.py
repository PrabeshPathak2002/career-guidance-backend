"""
Main FastAPI application for the Career Guidance API.
Sets up the app, includes routers, and defines top-level endpoints.
"""

from fastapi import FastAPI, HTTPException, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from app.routers.sessions import router as sessions_router
from app.routers.answers import router as answers_router
from app.services.ai_service import generate_career_recommendation
from app.services.db import sessions_collection
from app.rate_limiter import limiter

# Create the FastAPI app instance
app = FastAPI(
    title="Career Guidance API",
    description="AI-powered career guidance with rate limiting",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # React dev server
        "http://localhost:5173",           # Vite dev server
        "https://career-guidance-frontend-flame.vercel.app"  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers for session and answer management
app.include_router(sessions_router)
app.include_router(answers_router)

@app.get("/")
@limiter.limit("30/minute")
def root(request: Request):
    """
    Root endpoint to verify the API is running.
    Rate limited to 30 requests per minute per IP.
    """
    return {"message": "Career Guidance API"}

@app.get("/recommend")
@limiter.limit("10/minute")  # Stricter limit for AI recommendations
async def give_recommendation(session_id: str, request: Request):
    """
    Generate career recommendations based on the answers in a session.
    Fetches the session by ID, retrieves answers, and calls the AI service.
    Rate limited to 10 requests per minute per IP due to AI service costs.
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