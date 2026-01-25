from pydantic import BaseModel, Field
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
    created_at: datetime = Field(default_factory=datetime.now)
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
    caloriesBurnt: Metric
    # Zonas de HR
    hrZoneNa: HRZone
    hrZoneWarmUp: HRZone
    hrZoneFatBurn: HRZone
    hrZoneAerobic: HRZone
    hrZoneAnaerobic: HRZone
    hrZoneExtreme: HRZone
    # Efectos finales
    aerobicTrainingEffect: Metric
    currentWorkoutLoad: Metric

    class Config:
        # Esto permite que si envías el JSON tal cual, Pydantic lo entienda
        populate_by_name = True
