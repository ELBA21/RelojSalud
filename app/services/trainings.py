from app.models.trainings import Workout_trote
from app.database import MongoDBConnectionManager
from app.services.utils import load_json_from_path, to_out, get_gpx_path
from datetime import datetime, timedelta

local_COLLECTION = "V2_test2"


async def create_training(payload: Workout_trote):
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


# Teoricamente deberia funcionar para todos los modelos habidos y por haber
async def get_stats_list(
    fecha_inicio: datetime, fecha_fin: datetime, parametros: list[str]
) -> list[dict]:
    output = {"training_date": 1, "_id": 0}
    for field in Workout_trote.model_fields:
        if field in parametros:
            output[str(field)] = 1
    async with MongoDBConnectionManager() as db:
        cursor = (
            db[local_COLLECTION]
            .find(
                {"training_date": {"$gte": fecha_inicio, "$lte": fecha_fin}},
                output,
            )
            .sort("training_date", 1)
        )
        return await cursor.to_list(400)


# Obtiene fechas validas
async def get_fechas_training(date_inicio, date_fin) -> list[datetime]:
    # Esta funcion es basicamente para tener datos limpios en el frontEnd
    if date_fin is None or date_inicio is None:
        if date_fin is None:
            date_fin = datetime.today()
        if date_inicio is None:
            date_inicio = date_fin - timedelta(days=30)

    async with MongoDBConnectionManager() as db:
        cursor = (
            db[local_COLLECTION]
            .find(
                {"training_date": {"$gte": date_inicio, "$lte": date_fin}},
                {"training_date": 1, "_id": 0},
            )
            .sort("training_date", 1)
        )
        date_list, lista_iterable = (
            [],
            await cursor.to_list(
                1000
            ),  # COMO QUE PUEDO METER UN AWAIT ASI WTF FUNCIONA¿¿¿¿
        )
        for date in lista_iterable:
            date_list.append(date["training_date"])

        return date_list
