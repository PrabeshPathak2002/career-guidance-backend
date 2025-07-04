import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client["career_guidance"]
questions_collection = db["questions"]

async def fix_questions():
    await questions_collection.delete_many({})
    with open("app/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    await questions_collection.insert_one({"questions": questions})
    print("Questions loaded and cleaned.")

asyncio.run(fix_questions())