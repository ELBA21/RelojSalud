from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import mongo_connection_check
from app.config import FastAPIConfig, ENV


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
