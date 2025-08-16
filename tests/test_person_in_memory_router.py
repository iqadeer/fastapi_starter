import pytest
from app.routers.person_in_memory_router import get_person, get_person_by_id, post_person, put_person_by_id, delete_person_by_id
from app.schemas.person_schema import Person

# with autouse=true It will be available in all tests, we don't need to request it via argument dependency
@pytest.fixture(autouse=True)
def person_list() -> list[Person]:
    return [
        Person(
            id=1, first_name="John", last_name="Doe",
            city="NYC", terms_accepted=True, gender="M", dob="1990-01-01"
        ),
        Person(
            id=2, first_name="Jane", last_name="Smith",
            city="LA", terms_accepted=True, gender="F", dob="1992-02-02"
        ),
    ]

@pytest.mark.asyncio
async def test_get_all_persons(mocker, person_list):
    # Arrange: create a fake service
    # Below is for sync service mocking. If the function is async use AsyncMock
    # mock_service = mocker.Mock()
    mock_service = mocker.AsyncMock()
    mock_service.get_all_persons.return_value = person_list

    # Act: call the router function directly
    result = await get_person(person_service=mock_service)

    # Assert
    assert len(result) == 2
    assert result[0].first_name == "John"
    assert result[1].first_name == "Jane"
    mock_service.get_all_persons.assert_called_once()

@pytest.mark.asyncio
async def test_get_person_by_id(mocker, person_list):
    # Arrange: create a fake service
    mock_service = mocker.AsyncMock()
    mock_service.get_person_by_id.return_value = person_list[1]

    # Act: call the router function directly
    result = await get_person_by_id(2, person_service=mock_service)

    # Assert
    assert result is not None
    assert result.first_name == "Jane"
    mock_service.get_person_by_id.assert_called_once()
    mock_service.get_person_by_id.assert_called_once_with(2)
    called_args, called_kwargs = mock_service.get_person_by_id.call_args
    assert called_args[0] == 2
    assert len(called_args) == 1

@pytest.mark.asyncio
async def test_post_person(mocker, person_list):
    # Arrange: create a fake service
    mock_person = person_list[0]
    mock_service = mocker.AsyncMock()
    mock_service.create_person.return_value = mock_person.id

    # Act: call the router function directly
    result = await post_person(mock_person, person_service=mock_service)

    # Assert
    assert result is not None
    assert result == mock_person.id
    mock_service.create_person.assert_called_once()
    mock_service.create_person.assert_called_once_with(mock_person)
    called_args, called_kwargs = mock_service.create_person.call_args
    assert called_args[0] == mock_person


@pytest.mark.asyncio
async def test_update_person_by_id(mocker, person_list):
    # Arrange: create a fake service
    mock_person = person_list[0]
    mock_service = mocker.AsyncMock()
    mock_service.update_person.return_value = None

    # Act: call the router function directly
    result = await put_person_by_id(2, mock_person, person_service=mock_service)

    # Assert
    assert result is None
    mock_service.update_person.assert_called_once()
    mock_service.update_person.assert_called_once_with(2, mock_person)
    called_args, called_kwargs = mock_service.update_person.call_args
    assert called_args[0] == 2
    assert called_args[1] == mock_person


@pytest.mark.asyncio
@pytest.mark.parametrize("person_id", [4, 6, 0, 9, 10])
async def test_delete_person_by_id(mocker, person_list, person_id):
    # Arrange: create a fake service
    mock_person = person_list[0]
    mock_service = mocker.AsyncMock()
    mock_service.delete_person.return_value = None

    # Act: call the router function directly
    result = await delete_person_by_id(person_id, person_service=mock_service)

    # Assert
    assert result is None
    mock_service.delete_person.assert_called_once()
    mock_service.delete_person.assert_called_once_with(person_id)
    called_args, called_kwargs = mock_service.delete_person.call_args
    assert called_args[0] == person_id
