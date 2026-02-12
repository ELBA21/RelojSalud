from typing import Tuple, Any
from app.models.trainings import Workout
import json
from pathlib import Path
from datetime import datetime


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


def get_gpx_path(file_path: str) -> str:
    # Se intenta tomar la ruta padre, ir a la carpeta hermana
    # Y renotrnar ubicacion mas cercana
    nombre = Path(file_path).stem
    # print(f"test: {nombre}")
    gpx_folder = Path(file_path).parent.parent / "GPX_Entrenamiento"
    # print(gpx_folder)
    resultados = list(gpx_folder.glob(f"gadgetbridge-track-{nombre}.gpx"))
    if resultados:
        # print(f"archivo encontrado {resultados[0]}")
        archivo = str(resultados[0])
    else:
        # print("No se encontro archivo")
        archivo = "olaNuro"
    # print(f"ruta absolita para \n {archivo}")
    return archivo
