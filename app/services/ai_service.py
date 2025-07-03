from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def generate_career_recommendation(answers: list[str]) -> str:
    if not answers:
        return "No answers provided. Please complete at least one question."

    prompt = (
        "You are a career guidance expert. Based on the user's answers below, "
        "recommend 2-3 career paths. Also explain why each is suitable and how the user can pursue them:\n\n"
        + "\n".join(f"- {a}" for a in answers)
    )

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=[
            {"role": "system", "content": "You are a professional career counselor."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content