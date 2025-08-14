# database.py
from typing import AsyncGenerator, Any, Mapping
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.database import Database as PymongoDatabase


# def get_db() -> Generator[Database, None, None]:
#     client = MongoClient("mongodb://localhost:27017/")
#     try:
#         yield  client["mydatabase"]
#     finally:
#         client.close()  # Ensure connection is closed



async def get_db() -> AsyncGenerator[AsyncDatabase[Mapping[str, Any] | Any], None]:
    client = AsyncMongoClient("mongodb://localhost:27017/")
    try:
        yield client["mydatabase"]
    finally:
        await client.close()

# from pymongo import MongoClient
#
# # Change this to your MongoDB URI
# client = MongoClient("mongodb://localhost:27017/")
#
# db = client["mydatabase"]  # Database name
# person_collection = db["persons"]  # Collection name
