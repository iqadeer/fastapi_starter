import pytest
from bson import ObjectId

from app.schemas.person_schema_mongo import PersonMongo
from app.services.person_service import PersonService


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
async def test_get_all_persons(mock_person_db):
    mock_db, mock_collection, mock_cursor, fake_persons = mock_person_db
    service = PersonService(db=mock_db)

    # Act
    result = await service.get_all_persons()

    # Assert
    assert len(result) == 2
    assert all("_id" in p and isinstance(p["_id"], str) for p in result)
    assert result[0]["first_name"] == "John"
    assert result[1]["first_name"] == "Jane"

    mock_collection.find.assert_called_once_with({})
    mock_cursor.to_list.assert_called_once_with(None)


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_get_person_by_id(mocker, mock_person_db, person_id):
    mock_db, mock_collection, _, fake_persons = mock_person_db

    # Make find_one an async mock returning the first person
    mock_collection.find_one = mocker.AsyncMock()
    mock_collection.find_one.return_value = fake_persons[0]

    service = PersonService(db=mock_db)

    # Act
    result = await service.get_person_by_id(person_id)

    # Assert
    assert result is not None
    assert result["_id"] == fake_persons[0]["_id"]
    assert result["first_name"] == "John"

    mock_collection.find_one.assert_called_once_with({"_id": ObjectId(person_id)})


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_create_person(mocker, mock_person_db, person_id):
    mock_db, mock_collection, _, fake_persons = mock_person_db

    # Make find_one an async mock returning the first person
    inserted_id = ObjectId(person_id)
    mock_collection.insert_one = mocker.AsyncMock()
    mock_collection.insert_one.return_value = mocker.MagicMock(inserted_id=inserted_id)
    service = PersonService(db=mock_db)
    person_model = PersonMongo(**fake_persons[0])
    # Act
    result = await service.create_person(person_model)

    # Assert
    assert result is not None
    assert result == person_id

    mock_collection.insert_one.assert_called_once_with(person_model.model_dump())


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_update_person(mocker, mock_person_db, person_id):
    mock_db, mock_collection, _, fake_persons = mock_person_db

    # Make find_one an async mock returning the first person
    updated_id = ObjectId(person_id)
    mock_collection.update_one = mocker.AsyncMock()
    mock_collection.update_one.return_value = mocker.MagicMock(modified_count=1, matched_count=1)
    service = PersonService(db=mock_db)
    person_model = PersonMongo(**fake_persons[0])
    # Act
    result = await service.update_person(person_id, person_model)

    # Assert
    assert result is not None
    modified_count, matched_count = result
    assert modified_count == 1
    assert matched_count == 1

    person_dict = person_model.model_dump(exclude={"id"})
    mock_collection.update_one.assert_called_once_with({"_id": updated_id}, {"$set": person_dict})


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [
    "64f0c0d2e1f1a2b3c4d5e6f7",
    "64f0c0d2e1f1a2b3c4d5e6f8"
])
async def test_delete_person(mocker, mock_person_db, person_id):
    mock_db, mock_collection, _, fake_persons = mock_person_db

    # Make find_one an async mock returning the first person
    deleted_id = ObjectId(person_id)
    mock_collection.delete_one = mocker.AsyncMock()
    mock_collection.delete_one.return_value = mocker.MagicMock(deleted_count=1)
    service = PersonService(db=mock_db)
    person_model = PersonMongo(**fake_persons[0])
    # Act
    deleted_count = await service.delete_person(person_id)

    # Assert
    assert deleted_count is not None
    assert deleted_count == 1

    person_dict = person_model.model_dump(exclude={"id"})
    mock_collection.delete_one.assert_called_once_with({"_id": deleted_id})
