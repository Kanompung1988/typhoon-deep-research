"""Utility helpers for working with GeoJSON geometries."""

from __future__ import annotations

from typing import Any, Dict

import geopandas as gpd
from shapely.geometry import shape


def geojson_area_hectares(geometry: Dict[str, Any]) -> float:
  """Return the area of a GeoJSON geometry in hectares.

  Args:
      geometry: A GeoJSON FeatureCollection or geometry dictionary.

  Returns:
      The area in hectares.

  Notes:
      Uses GeoPandas to project the geometry to an equal-area CRS (World Cylindrical Equal Area).
  """

  if "type" not in geometry:
    raise ValueError("Invalid GeoJSON: missing type field")

  if geometry["type"] == "FeatureCollection":
    if not geometry.get("features"):
      raise ValueError("FeatureCollection must contain at least one feature")
    geom = shape(geometry["features"][0]["geometry"])
  elif geometry["type"] == "Feature":
    geom = shape(geometry["geometry"])
  else:
    geom = shape(geometry)

  gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326").to_crs("EPSG:6933")
  area_sq_m = float(gdf.area.iloc[0])
  return area_sq_m / 10_000


__all__ = ["geojson_area_hectares"]
