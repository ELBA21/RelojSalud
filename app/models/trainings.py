from pydantic import BaseModel, Field, AliasChoices
from typing import Optional
from datetime import datetime, time


# Definimos la estructura base de una métrica (la pieza que se repita)
class Metric(BaseModel):
    unit: str
    value: float


# Definimos la estructura de las zonas de ritmo cardíaco
class HRZone(Metric):
    type: str
    color: int
    progress: int


class Workout_libre(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    activeSeconds: Metric
    averageHR: Metric
    maxHR: Metric
    minHR: Optional[Metric] = None

    calories: Metric = Field(
        validation_alias=AliasChoices("active_calories", "caloriesBurnt")
    )

    # Zona de HR
    hrZoneNa: HRZone
    hrZoneWarmUp: HRZone
    hrZoneFatBurn: HRZone
    hrZoneAerobic: HRZone
    hrZoneAnaerobic: HRZone
    hrZoneExtreme: HRZone

    # Efectos finales
    aerobicTrainingEffect: Metric
    anaerobicTrainingEffect: Optional[Metric] = None
    currentWorkoutLoad: Metric
    training_type: str = "libre"

    class Config:
        # Esto permite que si envías el JSON tal cual, Pydantic lo entienda
        populate_by_name = True


# El modelo principal que representa todo el JSON
class Workout_trote(Workout_libre):
    maxCadence: Metric
    averageCadence: Metric
    averageStride: Metric
    steps: Metric
    distanceMeters: Metric
    maxPace: Metric
    averageKMPaceSeconds: Metric

    baseAltitude: Optional[Metric] = None
    maximumOxygenUptake: Optional[Metric] = None

    gpx_path: Optional[str] = None


class Workout_summary(BaseModel):
    total_workout: int
    total_calories: int
    total_time: int  # Segundos quiza
    first_date: datetime
    last_date: datetime
    workout_count: dict[str, int]
