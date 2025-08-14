from fastapi import FastAPI

from db.database import lifespan
from routers import person_inmemory
from routers import person_mongo_router

app = FastAPI(lifespan=lifespan)

app.include_router(person_inmemory.router)
app.include_router(person_mongo_router.router)


