"""Carbon and biomass conversion utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

CARBON_FRACTION = 0.47
CO2E_CONVERSION = 3.67


def biomass_to_carbon(biomass_tonnes: float) -> float:
  """Convert above ground biomass (tonnes) to tonnes of carbon."""

  return biomass_tonnes * CARBON_FRACTION


def carbon_to_co2e(carbon_tonnes: float) -> float:
  """Convert tonnes of carbon to tonnes of CO₂ equivalent."""

  return carbon_tonnes * CO2E_CONVERSION


@dataclass
class BiomassEstimation:
  """Result of biomass estimation."""

  biomass: float
  carbon_stock: float
  co2e: float
  credits: float
  metadata: Dict[str, object]


def estimate_carbon_from_indices(
  ndvi_series: List[float],
  area_hectares: float,
  biomass_coefficients: Tuple[float, float] = (150, 50),
  baseline_degradation_rate: float = 0.02,
) -> BiomassEstimation:
  """Estimate carbon metrics from NDVI observations.

  Args:
      ndvi_series: Historical NDVI values (cloud-filtered).
      area_hectares: Project area in hectares.
      biomass_coefficients: Tuple (slope, intercept) for NDVI→biomass regression (t/ha).
      baseline_degradation_rate: Annual percent biomass loss without intervention.
  """

  if not ndvi_series:
    raise ValueError("NDVI series required for carbon estimation")

  slope, intercept = biomass_coefficients
  ndvi_array = np.array(ndvi_series)
  biomass_per_hectare = slope * ndvi_array.mean() + intercept
  biomass_total = biomass_per_hectare * area_hectares
  carbon_stock = biomass_to_carbon(biomass_total)
  co2e = carbon_to_co2e(carbon_stock)

  avoided_emissions = biomass_total * baseline_degradation_rate
  credits = carbon_to_co2e(biomass_to_carbon(avoided_emissions))

  metadata = {
    "ndvi_mean": float(ndvi_array.mean()),
    "ndvi_observations": len(ndvi_series),
    "biomass_coefficients": {
      "slope": slope,
      "intercept": intercept,
    },
    "baseline_degradation_rate": baseline_degradation_rate,
    "area_hectares": area_hectares,
  }

  return BiomassEstimation(
    biomass=biomass_total,
    carbon_stock=carbon_stock,
    co2e=co2e,
    credits=credits,
    metadata=metadata,
  )


__all__ = [
  "BiomassEstimation",
  "biomass_to_carbon",
  "carbon_to_co2e",
  "estimate_carbon_from_indices",
]
