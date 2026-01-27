from typing import Any
from bson import ObjectId
from fastapi import HTTPException, status


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
