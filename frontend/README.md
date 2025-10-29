# CarbonEye Agent Frontend

This folder contains a minimal **Next.js 14** prototype with **Leaflet** map tooling for the CarbonEye Agent. It enables
users to digitise a project area, export it as GeoJSON, and call the backend carbon accounting API.

## Key features

- Leaflet map with drawing controls (polygon + rectangle)
- Client-side GeoJSON state management and POST request to the backend
- Result panel surfacing biomass/carbon/credit metrics and metadata
- Modular component structure that can scale into a dashboard

## Getting started

```bash
cd frontend
npm install
npm run dev
```

The app assumes the backend FastAPI server runs on `http://localhost:8000`. Override this by setting
`NEXT_PUBLIC_API_BASE_URL` in a `.env.local` file.

## Directory structure

```
frontend/
├── package.json
├── next.config.mjs
├── src/
│   ├── app/page.tsx          # Marketing copy + map component
│   ├── components/CarbonMap.tsx
│   └── lib/api.ts            # Shared fetch helper
└── README.md
```

## TODOs

- [ ] Add authentication and project management UI
- [ ] Support uploading existing shapefiles/GeoJSON files
- [ ] Integrate charts for time-series NDVI/EVI visualisation
- [ ] Persist map state and recent analyses
