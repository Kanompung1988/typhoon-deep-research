# CarbonEye Agent — System Diagram

```mermaid
flowchart LR
  subgraph Frontend
    UI[Leaflet Map UI]
    Draw[Polygon Drawing]
  end

  subgraph Backend
    API[FastAPI `/calculate_carbon`]
    Agent[LLM Methodology Agent]
    GEE[Earth Engine Client]
    Model[Biomass/Carbon Model]
    Report[Report Generator]
  end

  subgraph DataStores
    PostGIS[(PostGIS / Spatial DB)]
    Ledger[(Verification Ledger)]
    Reports[(JSON/PDF Reports)]
  end

  UI -->|GeoJSON POST| API
  Draw --> UI
  API -->|Invoke| Agent
  API -->|Request NDVI/EVI| GEE
  GEE -->|Indices & Biomass Layers| Model
  Agent -->|Method config| Model
  Model -->|Biomass/Carbon Metrics| API
  API --> Reports
  API -->|Persist| PostGIS
  Reports --> Ledger
  Reports -->|Download| UI
```

**Data flow summary**

1. Users draw/upload polygons in the Leaflet UI and submit GeoJSON to the API.
2. FastAPI validates geometry, computes area, and coordinates Earth Engine + ML calls.
3. The LLM agent selects methodologies, datasets, and conversion factors.
4. Biomass model converts NDVI/EVI + auxiliary biomass data into carbon stock and CO₂e.
5. Results are cached, persisted, and available via JSON/PDF reports, ready for carbon market verification.
