from fastapi import APIRouter, HTTPException, status

from app.schemas.person_schema import Person

person1 = Person(id=1, first_name="John", last_name="Smith", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person2 = Person(id=2, first_name="John", last_name="Smith1", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person3 = Person(id=3, first_name="John", last_name="Smith2", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person_db: list[Person] = [person1, person2, person3]

next_id: int = 4

router = APIRouter(prefix="/api/person", tags=["person_in_memory"])

@router.get("/")
async def get_person():
    return  person_db

@router.get("/{id}")
async def get_person_by_id(id_: int):
    # Find person by ID
    person = next((p for p in person_db if p.id == id_), None)

    if person:
        return person

    # Return 404 if not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with ID {id_} not found"
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_person(person: Person):
    global next_id
    person.id = next_id
    person_db.append(person)
    next_id += 1


@router.put("/{id}")
async def put_person_by_id(id_: int, person: Person):
    person_db[id_] = person

@router.delete("/{id}")
async def delete_person_by_id(person_id: int):
    person_db.pop(person_id)