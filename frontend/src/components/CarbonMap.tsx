"use client";

import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";

import { useCallback, useMemo, useState } from "react";
import { FeatureGroup, MapContainer, TileLayer } from "react-leaflet";
import { EditControl } from "react-leaflet-draw";
import L, { LeafletMouseEvent } from "leaflet";
import type { FeatureCollection, Polygon } from "geojson";

interface CarbonMapProps {
  readonly apiBaseUrl?: string;
}

interface CarbonResponse {
  biomass: number;
  carbon_stock: number;
  co2e: number;
  credits: number;
  metadata: Record<string, unknown>;
}

const DEFAULT_CENTER: [number, number] = [0, 0];
const DEFAULT_ZOOM = 4;

export function CarbonMap({ apiBaseUrl = "http://localhost:8000" }: CarbonMapProps) {
  const [geojson, setGeojson] = useState<FeatureCollection<Polygon> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CarbonResponse | null>(null);

  const handleCreated = useCallback((event: L.LeafletEvent) => {
    const layer = (event as unknown as { layer: L.Layer }).layer;
    if (layer instanceof L.Polygon || layer instanceof L.Rectangle) {
      const feature = layer.toGeoJSON() as FeatureCollection<Polygon>;
      setGeojson(feature);
      setResult(null);
      setError(null);
    }
  }, []);

  const handleDeleted = useCallback(() => {
    setGeojson(null);
    setResult(null);
    setError(null);
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!geojson) {
      setError("Draw a polygon before requesting a calculation.");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiBaseUrl}/calculate_carbon`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ geometry: geojson })
      });

      if (!response.ok) {
        throw new Error(`API responded with ${response.status}`);
      }

      const payload: CarbonResponse = await response.json();
      setResult(payload);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setIsLoading(false);
    }
  }, [apiBaseUrl, geojson]);

  const handleClick = useCallback((event: LeafletMouseEvent) => {
    console.debug("Clicked coordinates", event.latlng);
  }, []);

  const editHandlers = useMemo(
    () => ({
      edit: {
        selectedPathOptions: {
          maintainColor: true
        }
      },
      remove: {}
    }),
    []
  );

  return (
    <div className="space-y-4">
      <div className="h-[60vh] w-full rounded-lg border border-slate-200">
        <MapContainer
          center={DEFAULT_CENTER}
          zoom={DEFAULT_ZOOM}
          className="h-full w-full"
          scrollWheelZoom
          whenCreated={(map) => map.on("click", handleClick)}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <FeatureGroup>
            <EditControl
              position="topright"
              onCreated={handleCreated}
              onDeleted={handleDeleted}
              draw={{
                polyline: false,
                circle: false,
                circlemarker: false,
                marker: false,
                polygon: true,
                rectangle: true
              }}
              edit={editHandlers.edit}
              remove={editHandlers.remove}
            />
          </FeatureGroup>
        </MapContainer>
      </div>

      <div className="flex items-center gap-4">
        <button
          type="button"
          onClick={handleSubmit}
          className="rounded bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isLoading}
        >
          {isLoading ? "Calculating…" : "Calculate carbon"}
        </button>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>

      {result && (
        <div className="rounded border border-slate-200 bg-white p-4 shadow-sm">
          <h2 className="text-lg font-semibold">Estimated carbon metrics</h2>
          <ul className="mt-2 space-y-1 text-sm text-slate-700">
            <li><strong>Biomass:</strong> {result.biomass.toLocaleString()} t/ha</li>
            <li><strong>Carbon stock:</strong> {result.carbon_stock.toLocaleString()} t C</li>
            <li><strong>CO₂e:</strong> {result.co2e.toLocaleString()} t CO₂e</li>
            <li><strong>Credits/year:</strong> {result.credits.toLocaleString()} tCO₂e</li>
          </ul>
          <details className="mt-3 text-sm">
            <summary className="cursor-pointer font-medium">Metadata</summary>
            <pre className="mt-2 overflow-x-auto rounded bg-slate-50 p-3 text-xs text-slate-600">
              {JSON.stringify(result.metadata, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
}

export default CarbonMap;
