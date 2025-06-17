from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from openai import OpenAI
import os


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

app = FastAPI()

# Placeholder questions
questions = [
    "What are your favorite subjects or activities?",
    "Which skills do you excel at or enjoy developing?",
    #"What level of education have you completed or plan to complete?",
    #"Do you prefer working with people, data, technology, or things?",
    #"What kind of work environment do you prefer?",
    #"What are your core values in a job?",
    #"Are there any industries or roles you are already interested in or want to avoid?"
]

sessions = {}

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@app.get("/")
def root():
    return {"message": "Career Guidance API"}

@app.post("/session")
async def start_session():
    session_id = str(uuid4())
    sessions[session_id] = {"answers": [], "current_question": 0}
    return {
        "session_id": session_id,
        "question_number": 1,
        "question": questions[0]
    }

@app.get("/question")
async def get_next_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sess = sessions[session_id]
    idx = sess["current_question"] + 1
    if idx >= len(questions):
        return {"message": "Interview Complete."}
    sess["current_question"] = idx
    return {"question_number": idx + 1, "question": questions[idx]}

@app.post("/answer")
async def submit_answer(req: AnswerRequest):
    if req.session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sess = sessions[req.session_id]
    sess["answers"].append(req.answer)
    return {"status": "Answer recorded"}

@app.get("/recommend")
async def give_recommendation(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    answers = sessions[session_id]["answers"]
    prompt = ("Based on the following user answers, suggest 2-3 suitable career paths and explain your reasoning and how should they achieve it:\n"
        f"{answers}")
    try:
        response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {"role": "system", "content": "..."},
            {"role": "user", "content": prompt}
        ]
        )
        return {"recommendations": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"AI request failed: {str(e)}")

@app.post("/reset")
async def reset_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(404, "Session not found.")
    sessions[session_id] = {"answers": [], "current_question": 0}
    return {"status": "Session reset."}
