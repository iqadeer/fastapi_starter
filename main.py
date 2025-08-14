from fastapi import FastAPI
from routers import person_inmemory
from routers import person_mongo_router

app = FastAPI()

app.include_router(person_inmemory.router)
app.include_router(person_mongo_router.router)


