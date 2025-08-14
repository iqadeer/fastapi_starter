# person_service.py
from typing import Annotated

from bson import ObjectId
from fastapi import Depends
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from db.database import get_db  # Import your existing DB dependency
from schemas.person_schema_mongo import PersonMongo


class PersonService:
    def __init__(self, db: AsyncDatabase):
        self.collection: AsyncCollection = db["persons"]

    async def get_all_persons(self) -> list[dict]:
        persons = await self.collection.find({}).to_list(None)
        for p in persons:
            p["_id"] = str(p["_id"])
        return persons

    async def get_person_by_id(self, person_id: str) :
        return await self.collection.find_one({"_id": ObjectId(person_id)})

    async def create_person(self, person: PersonMongo) -> str :
        person_dict = person.model_dump()
        result = await self.collection.insert_one(person_dict)
        new_id = str(result.inserted_id)
        return new_id

    async def update_person(self, person_id: str, person: PersonMongo) -> tuple[int, int] :
        person_dict = person.model_dump(exclude={"id"})  # exclude id so Mongo keeps _id
        result = await self.collection.update_one(
            {"_id": ObjectId(person_id)},
            {"$set": person_dict}
        )

        return result.modified_count, result.matched_count

    async def delete_person(self, person_id: str) -> int :
        result = await self.collection.delete_one({"_id": ObjectId(person_id)})
        return result.deleted_count

# Define the FastAPI dependency here (no separate file needed)
def get_person_service(
    db: Annotated[AsyncDatabase, Depends(get_db)]  # Inject DB
) -> PersonService:
    return PersonService(db)  # Return initialized service