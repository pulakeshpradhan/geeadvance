"""
GeeAdvance - Landscape Metrics for Google Earth Engine

A Python package for advanced landscape metrics analysis using Google Earth Engine.
Implements landscape ecology metrics similar to the R landscapemetrics package.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

__version__ = "0.1.0"
__author__ = "Pulakesh Pradhan"
__email__ = "pulakesh.mid@gmail.com"

# Import main modules
from .auth import authenticate, initialize, is_authenticated
from .datasets import load_dataset, list_datasets, get_dataset_info, get_landcover_classes
from .metrics import (
    calculate_metrics,
    area_metrics,
    edge_metrics,
    shape_metrics,
    core_metrics,
    aggregation_metrics,
    diversity_metrics,
)
from .export import export_tif, export_geojson, export_to_drive, export_to_asset
from .download import download_large_area, download_collection, estimate_download_size
from .utils import get_projection, get_scale, clip_to_geometry, create_bbox, calculate_ndvi

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Authentication
    "authenticate",
    "initialize",
    "is_authenticated",
    # Datasets
    "load_dataset",
    "list_datasets",
    "get_dataset_info",
    "get_landcover_classes",
    # Metrics
    "calculate_metrics",
    "area_metrics",
    "edge_metrics",
    "shape_metrics",
    "core_metrics",
    "aggregation_metrics",
    "diversity_metrics",
    # Export
    "export_tif",
    "export_geojson",
    "export_to_drive",
    "export_to_asset",
    # Download (with geemap tiling support)
    "download_large_area",
    "download_collection",
    "estimate_download_size",
    # Utils
    "get_projection",
    "get_scale",
    "clip_to_geometry",
    "create_bbox",
    "calculate_ndvi",
]
