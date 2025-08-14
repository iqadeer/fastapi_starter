from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_client = AsyncMongoClient("mongodb://localhost:27017/")
    yield
    await app.state.db_client.close()
