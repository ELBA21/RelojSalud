from fastapi import APIRouter, HTTPException, status, Query
from typing import Annotated
from app.models.trainings import Workout_trote
from app.services.trainings import (
    import_training,
    create_training,
    get_training_of_the_day,
    get_stats_list,
    get_fechas_training,
)
from datetime import datetime

router = APIRouter(prefix="/training", tags=["training"])


@router.post("_test", response_model=Workout_trote, status_code=status.HTTP_201_CREATED)
async def create_training_router(payload: Workout_trote):
    result = await create_training(payload)
    if not result:
        raise HTTPException(500, "No se pudo crear el entrenamiento")

    return result


@router.post(
    "/by_path", response_model=Workout_trote, status_code=status.HTTP_201_CREATED
)
async def import_training_router(training_path: str):
    result = await import_training(training_path)

    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result


@router.get("/daily", response_model=Workout_trote)
async def get_training_of_the_day_router(date: datetime) -> dict:
    result = await get_training_of_the_day(date)

    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result


@router.get("/get_list")
async def get_stats_lists_router(
    fecha_inicio: datetime = Query(example="2026-01-01"),
    fecha_fin: datetime = Query(example="2026-02-01"),
    parametros: list[str] = Query(
        default=[], example=["averageHR", "maxHR"], description="String de parametro"
    ),
):
    result = await get_stats_list(fecha_inicio, fecha_fin, parametros)
    if not result:
        raise HTTPException(500, "No se concreta la accion")
    return result
