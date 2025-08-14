from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.routers import person_in_memory_router
from app.routers import person_mongo_router

app = FastAPI(lifespan=lifespan)

app.include_router(person_in_memory_router.router)
app.include_router(person_mongo_router.router)




