from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.routers import person_inmemory
from app.routers import person_mongo_router

app = FastAPI(lifespan=lifespan)

app.include_router(person_inmemory.router)
app.include_router(person_mongo_router.router)


