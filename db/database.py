# database.py
from typing import AsyncGenerator, Any, Mapping
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

async def get_db() -> AsyncGenerator[AsyncDatabase[Mapping[str, Any] | Any], None]:
    client = AsyncMongoClient("mongodb://localhost:27017/")
    try:
        yield client["mydatabase"]
    finally:
        await client.close()
