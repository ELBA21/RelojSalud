from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck", tags=["system"])
def healthcheck():
    return {"status": "online", "version": "0.1.0"}
