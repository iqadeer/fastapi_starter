# database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from pymongo import AsyncMongoClient
from fastapi import FastAPI

client: AsyncMongoClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = AsyncMongoClient("mongodb://localhost:27017/")
    yield
    await client.close()

async def get_db() -> AsyncGenerator:
    yield client["mydatabase"]