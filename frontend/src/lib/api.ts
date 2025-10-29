export interface CarbonCalculationRequest {
  geometry: GeoJSON.FeatureCollection<GeoJSON.Polygon>;
}

export async function calculateCarbon(
  request: CarbonCalculationRequest,
  apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000"
) {
  const response = await fetch(`${apiBaseUrl}/calculate_carbon`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    throw new Error(`Failed to calculate carbon: ${response.status}`);
  }

  return response.json();
}
