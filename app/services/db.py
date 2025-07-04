import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

if os.getenv("TESTING", "0") == "1":
    from pymongo import MongoClient
    client = MongoClient(MONGO_URL)
else:
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(MONGO_URL)

db = client["career_guidance"]
sessions_collection = db["sessions"]
questions_collection = db["questions"]
print("Using MongoDB URL:", MONGO_URL)