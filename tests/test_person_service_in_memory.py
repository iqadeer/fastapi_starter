# tests/test_person_service_in_memory.py
import pytest
import asyncio

from app.schemas.person_schema import Person
from app.services.person_service_in_memory import PersonServiceInMemory


# Fixture to provide a fresh in-memory list for each test
@pytest.fixture
def person_db_fixture():
    return []


# Fixture to provide the service
@pytest.fixture
def person_service(person_db_fixture):
    return PersonServiceInMemory(person_db_fixture)


# Test get_all_persons
@pytest.mark.asyncio
async def test_get_all_persons_empty(person_service):
    result = await person_service.get_all_persons()
    assert result == []


@pytest.mark.asyncio
async def test_create_person(person_service):
    person = Person(first_name="Alice", dob='10/10/2025', gender='male', last_name='Smith', city='Springfield', terms_accepted=False)
    person_id = await person_service.create_person(person)

    assert person_id == 4  # first ID from next_person_id()
    assert len(await person_service.get_all_persons()) == 1
    assert (await person_service.get_person_by_id(person_id)).first_name == "Alice"


@pytest.mark.asyncio
async def test_get_person_by_id(person_service):
    person = Person(first_name="Alice", dob='10/10/2025', gender='male', last_name='Smith', city='Springfield', terms_accepted=False)
    person_id = await person_service.create_person(person)

    result: Person = await person_service.get_person_by_id(person_id)
    assert result is not None
    assert result.first_name == "Alice"


@pytest.mark.asyncio
async def test_update_person(person_service):
    person:Person = Person(first_name="Alice", dob='10/10/2025', gender='male', last_name='Smith', city='Springfield', terms_accepted=False)
    person_id = await person_service.create_person(person)

    updated_person = Person(first_name="Alice", dob='11/10/2025', gender='male', last_name='Smith', city='Springfield', terms_accepted=False)
    await person_service.update_person(person_id, updated_person)  # current code uses index
    result: list[Person] = await person_service.get_all_persons()
    assert result[0].first_name == "Alice"
    assert result[0].dob == '11/10/2025'


@pytest.mark.asyncio
async def test_delete_person(person_service):
    person = Person(first_name="Alice", dob='10/10/2025', gender='male', last_name='Smith', city='Springfield', terms_accepted=False)
    person_id = await person_service.create_person(person)

    await person_service.delete_person(person_id)  # delete by index
    all_persons = await person_service.get_all_persons()
    assert all_persons == []
