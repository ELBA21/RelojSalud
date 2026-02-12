from pydantic import BaseModel, Field, AliasChoices
from typing import Optional
from datetime import datetime


# Definimos la estructura base de una métrica (la pieza que se repita)
class Metric(BaseModel):
    unit: str
    value: float


# Definimos la estructura de las zonas de ritmo cardíaco
class HRZone(Metric):
    type: str
    color: int
    progress: int


# El modelo principal que representa todo el JSON
class Workout(BaseModel):
    # Datos poblados por el pydantic
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    # Datos generales del reloj
    activeSeconds: Metric
    averageHR: Metric
    maxHR: Metric
    minHR: Optional[Metric] = None
    maxCadence: Metric
    averageCadence: Metric
    averageStride: Metric
    steps: Metric
    distanceMeters: Metric
    maxPace: Metric
    averageKMPaceSeconds: Metric

    calories: Metric = Field(
        validation_alias=AliasChoices("active_calories", "caloriesBurnt")
    )
    baseAltitude: Optional[Metric] = None
    # Zonas de HR
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
    maximumOxygenUptake: Optional[Metric] = None

    gpx_path: Optional[str] = None

    class Config:
        # Esto permite que si envías el JSON tal cual, Pydantic lo entienda
        populate_by_name = True
