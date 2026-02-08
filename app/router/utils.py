from typing import Any, Tuple
from bson import ObjectId
from fastapi import HTTPException, status
from app.models.trainings import Workout
import json
from pathlib import Path
from datetime import datetime


def oid(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"ID {id_str} no es formato valido mongoDB",
        )
    return ObjectId(id_str)


def to_out(doc: dict[str, Any]) -> dict[str, Any]:
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id"))
    return doc


def load_json_from_path(file_path: str) -> Tuple[Workout, datetime]:
    print(f"Debug: {file_path}")
    path = Path(file_path)

    # Obtenemos fecha
    nombre = path.stem
    formato = "%Y-%m-%dT%H_%M_%S%z"
    nomre_limpio = nombre[:-3] + nombre[-2:]
    fecha_obj = datetime.strptime(nomre_limpio, formato)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    workout_obj = Workout.model_validate(data)

    return workout_obj, fecha_obj
