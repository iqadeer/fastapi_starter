from typing import Optional

import humps
from bson import ObjectId
from pydantic import BaseModel, Field


class PersonMongo(BaseModel):
    # id: Optional[ObjectId] = Field(default=None, alias='_id')
    first_name: str = Field(..., max_length=60, min_length=1)
    last_name: str = Field(..., max_length=60, min_length=1)
    dob: str | None = None
    gender: str | None
    city: str
    terms_accepted: bool
    model_config = {
        "populate_by_name": True,
        "alias_generator": humps.camelize, # auto snake→camel
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "first_name": "Imran",
                "last_name": "Qadeer",
                "dob": "10/10/2001",
                "gender": "Male",
                "city": "Lahore",
                "terms_accepted": True
            }
        }
    }
