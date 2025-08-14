# database.py
from typing import AsyncGenerator

from fastapi import Request
from pymongo import AsyncMongoClient


async def get_db(request: Request) -> AsyncGenerator:
    client: AsyncMongoClient = request.app.state.db_client
    yield client["mydatabase"]