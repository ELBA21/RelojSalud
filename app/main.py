from fastapi import FastAPI
from app.router import healthcheck


app = FastAPI(title="Salud")

app.include_router(healthcheck.router)
app.include_router(healthcheck.router, prefix="/api/v1")


@app.get("/")
def chekee():
    return {"status": "de pana banana"}
