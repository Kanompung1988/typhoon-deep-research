"""Machine learning utilities for biomass estimation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass
class BiomassModelConfig:
  name: str
  version: str
  ndvi_to_biomass_coefficients: tuple[float, float]
  source: str


def choose_model(metadata: Dict[str, str]) -> BiomassModelConfig:
  """Pick a biomass model configuration based on metadata.

  In production this should rely on the LLM agent's reasoning. For the prototype we return
  a fixed configuration representing an IPCC Tier 2 linear regression.
  """

  _ = metadata
  return BiomassModelConfig(
    name="ipcc-tier2-linear",
    version="0.1.0",
    ndvi_to_biomass_coefficients=(175.0, 30.0),
    source="Derived from IPCC 2006 guidelines - humid tropical forest default",
  )


def predict_biomass(ndvi_series: List[float], coefficients: tuple[float, float]) -> float:
  """Return biomass per hectare from NDVI observations using linear regression."""

  if not ndvi_series:
    raise ValueError("NDVI series cannot be empty")

  slope, intercept = coefficients
  return float(np.mean(ndvi_series) * slope + intercept)


__all__ = ["BiomassModelConfig", "choose_model", "predict_biomass"]
