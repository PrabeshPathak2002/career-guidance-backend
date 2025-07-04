"""
Script to load or reset the career guidance questions in the MongoDB database.
Reads questions from a JSON file and stores them in the 'questions' collection.
Run this script whenever you want to update or reset the questions in the DB.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import json

# Load environment variables from .env file
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

# Connect to MongoDB using Motor (async client)
client = AsyncIOMotorClient(MONGO_URL)
db = client["career_guidance"]
questions_collection = db["questions"]

async def fix_questions():
    """
    Remove all existing questions and load new ones from the JSON file.
    This ensures the DB always has the latest set of questions.
    """
    await questions_collection.delete_many({})  # Clear out old questions
    with open("app/questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)
    await questions_collection.insert_one({"questions": questions})  # Insert new questions
    print("Questions loaded and cleaned.")

# Run the async function to update the DB
asyncio.run(fix_questions())