import json

import pytest
from bson import ObjectId

from app.schemas.person_schema_mongo import PersonMongo
from app.services.person_service import PersonService
from app.routers.person_mongo_router import get_persons, get_person_by_id, create_person, put_person_by_id, delete_person_by_id


@pytest.fixture()
def mock_person_db(mocker):
    # Fake persons data
    fake_persons = [
        {"_id": ObjectId(), "first_name": "John", "last_name": "Doe", "city": "NYC", "terms_accepted": True, "gender": "Male"},
        {"_id": ObjectId(), "first_name": "Jane", "last_name": "Smith", "city": "LA", "terms_accepted": True, "gender": "Female"},
    ]

    # Mock the cursor returned by find()
    mock_cursor = mocker.MagicMock()
    mock_cursor.to_list = mocker.AsyncMock()
    mock_cursor.to_list.return_value = fake_persons

    # Mock the collection
    mock_collection = mocker.MagicMock()
    mock_collection.find.return_value = mock_cursor

    # Mock the database
    mock_db = mocker.MagicMock()
    mock_db.__getitem__.return_value = mock_collection  # db["persons"] returns mock_collection

    return mock_db, mock_collection, mock_cursor, fake_persons


@pytest.mark.asyncio
async def test_get_all_persons(mocker, mock_person_db):
    # Arrange: create a fake service
    # Below is for sync service mocking. If the function is async use AsyncMock
    # mock_service = mocker.Mock()
    db, collection, cursor, person_list = mock_person_db
    mock_service = mocker.AsyncMock()
    mock_service.get_all_persons.return_value = person_list

    # Act: call the router function directly
    result = await get_persons(person_service=mock_service)

    # Assert
    assert len(result) == 2
    assert result[0]["first_name"] == "John"
    assert result[1]["first_name"] == "Jane"
    mock_service.get_all_persons.assert_called_once()

@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_create_person(mocker, mock_person_db, person_id):
    # Arrange: create a fake service
    db, collection, cursor, person_list = mock_person_db
    mock_service = mocker.AsyncMock()
    mock_service.create_person.return_value = person_id

    person_model = PersonMongo(**person_list[0])
    # Act: call the router function directly
    result = await create_person(person=person_model, request=mocker.MagicMock(), person_service=mock_service)

    # Assert
    assert result is not None
    body = result.body

    data = json.loads(body)
    assert data["id"] == person_id
    mock_service.create_person.assert_called_once()
    mock_service.create_person.assert_called_once_with(person_model)
    called_args, called_kwargs = mock_service.create_person.call_args
    assert called_args[0] == person_model
    assert len(called_args) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_update_person(mocker, mock_person_db, person_id):
    # Arrange: update a fake service
    db, collection, cursor, person_list = mock_person_db
    mock_service = mocker.AsyncMock()
    mock_service.update_person.return_value = (1, 1)

    person_model = PersonMongo(**person_list[0])
    # Act: call the router function directly
    result = await put_person_by_id(person_id=person_id, person=person_model, person_service=mock_service)

    # Assert
    assert result is None

    mock_service.update_person.assert_called_once()
    mock_service.update_person.assert_called_once_with(person_id, person_model)
    called_args, called_kwargs = mock_service.update_person.call_args
    assert called_args[0] == person_id
    assert called_args[1] == person_model
    assert len(called_args) == 2

@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_delete_person(mocker, mock_person_db, person_id):
    # Arrange: delete a fake service
    db, collection, cursor, person_list = mock_person_db
    mock_service = mocker.AsyncMock()
    mock_service.delete_person.return_value = 1

    person_model = PersonMongo(**person_list[0])
    # Act: call the router function directly
    result = await delete_person_by_id(person_id=person_id, person_service=mock_service)

    # Assert
    assert result is None

    mock_service.delete_person.assert_called_once()
    mock_service.delete_person.assert_called_once_with(person_id)
    called_args, called_kwargs = mock_service.delete_person.call_args
    assert called_args[0] == person_id
    assert len(called_args) == 1