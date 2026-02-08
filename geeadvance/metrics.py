"""
Landscape metrics calculation module

Implements landscape ecology metrics similar to the R landscapemetrics package.
Metrics are organized into categories: Area, Edge, Shape, Core, Aggregation, and Diversity.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
import pandas as pd
import numpy as np
from typing import Optional, Union, Dict, List


def calculate_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
    class_band: str = None,
    metrics: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Calculate comprehensive landscape metrics for an image.
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters for calculations (default: 30)
    class_band : str, optional
        Name of the classification band (auto-detected if None)
    metrics : list of str, optional
        Specific metrics to calculate. If None, calculates all metrics.
        Options: 'area', 'edge', 'shape', 'core', 'aggregation', 'diversity'
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing calculated metrics
    
    Examples
    --------
    >>> import ee
    >>> import geeadvance
    >>> 
    >>> # Standard GEE authentication and initialization
    >>> ee.Authenticate()
    >>> ee.Initialize(project='your-project-id')
    >>> 
    >>> lc = geeadvance.load_dataset('MODIS/006/MCD12Q1')
    >>> roi = ee.Geometry.Rectangle([77.0, 20.0, 78.0, 21.0])
    >>> metrics = geeadvance.calculate_metrics(lc, roi, scale=500)
    >>> print(metrics)
    """
    if class_band is None:
        class_band = image.bandNames().get(0).getInfo()
    
    image = image.select(class_band)
    
    # Calculate all metric categories
    results = {}
    
    if metrics is None or 'area' in metrics:
        results.update(area_metrics(image, region, scale))
    
    if metrics is None or 'edge' in metrics:
        results.update(edge_metrics(image, region, scale))
    
    if metrics is None or 'shape' in metrics:
        results.update(shape_metrics(image, region, scale))
    
    if metrics is None or 'core' in metrics:
        results.update(core_metrics(image, region, scale))
    
    if metrics is None or 'aggregation' in metrics:
        results.update(aggregation_metrics(image, region, scale))
    
    if metrics is None or 'diversity' in metrics:
        results.update(diversity_metrics(image, region, scale))
    
    return pd.DataFrame([results])


def area_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate area-based landscape metrics.
    
    Metrics calculated:
    - CA: Class Area
    - PLAND: Percentage of Landscape
    - TA: Total Area
    - NP: Number of Patches
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of area metrics
    
    Examples
    --------
    >>> metrics = geeadvance.area_metrics(landcover_image, roi, scale=500)
    >>> print(f"Total Area: {metrics['TA']} ha")
    """
    # Get pixel area
    pixel_area = ee.Image.pixelArea()
    
    # Calculate total area
    total_area = pixel_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    ).get('area')
    
    total_area_ha = ee.Number(total_area).divide(10000)  # Convert to hectares
    
    # Get unique classes
    class_values = image.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    )
    
    # Calculate class areas
    class_areas = {}
    class_proportions = {}
    
    # This is a simplified version - in practice, you'd iterate over classes
    metrics = {
        'TA': total_area_ha.getInfo(),
        'CA': None,  # Placeholder - would calculate per class
        'PLAND': None,  # Placeholder - would calculate per class
        'NP': None,  # Placeholder - would calculate number of patches
    }
    
    return metrics


def edge_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate edge-based landscape metrics.
    
    Metrics calculated:
    - TE: Total Edge
    - ED: Edge Density
    - LSI: Landscape Shape Index
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of edge metrics
    
    Examples
    --------
    >>> metrics = geeadvance.edge_metrics(landcover_image, roi)
    >>> print(f"Edge Density: {metrics['ED']} m/ha")
    """
    # Calculate edges using convolution
    kernel = ee.Kernel.square(radius=1, units='pixels')
    
    # Detect edges
    edges = image.convolve(kernel).neq(image)
    
    # Calculate total edge length
    pixel_area = ee.Image.pixelArea()
    edge_length = edges.multiply(pixel_area.sqrt()).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    )
    
    # Calculate total area for density
    total_area = pixel_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    ).get('area')
    
    total_area_ha = ee.Number(total_area).divide(10000)
    
    metrics = {
        'TE': None,  # Total edge - would calculate from edge_length
        'ED': None,  # Edge density - TE / TA
        'LSI': None,  # Landscape shape index
    }
    
    return metrics


