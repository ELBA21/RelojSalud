from fastapi import APIRouter, HTTPException, status
from app.models.trainings import Workout
from app.services.trainings import (
    import_training,
    create_training,
    get_training_of_the_day,
)
from datetime import datetime

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
