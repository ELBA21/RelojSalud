from app.models.trainings import Workout
from app.database import MongoDBConnectionManager
from app.services.utils import load_json_from_path, to_out, get_gpx_path
from datetime import datetime

local_COLLECTION = "trainings_test_5"


async def create_training(payload: Workout):
    doc = payload.model_dump()

    now = payload.created_at
    doc["year"] = now.year
    doc["month"] = now.month
    doc["day"] = now.day

    async with MongoDBConnectionManager() as db:
        result = await db[local_COLLECTION].insert_one(doc)
        created = await db[local_COLLECTION].find_one({"_id": result.inserted_id})
        if not created:
            return
    return to_out(created)


async def import_training(training_path: str):
    # Obtenemos el objeto pydantic
    payload_workout, objeto_fecha = load_json_from_path(training_path)
    # Transformamos dicho modelo a un dicionario python
    doc = payload_workout.model_dump()

    doc["training_date"] = objeto_fecha
    gpx_path = get_gpx_path(training_path)
    if gpx_path != "olaNuro":
        doc["gpx_path"] = gpx_path
    else:
        doc["gpx_path"] = None
    async with MongoDBConnectionManager() as db:
        existe = await db[local_COLLECTION].find_one(
            {"training_date": doc["training_date"]}
        )
        if not existe:
            result = await db[local_COLLECTION].insert_one(doc)
            created = await db[local_COLLECTION].find_one({"_id": result.inserted_id})
            if not created:
                return {"result": None}

            return to_out(created)
        else:
            return to_out(existe)


# Funcion GET
async def get_training_of_the_day(date: datetime) -> dict:
    dia_inicio = date.replace(hour=0, minute=0, second=0, microsecond=0)
    dia_fin = date.replace(hour=23, minute=59, second=59)

    async with MongoDBConnectionManager() as db:
        result = await db[local_COLLECTION].find_one(
            {"training_date": {"$gt": dia_inicio, "$lt": dia_fin}}
        )

    if not result:
        return {"result": None}
    return result
