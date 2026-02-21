from app.models.trainings import Workout
from app.database import MongoDBConnectionManager
from app.services.utils import load_json_from_path, to_out, get_gpx_path
from datetime import datetime, timedelta

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

    # averageKMPaceSeconds: Metric


async def get_stats_list(
    date_inicio: datetime | None = None,
    date_fin: datetime | None = None,
    activeSeconds: bool = False,
    averageHR: bool = False,
    maxHR: bool = False,
    minHR: bool = False,
    maxCadence: bool = False,
    averageCadence: bool = False,
    averageStride: bool = False,
    steps: bool = False,
    distanceMeters: bool = False,
    averageKMPaceSeconds: bool = False,
    calories: bool = False,
    baseAltitude: bool = False,
    hrZoneNa: bool = False,
    hrZoneWarmUp: bool = False,
    hrZoneFatBurn: bool = False,
    hrZoneAerobic: bool = False,
    hrZoneAnaerobic: bool = False,
    hrZoneExtreme: bool = False,
    aerobicTrainingEffect: bool = False,
    anaerobicTrainingEffect: bool = False,
    currentWorkoutLoad: bool = False,
    maximumOxygenUptake: bool = False,
    gpx_path: bool = False,
) -> list[dict]:
    retornoDeDatos = {"training_date": 1, "_id": 0}
    # Vale suena tonto, pero mongoDB solo trabaja con inclusion o exclusion,Entonces debo pasar todo lo que quiera a un objeto y entregar los 1
    # Entonces asumiria que todo lo que no es, no lo quiero, Pero no puedo ir poniendo 1 y 0 asi como asi, pq solo es inclusion o exclusion, no ambos
    # Aparentemente la unica excepcion es "_id": 0
    if activeSeconds:
        retornoDeDatos["activeSeconds"] = 1
    if averageHR:
        retornoDeDatos["averageHR"] = 1
    if maxHR:
        retornoDeDatos["maxHR"] = 1
    if minHR:
        retornoDeDatos["minHR"] = 1
    if maxCadence:
        retornoDeDatos["maxCadence"] = 1
    if averageCadence:
        retornoDeDatos["averageCadence"] = 1
    if averageStride:
        retornoDeDatos["averageStride"] = 1
    if steps:
        retornoDeDatos["steps"] = 1
    if distanceMeters:
        retornoDeDatos["distanceMeters"] = 1
    if averageKMPaceSeconds:
        retornoDeDatos["averageKMPaceSeconds"] = 1
    if calories:
        retornoDeDatos["calories"] = 1
    if baseAltitude:
        retornoDeDatos["baseAltitude"] = 1
    if hrZoneNa:
        retornoDeDatos["hrZoneNa"] = 1
    if hrZoneWarmUp:
        retornoDeDatos["hrZoneWarmUp"] = 1
    if hrZoneFatBurn:
        retornoDeDatos["hrZoneFatBurn"] = 1
    if hrZoneAerobic:
        retornoDeDatos["hrZoneAerobic"] = 1
    if hrZoneAnaerobic:
        retornoDeDatos["hrZoneAnaerobic"] = 1
    if hrZoneExtreme:
        retornoDeDatos["hrZoneExtreme"] = 1
    if aerobicTrainingEffect:
        retornoDeDatos["aerobicTrainingEffect"] = 1
    if anaerobicTrainingEffect:
        retornoDeDatos["anaerobicTrainingEffect"] = 1
    if currentWorkoutLoad:
        retornoDeDatos["currentWorkoutLoad"] = 1
    if maximumOxygenUptake:
        retornoDeDatos["maximumOxygenUptake"] = 1
    if gpx_path:
        retornoDeDatos["gpx_path"] = 1
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
                retornoDeDatos,
            )
            .sort("training_date", 1)
        )
        return await cursor.to_list(1000)


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
