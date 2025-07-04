"""
Pydantic model for answer submission requests.
Defines the expected structure for submitting an answer to a session.
"""

from pydantic import BaseModel  

class AnswerRequest(BaseModel):
    """
    Model for an answer submission.
    - session_id: The ID of the session to which the answer belongs
    - answer: The user's answer to the current question
    """
    session_id: str
    answer: str