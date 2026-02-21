from fastapi import APIRouter, HTTPException, status
from app.models.trainings import Workout
from app.services.trainings import (
    import_training,
    create_training,
    get_training_of_the_day,
    get_stats_list,
    get_fechas_training,
)
from datetime import datetime, timedelta

router = APIRouter(prefix="/training", tags=["training"])


@router.post("_test", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_training_router(payload: Workout):
    result = await create_training(payload)
    if not result:
        raise HTTPException(500, "No se pudo crear el entrenamiento")

    return result


@router.post("/by_path", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def import_training_router(training_path: str):
    result = await import_training(training_path)

    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result


@router.get("/daily", response_model=Workout)
async def get_training_of_the_day_router(date: datetime) -> dict:
    result = await get_training_of_the_day(date)

    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result


@router.get("/get_list")
async def get_stats_list_router(
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
):
    result = await get_stats_list(
        date_inicio,
        date_fin,
        activeSeconds,
        averageHR,
        maxHR,
        minHR,
        maxCadence,
        averageCadence,
        averageStride,
        steps,
        distanceMeters,
        averageKMPaceSeconds,
        calories,
        baseAltitude,
        hrZoneNa,
        hrZoneWarmUp,
        hrZoneFatBurn,
        hrZoneAerobic,
        hrZoneAnaerobic,
        hrZoneExtreme,
        aerobicTrainingEffect,
        anaerobicTrainingEffect,
        currentWorkoutLoad,
        maximumOxygenUptake,
        gpx_path,
    )
    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result


@router.get("/get_fechas_training")
async def get_fechas_training_router(
    date_inicio: datetime | None = None, date_fin: datetime | None = None
):
    result = await get_fechas_training(date_inicio, date_fin)

    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result
