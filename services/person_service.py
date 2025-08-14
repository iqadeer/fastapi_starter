# person_service.py
from typing import Annotated

from bson import ObjectId
from fastapi import Depends
from pymongo.database import Database
from pymongo.collection import Collection
from db.db import get_db  # Import your existing DB dependency
from schemas.person_schema_mongo import PersonMongo


class PersonService:
    def __init__(self, db: Database):
        self.collection: Collection = db["persons"]

    def get_all_persons(self) -> list[dict]:
        persons = list(self.collection.find({}))
        for p in persons:
            p["_id"] = str(p["_id"])
        return persons

    def get_person_by_id(self, person_id: str) :
        return self.collection.find_one({"_id": ObjectId(person_id)})

    def create_person(self, person: PersonMongo) -> str :
        person_dict = person.model_dump()
        result = self.collection.insert_one(person_dict)
        new_id = str(result.inserted_id)
        return new_id

    def update_person(self, person_id: str, person: PersonMongo) -> tuple[int, int] :
        person_dict = person.model_dump(exclude={"id"})  # exclude id so Mongo keeps _id
        result = self.collection.update_one(
            {"_id": ObjectId(person_id)},
            {"$set": person_dict}
        )

        return result.modified_count, result.matched_count

    def delete_person(self, person_id: str) -> int :
        result = self.collection.delete_one({"_id": ObjectId(person_id)})
        return result.deleted_count

# Define the FastAPI dependency here (no separate file needed)
def get_person_service(
    db: Annotated[Database, Depends(get_db)]  # Inject DB
) -> PersonService:
    return PersonService(db)  # Return initialized service