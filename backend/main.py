"""FastAPI backend for the CarbonEye Agent."""

from __future__ import annotations

import datetime as dt
import json
import uuid
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from backend.models.biomass_model import BiomassModelConfig, choose_model
from backend.models.gee_client import EarthEngineClient
from backend.utils.carbon import BiomassEstimation, estimate_carbon_from_indices
from backend.utils.geo import geojson_area_hectares
from backend.utils.reporting import ReportPayload, build_pdf_report

RESULT_CACHE: Dict[str, Dict[str, Any]] = {}
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

app = FastAPI(title="CarbonEye Agent API", version="0.1.0")
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"]
)


class GeometryPayload(BaseModel):
  geometry: Dict[str, Any] = Field(..., description="GeoJSON geometry or FeatureCollection")
  project_name: str = Field("Untitled project")
  start_date: dt.date | None = Field(default=None)
  end_date: dt.date | None = Field(default=None)


class CarbonResult(BaseModel):
  job_id: str
  biomass: float
  carbon_stock: float
  co2e: float
  credits: float
  metadata: Dict[str, Any]


@app.post("/calculate_carbon", response_model=CarbonResult)
async def calculate_carbon(payload: GeometryPayload) -> CarbonResult:
  """Ingest polygon, query GEE + ML, and return carbon metrics."""

  geometry = payload.geometry
  try:
    area_hectares = geojson_area_hectares(geometry)
  except ValueError as exc:
    raise HTTPException(status_code=400, detail=str(exc)) from exc

  client = EarthEngineClient()
  start_date = payload.start_date or (dt.date.today() - dt.timedelta(days=365))
  end_date = payload.end_date or dt.date.today()
  ndvi_series = client.fetch_ndvi_series(geometry, start_date, end_date)

  model_config: BiomassModelConfig = choose_model({
    "region": "tropical",
    "dataset": "Sentinel-2",
    "llm_reasoning": "TODO: Replace with agent call"
  })

  estimation: BiomassEstimation = estimate_carbon_from_indices(
    ndvi_series,
    area_hectares,
    biomass_coefficients=model_config.ndvi_to_biomass_coefficients,
  )

  job_id = uuid.uuid4().hex
  result_payload = {
    "job_id": job_id,
    "biomass": estimation.biomass,
    "carbon_stock": estimation.carbon_stock,
    "co2e": estimation.co2e,
    "credits": estimation.credits,
    "metadata": {
      **estimation.metadata,
      "model": model_config.__dict__,
      "ndvi_series": ndvi_series,
      "start_date": start_date.isoformat(),
      "end_date": end_date.isoformat(),
      "project_name": payload.project_name,
      "area_hectares": area_hectares,
    }
  }

  RESULT_CACHE[job_id] = result_payload
  (REPORTS_DIR / f"{job_id}.json").write_text(json.dumps(result_payload, indent=2))

  return CarbonResult(**result_payload)


@app.get("/report/{job_id}")
async def get_report(job_id: str, format: str = Query("json", pattern="^(json|pdf)$")) -> Response:
  """Return stored report in JSON or PDF format."""

  if job_id not in RESULT_CACHE:
    raise HTTPException(status_code=404, detail="Unknown job id")

  record = RESULT_CACHE[job_id]

  if format == "json":
    return JSONResponse(record)

  payload = ReportPayload(
    job_id=job_id,
    project_name=record["metadata"].get("project_name", "Untitled project"),
    metrics={
      "Biomass (t)": f"{record['biomass']:.2f}",
      "Carbon stock (t C)": f"{record['carbon_stock']:.2f}",
      "CO₂e (t)": f"{record['co2e']:.2f}",
      "Credits/year (tCO₂e)": f"{record['credits']:.2f}",
    },
    metadata=record["metadata"],
  )
  pdf_bytes = build_pdf_report(payload)

  return Response(content=pdf_bytes, media_type="application/pdf")


@app.get("/health")
async def health() -> Dict[str, str]:
  """Health probe for uptime checks."""

  return {"status": "ok"}


@app.get("/")
async def root() -> Dict[str, str]:
  return {"message": "CarbonEye Agent API"}