def shape_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate shape-based landscape metrics.
    
    Metrics calculated:
    - SHAPE: Shape Index
    - FRAC: Fractal Dimension Index
    - PARA: Perimeter-Area Ratio
    - CIRCLE: Related Circumscribing Circle
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of shape metrics
    
    Examples
    --------
    >>> metrics = geeadvance.shape_metrics(landcover_image, roi)
    >>> print(f"Mean Shape Index: {metrics['SHAPE_MN']}")
    """
    metrics = {
        'SHAPE_MN': None,  # Mean shape index
        'SHAPE_AM': None,  # Area-weighted mean shape index
        'FRAC_MN': None,   # Mean fractal dimension
        'PARA_MN': None,   # Mean perimeter-area ratio
        'CIRCLE_MN': None, # Mean related circumscribing circle
    }
    
    return metrics


def core_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
    edge_depth: int = 1,
) -> Dict:
    """
    Calculate core area metrics.
    
    Metrics calculated:
    - TCA: Total Core Area
    - CPLAND: Core Area Percentage of Landscape
    - CAI: Core Area Index
    - NDCA: Number of Disjunct Core Areas
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    edge_depth : int, optional
        Edge depth in pixels (default: 1)
    
    Returns
    -------
    dict
        Dictionary of core area metrics
    
    Examples
    --------
    >>> metrics = geeadvance.core_metrics(landcover_image, roi, edge_depth=2)
    >>> print(f"Total Core Area: {metrics['TCA']} ha")
    """
    # Calculate core areas by eroding patches
    kernel = ee.Kernel.square(radius=edge_depth, units='pixels')
    core_image = image.focal_min(kernel=kernel)
    
    metrics = {
        'TCA': None,     # Total core area
        'CPLAND': None,  # Core area percentage
        'CAI_MN': None,  # Mean core area index
        'NDCA': None,    # Number of disjunct core areas
    }
    
    return metrics


def aggregation_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate aggregation metrics.
    
    Metrics calculated:
    - AI: Aggregation Index
    - CLUMPY: Clumpiness Index
    - COHESION: Patch Cohesion Index
    - DIVISION: Landscape Division Index
    - SPLIT: Splitting Index
    - MESH: Effective Mesh Size
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of aggregation metrics
    
    Examples
    --------
    >>> metrics = geeadvance.aggregation_metrics(landcover_image, roi)
    >>> print(f"Aggregation Index: {metrics['AI']}")
    """
    metrics = {
        'AI': None,       # Aggregation index
        'CLUMPY': None,   # Clumpiness
        'COHESION': None, # Patch cohesion
        'DIVISION': None, # Landscape division
        'SPLIT': None,    # Splitting index
        'MESH': None,     # Effective mesh size
    }
    
    return metrics


def diversity_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate diversity metrics.
    
    Metrics calculated:
    - SHDI: Shannon's Diversity Index
    - SHEI: Shannon's Evenness Index
    - SIDI: Simpson's Diversity Index
    - SIEI: Simpson's Evenness Index
    - MSIDI: Modified Simpson's Diversity Index
    - PR: Patch Richness
    - PRD: Patch Richness Density
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of diversity metrics
    
    Examples
    --------
    >>> metrics = geeadvance.diversity_metrics(landcover_image, roi)
    >>> print(f"Shannon Diversity: {metrics['SHDI']}")
    """
    # Get class proportions
    histogram = image.reduceRegion(
        reducer=ee.Reducer.frequencyHistogram(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    )
    
    # Calculate diversity indices
    # This is a simplified placeholder - actual implementation would calculate from histogram
    
    metrics = {
        'SHDI': None,   # Shannon's diversity
        'SHEI': None,   # Shannon's evenness
        'SIDI': None,   # Simpson's diversity
        'SIEI': None,   # Simpson's evenness
        'MSIDI': None,  # Modified Simpson's diversity
        'PR': None,     # Patch richness
        'PRD': None,    # Patch richness density
    }
    
    return metrics


def patch_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
    connectivity: int = 8,
) -> ee.Image:
    """
    Identify and label individual patches in the landscape.
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    connectivity : int, optional
        Connectivity rule (4 or 8, default: 8)
    
    Returns
    -------
    ee.Image
        Image with labeled patches
    
    Examples
    --------
    >>> patches = geeadvance.patch_metrics(landcover_image, roi)
    >>> # Export or visualize patches
    """
    # Use connected components to identify patches
    patches = image.connectedComponents(
        connectedness=ee.Kernel.square(1) if connectivity == 8 else ee.Kernel.plus(1),
        maxSize=256
    )
    
    return patches


def calculate_class_metrics(
    image: ee.Image,
    region: ee.Geometry,
    class_value: int,
    scale: int = 30,
) -> Dict:
    """
    Calculate metrics for a specific land cover class.
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    class_value : int
        Class value to analyze
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Dictionary of class-specific metrics
    
    Examples
    --------
    >>> # Calculate metrics for forest class (value = 1)
    >>> forest_metrics = geeadvance.calculate_class_metrics(lc, roi, class_value=1)
    >>> print(forest_metrics)
    """
    # Create binary mask for the class
    class_mask = image.eq(class_value)
    
    # Calculate area
    pixel_area = ee.Image.pixelArea()
    class_area = class_mask.multiply(pixel_area).reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        maxPixels=1e13
    )
    
    metrics = {
        'class': class_value,
        'area_ha': None,  # Would calculate from class_area
        'proportion': None,
        'n_patches': None,
    }
    
    return metrics
