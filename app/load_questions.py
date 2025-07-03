import json
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["career_guidance"]
questions_collection = db["questions"]

async def main():
    with open("app/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    # Remove existing questions to avoid duplicates
    await questions_collection.delete_many({})
    # Insert as a single document with a list, or as separate docs
    await questions_collection.insert_one({"questions": questions})
    print("Questions loaded into MongoDB.")

if __name__ == "__main__":
    asyncio.run(main())