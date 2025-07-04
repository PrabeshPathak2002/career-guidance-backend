"""
Database connection module for the Career Guidance API.
Handles both async (Motor) and sync (PyMongo) clients for production and testing environments.
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Get the MongoDB connection URL from environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Use PyMongo (sync) for tests, Motor (async) for production
if os.getenv("TESTING", "0") == "1":
    from pymongo import MongoClient
    client = MongoClient(MONGO_URL)
else:
    from motor.motor_asyncio import AsyncIOMotorClient
    client = AsyncIOMotorClient(MONGO_URL)

# Access the main database and collections
# 'career_guidance' is the main DB, with 'sessions' and 'questions' collections

db = client["career_guidance"]
sessions_collection = db["sessions"]
questions_collection = db["questions"]

# Print the MongoDB URL for debugging purposes
print("Using MongoDB URL:", MONGO_URL)