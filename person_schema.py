import humps
from pydantic import BaseModel, Field


class Person(BaseModel):
    id: int | None = None
    first_name: str = Field(..., max_length=60, min_length=1)
    last_name: str = Field(..., max_length=60, min_length=1)
    dob: str | None = None
    gender: str | None
    city: str
    terms_accepted: bool
    model_config = {
        "populate_by_name": True,
        "alias_generator": humps.camelize  # auto snake→camel
    }

