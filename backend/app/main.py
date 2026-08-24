from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Monitoramento ETE API", version="0.1.0")

READINGS: list[dict] = []

class Reading(BaseModel):
    device_id: str
    timestamp: Optional[datetime] = None
    timestamp_ms: Optional[int] = None
    ph: Optional[float] = Field(default=None, ge=0, le=14)
    turbidity_ntu: Optional[float] = Field(default=None, ge=0)
    conductivity_us_cm: Optional[float] = Field(default=None, ge=0)
    temperature_c: Optional[float] = None
    dissolved_oxygen_mg_l: Optional[float] = Field(default=None, ge=0)
    flow_l_min: Optional[float] = Field(default=None, ge=0)
    quality: str = "raw"
    calibration_version: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok", "service": "monitoramento-ete-api"}

@app.post("/api/v1/readings", status_code=201)
def create_reading(reading: Reading):
    data = reading.model_dump()
    data["timestamp"] = data["timestamp"] or datetime.now(timezone.utc)
    READINGS.append(data)
    # TODO: persistir em PostgreSQL/TimescaleDB antes do uso em campo.
    return {"accepted": True, "reading": data}

@app.get("/api/v1/readings")
def list_readings(limit: int = 100):
    return READINGS[-max(1, min(limit, 1000)):]

@app.get("/api/v1/latest")
def latest():
    return READINGS[-1] if READINGS else None
