# CarbonEye Agent Backend

A FastAPI prototype that accepts GeoJSON geometries, orchestrates Google Earth Engine (GEE) calls, estimates biomass via
AI/ML rules, and exposes reporting endpoints. The implementation is modular to support future integration with
LLM-driven methodology selection and carbon credit registries (e.g., Verra, T-VER).

## Running locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Key modules

- `backend/main.py` — FastAPI app with `/calculate_carbon`, `/report/{job_id}`, `/health`
- `backend/models/gee_client.py` — Earth Engine wrapper (mocked values with TODOs)
- `backend/models/biomass_model.py` — Model selection + NDVI→biomass helpers
- `backend/utils/carbon.py` — Conversion utilities and example carbon credit estimator
- `backend/utils/geo.py` — GeoJSON area calculation using GeoPandas/Shapely
- `backend/utils/reporting.py` — PDF report generator using ReportLab
- `backend/agent/` — Prompt templates for the methodology LLM agent

## Data flow (prototype)

1. Frontend submits GeoJSON via `/calculate_carbon`
2. Backend validates geometry and computes area (ha)
3. Google Earth Engine client fetches NDVI/EVI + biomass rasters (mocked here)
4. LLM/heuristics select biomass model coefficients (Tier 2 defaults)
5. `estimate_carbon_from_indices` converts NDVI → biomass → carbon → CO₂e → credits
6. Response cached and persisted as JSON; PDF report available at `/report/{job_id}?format=pdf`

## Assumptions & limitations

- Earth Engine integration returns mocked values; authentication + reducers must be implemented
- Biomass conversion uses linear regression; calibrate with field plots / local allometric equations
- Baseline deforestation rate fixed at 2% annually; replace with scenario modelling per standard
- GeoPandas reprojects to EPSG:6933; ensure geometry boundaries fall within projection limits
- ReportLab dependency is optional; switch to FPDF/WeasyPrint if preferred
- No persistent database yet; replace in-memory cache with PostGIS + ledger integration

## TODOs

- [ ] Implement async Earth Engine data access with retries and cloud masking
- [ ] Integrate LLM agent to reason about dataset/methodology selection
- [ ] Persist job metadata + geometries in PostGIS
- [ ] Add authentication + role-based access
- [ ] Connect to carbon credit registries for verification workflows
