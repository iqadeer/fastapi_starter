# database.py
from contextlib import asynccontextmanager, contextmanager
from typing import Generator

from pymongo import MongoClient
from pymongo.database import Database


def get_db() -> Generator[Database, None, None]:
    client = MongoClient("mongodb://localhost:27017/")
    try:
        yield  client["mydatabase"]
    finally:
        client.close()  # Ensure connection is closed




# from pymongo import MongoClient
#
# # Change this to your MongoDB URI
# client = MongoClient("mongodb://localhost:27017/")
#
# db = client["mydatabase"]  # Database name
# person_collection = db["persons"]  # Collection name
