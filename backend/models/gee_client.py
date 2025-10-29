"""Google Earth Engine integration layer.

This module wraps the Earth Engine client. It is intentionally light-weight and contains TODOs where
project-specific logic should be implemented."""

from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List


class EarthEngineClient:
  """Facade over the Google Earth Engine Python API."""

  def __init__(self, *, project: str | None = None):
    self.project = project
    # TODO: initialise ee.Authenticate() / ee.Initialize(project=project)

  def fetch_ndvi_series(
    self,
    geometry: Dict[str, Any],
    start_date: dt.date,
    end_date: dt.date,
    dataset: str = "COPERNICUS/S2_SR",
  ) -> List[float]:
    """Return NDVI measurements for the provided geometry.

    This prototype returns mocked values. Replace with Earth Engine reducers.
    """

    # TODO: Use ee.ImageCollection(dataset).filterDate(...).filterBounds(...)
    #       .map(cloud_mask).map(calculate_ndvi) and reduceRegion/reduceColumns
    _ = (geometry, start_date, end_date, dataset)
    return [0.62, 0.65, 0.61, 0.58]

  def fetch_biomass_raster(self, geometry: Dict[str, Any], dataset: str = "ESA/BIOMASS/ALBE/V1") -> float:
    """Sample biomass raster to approximate AGB in t/ha.

    TODO: Implement ee.Image(dataset).sample()
    """

    _ = (geometry, dataset)
    return 130.0


__all__ = ["EarthEngineClient"]
