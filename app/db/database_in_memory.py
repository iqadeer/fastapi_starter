from app.schemas.person_schema import Person

person1 = Person(id=1, first_name="John", last_name="Smith", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person2 = Person(id=2, first_name="John", last_name="Smith1", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person3 = Person(id=3, first_name="John", last_name="Smith2", dob='2024-02-13', gender="Male", city="London", terms_accepted=True)
person_db: list[Person] = [person1, person2, person3]

next_id: int = 3

def next_person_id() -> int:
    global next_id
    next_id += 1
    return next_id

async def get_in_memory_db():
    return person_db