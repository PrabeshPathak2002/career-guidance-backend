from pydantic import BaseModel  

class AnswerRequest(BaseModel):
    session_id: str
    answer: str