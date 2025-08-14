from fastapi import APIRouter, HTTPException, status, Request, Depends
from bson import ObjectId
from typing import Annotated

from app.schemas.person_schema_mongo import PersonMongo
from fastapi.responses import JSONResponse

from app.services.person_service import PersonService, get_person_service

router = APIRouter(prefix="/api/person_mongo", tags=["person_mongo_db"])

# GET all persons
@router.get("/")
async def get_persons(person_service: Annotated[PersonService, Depends(get_person_service)]):
    return await person_service.get_all_persons()

# GET single person by ID
@router.get("/{person_id}")
async def get_person_by_id(person_id: str, person_service: Annotated[PersonService, Depends(get_person_service)]):
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    person = await person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person["_id"] = str(person["_id"])
    return person

# POST a new person
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_person(person: PersonMongo, request: Request,
                        person_service: Annotated[PersonService, Depends(get_person_service)]):
    new_id = await person_service.create_person(person)
    location = request.url_for("get_person_by_id", id=new_id)  # assuming you have a `get_person` route
    return JSONResponse(
        content={"id": new_id},
        status_code=status.HTTP_201_CREATED,
        headers={"Location": str(location)})
    # return {"id": str(result.inserted_id)}

# Update a new person
@router.put("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_person_by_id(person_id: str, person: PersonMongo,
                           person_service: Annotated[PersonService, Depends(get_person_service)]):

    if not ObjectId.is_valid(person_id.strip()):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    (modified_count, matched_count) = await person_service.update_person(person_id.strip(), person)

    if matched_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")

    # not needed as default is already changed in @router
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_id(person_id: str, person_service: Annotated[PersonService, Depends(get_person_service)]):
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    deleted_count = await person_service.delete_person(person_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")


    # not needed as default is already changed in @router
    # return Response(status_code=status.HTTP_204_NO_CONTENT)