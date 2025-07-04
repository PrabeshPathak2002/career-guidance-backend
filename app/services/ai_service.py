"""
Service for generating career recommendations using an AI model (OpenAI-compatible API).
Builds a prompt from user answers and requests recommendations from the AI.
"""

from openai import OpenAI
import os

# Initialize the OpenAI client with the OpenRouter endpoint and API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_career_recommendation(answers: list[str]) -> str:
    """
    Given a list of user answers, generate career recommendations using the AI model.
    Returns a string with 2-3 career paths, explanations, and next steps.
    """
    if not answers:
        return "No answers provided. Please complete at least one question."

    # Build a prompt for the AI model based on the user's answers
    prompt = (
        "You are a career guidance expert. Based on the user's answers below, "
        "recommend 2-3 career paths. Also explain why each is suitable and how the user can pursue them:\n\n"
        + "\n".join(f"- {a}" for a in answers)
    )

    # Call the AI model to get recommendations
    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {"role": "system", "content": "You are a professional career counselor."},
            {"role": "user", "content": prompt}
        ]
    )

    # Return the AI's response (the recommendations)
    return response.choices[0].message.content