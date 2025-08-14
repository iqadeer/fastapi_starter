from typing import Annotated

from app.db.database_in_memory import next_person_id, get_in_memory_db
from app.schemas.person_schema import Person
from fastapi import Depends

class PersonServiceInMemory:
    def __init__(self, db: list[Person]):
        self.person_db = db

    async def get_all_persons(self) -> list[Person]:
        return self.person_db

    async def get_person_by_id(self, id_: int):
        return next((p for p in self.person_db if p.id == id_), None)

    async def create_person(self, person: Person):
        person.id = next_person_id()
        self.person_db.append(person)
        return person.id

    async def update_person(self, id_: int, person: Person):
        self.person_db[id_] = person

    async def delete_person(self, id_: int):
        self.person_db.pop(id_)


def get_person_service_in_memory(db: Annotated[list[Person], Depends(get_in_memory_db)]) -> PersonServiceInMemory:
    return PersonServiceInMemory(db)