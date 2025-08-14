from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends

from app.schemas.person_schema import Person
from app.services.person_service_in_memory import PersonServiceInMemory, get_person_service_in_memory

router = APIRouter(prefix="/api/person", tags=["person_in_memory"])

@router.get("/")
async def get_person(person_service: Annotated[PersonServiceInMemory, Depends(get_person_service_in_memory)]):
    return  await person_service.get_all_persons()

@router.get("/{id}")
async def get_person_by_id(id_: int, person_service: Annotated[PersonServiceInMemory, Depends(get_person_service_in_memory)]):
    # Find person by ID
    person = await person_service.get_person_by_id(id_)

    if person:
        return person

    # Return 404 if not found
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Person with ID {id_} not found"
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_person(person: Person, person_service: Annotated[PersonServiceInMemory, Depends(get_person_service_in_memory)]):
    return await person_service.create_person(person)


@router.put("/{id}")
async def put_person_by_id(id_: int, person: Person, person_service: Annotated[PersonServiceInMemory, Depends(get_person_service_in_memory)]):
    return await person_service.update_person(id_, person)

@router.delete("/{id}")
async def delete_person_by_id(person_id: int, person_service: Annotated[PersonServiceInMemory, Depends(get_person_service_in_memory)]):
    return await person_service.delete_person(person_id)
