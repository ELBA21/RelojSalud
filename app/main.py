from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import mongo_connection_check
from app.config import FastAPIConfig, ENV

from app.router.trainings import router as trainings_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await mongo_connection_check()
    yield


app = FastAPI(**FastAPIConfig.dict(), lifespan=lifespan)


@app.get("/")
def chekee():
    return {
        "status": "asdasde pana Banana",
        "name": app.title,
        "version": app.version,
        "env": ENV,
    }


app.include_router(trainings_router)
