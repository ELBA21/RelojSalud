from app.models.trainings import Workout
from app.database import MongoDBConnectionManager
from app.services.utils import load_json_from_path, to_out, get_gpx_path

local_COLLECTION = "trainings_test_4"


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
    async with MongoDBConnectionManager() as db:
        result = await db[local_COLLECTION].insert_one(doc)
        created = await db[local_COLLECTION].find_one({"_id": result.inserted_id})
        if not created:
            return
    return to_out(created)
