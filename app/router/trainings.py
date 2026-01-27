from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from app.models.trainings import Workout
from app.database import MongoDBConnectionManager
from app.router.utils import to_out

router = APIRouter(prefix="/training", tags=["training"])


@router.post("", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_training(payload: Workout):
    doc = payload.model_dump()

    now = payload.created_at
    doc["year"] = now.year
    doc["mont"] = now.month
    doc["day"] = now.day

    async with MongoDBConnectionManager() as db:
        result = await db["trainings"].insert_one(doc)
        created = await db["trainings"].find_one({"_id": result.inserted_id})
    if not created:
        raise HTTPException(status_code=500, detail="Eror al recuperar el dato")
    return to_out(created)
