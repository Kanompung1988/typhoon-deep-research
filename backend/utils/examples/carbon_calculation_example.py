"""Runnable example demonstrating carbon credit estimation."""

from __future__ import annotations

import json
from pathlib import Path

from backend.utils.carbon import estimate_carbon_from_indices


if __name__ == "__main__":
  ndvi_series = [0.62, 0.64, 0.60, 0.59, 0.63]
  area_hectares = 150.0

  estimation = estimate_carbon_from_indices(
    ndvi_series,
    area_hectares,
    biomass_coefficients=(175.0, 30.0),
    baseline_degradation_rate=0.02,
  )

  result = {
    "biomass_tonnes": round(estimation.biomass, 2),
    "carbon_stock_tonnes": round(estimation.carbon_stock, 2),
    "co2e_tonnes": round(estimation.co2e, 2),
    "credits_per_year": round(estimation.credits, 2),
    "metadata": estimation.metadata,
  }

  output_path = Path(__file__).parent / "carbon_estimate.json"
  output_path.write_text(json.dumps(result, indent=2))
  print(f"Wrote example estimation to {output_path}")
