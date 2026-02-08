from fastapi import APIRouter, HTTPException, status

from app.models.trainings import Workout
from app.database import MongoDBConnectionManager
from app.router.utils import to_out, load_json_from_path

router = APIRouter(prefix="/training", tags=["training"])
local_COLLECTION = "trainings_test_3"


@router.post("_test", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_training(payload: Workout):
    doc = payload.model_dump()

    now = payload.created_at
    doc["year"] = now.year
    doc["mont"] = now.month
    doc["day"] = now.day

    async with MongoDBConnectionManager() as db:
        result = await db[local_COLLECTION].insert_one(doc)
        created = await db[local_COLLECTION].find_one({"_id": result.inserted_id})
    if not created:
        raise HTTPException(status_code=500, detail="Eror al recuperar el dato")
    return to_out(created)


@router.post("/by_path", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def import_training(training_path: str):
    # Obtenemos el objeto pydantic
    payload_workout, objeto_fecha = load_json_from_path(training_path)
    # Transformamos dicho modelo a un dicionario python
    doc = payload_workout.model_dump()

    doc["training_date"] = objeto_fecha
    async with MongoDBConnectionManager() as db:
        result = await db[local_COLLECTION].insert_one(doc)
        created = await db[local_COLLECTION].find_one({"_id": result.inserted_id})
        if not created:
            raise HTTPException(status_code=500, detail="Error al recuperar dato")
    return to_out(created)
