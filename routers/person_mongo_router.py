from fastapi import APIRouter, HTTPException, status, Response, Request
from bson import ObjectId
from person_schema_mongo import PersonMongo
from db import person_collection
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/api/person_mongo", tags=["person_mongo_db"])

# GET all persons
@router.get("/")
async def get_person():
    persons = list(person_collection.find({}))
    # Convert ObjectId to string for JSON serialization
    for p in persons:
        p["_id"] = str(p["_id"])
    return persons

# GET single person by ID
@router.get("/{person_id}")
async def get_person_by_id(person_id: str):
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    person = person_collection.find_one({"_id": ObjectId(person_id)})
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person["_id"] = str(person["_id"])
    return person

# POST a new person
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_person(person: PersonMongo, request: Request):
    person_dict = person.model_dump()
    print(person_dict)
    result = person_collection.insert_one(person_dict)

    new_id = str(result.inserted_id)

    location = request.url_for("get_person_by_id", id=new_id)  # assuming you have a `get_person` route
    return JSONResponse(
        content={"id": new_id},
        status_code=status.HTTP_201_CREATED,
        headers={"Location": str(location)})
    # return {"id": str(result.inserted_id)}

@router.put("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def put_person_by_id(person_id: str, person: PersonMongo):
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    person_dict = person.model_dump(exclude={"id"})  # exclude id so Mongo keeps _id
    result = person_collection.update_one(
        {"_id": ObjectId(person_id)},
        {"$set": person_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")

    # not needed as default is already changed in @router
    # return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person_by_id(person_id: str):
    if not ObjectId.is_valid(person_id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = person_collection.delete_one({"_id": ObjectId(person_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Person not found")
    # not needed as default is already changed in @router
    # return Response(status_code=status.HTTP_204_NO_CONTENT)