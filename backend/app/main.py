from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Monitoramento ETE API", version="0.2.0")

READINGS: list[dict] = []

class Reading(BaseModel):
    device_id: str = Field(min_length=1, max_length=64)
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
    firmware_version: Optional[str] = None

class AlertThresholds(BaseModel):
    ph_min: Optional[float] = None
    ph_max: Optional[float] = None
    turbidity_max_ntu: Optional[float] = None
    conductivity_max_us_cm: Optional[float] = None
    temperature_max_c: Optional[float] = None
    dissolved_oxygen_min_mg_l: Optional[float] = None

DEFAULT_THRESHOLDS = AlertThresholds()


def evaluate_alerts(reading: dict, thresholds: AlertThresholds) -> list[dict]:
    """Generate monitoring alerts only; never labels regulatory compliance."""
    alerts = []
    checks = [
        ("ph_min", "ph", "below_min", lambda v, t: v < t),
        ("ph_max", "ph", "above_max", lambda v, t: v > t),
        ("turbidity_max_ntu", "turbidity_ntu", "above_max", lambda v, t: v > t),
        ("conductivity_max_us_cm", "conductivity_us_cm", "above_max", lambda v, t: v > t),
        ("temperature_max_c", "temperature_c", "above_max", lambda v, t: v > t),
        ("dissolved_oxygen_min_mg_l", "dissolved_oxygen_mg_l", "below_min", lambda v, t: v < t),
    ]
    for threshold_name, field, kind, predicate in checks:
        value = reading.get(field)
        threshold = getattr(thresholds, threshold_name)
        if value is not None and threshold is not None and predicate(value, threshold):
            alerts.append({"parameter": field, "kind": kind, "value": value, "threshold": threshold})
    return alerts


@app.get("/health")
def health():
    return {"status": "ok", "service": "monitoramento-ete-api", "readings": len(READINGS)}


@app.post("/api/v1/readings", status_code=201)
def create_reading(reading: Reading):
    data = reading.model_dump()
    data["timestamp"] = data["timestamp"] or datetime.now(timezone.utc)
    data["alerts"] = evaluate_alerts(data, DEFAULT_THRESHOLDS)
    READINGS.append(data)
    # TODO: persistir em PostgreSQL/TimescaleDB antes do uso em campo.
    return {"accepted": True, "reading": data}


@app.get("/api/v1/readings")
def list_readings(limit: int = Query(default=100, ge=1, le=1000)):
    return READINGS[-limit:]


@app.get("/api/v1/latest")
def latest():
    return READINGS[-1] if READINGS else None


@app.get("/api/v1/alerts")
def alerts(limit: int = Query(default=100, ge=1, le=1000)):
    result = []
    for reading in READINGS[-limit:]:
        for alert in reading.get("alerts", []):
            result.append({"timestamp": reading["timestamp"], "device_id": reading["device_id"], **alert})
    return result[-1000:]
