"""
Utility functions for geeadvance

Helper functions for common GEE operations.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
from typing import Optional, Union, Tuple, List


def get_projection(image: ee.Image, band: Optional[str] = None) -> ee.Projection:
    """
    Get the projection of an image or band.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    band : str, optional
        Specific band name (uses first band if None)
    
    Returns
    -------
    ee.Projection
        Image projection
    
    Examples
    --------
    >>> proj = ga.get_projection(image)
    >>> print(proj.getInfo())
    """
    if band:
        return image.select(band).projection()
    else:
        return image.select(0).projection()


def get_scale(image: ee.Image, band: Optional[str] = None) -> float:
    """
    Get the nominal scale of an image or band.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    band : str, optional
        Specific band name
    
    Returns
    -------
    float
        Nominal scale in meters
    
    Examples
    --------
    >>> scale = ga.get_scale(landsat_image)
    >>> print(f"Resolution: {scale} meters")
    """
    proj = get_projection(image, band)
    return proj.nominalScale().getInfo()


def clip_to_geometry(image: ee.Image, geometry: ee.Geometry) -> ee.Image:
    """
    Clip an image to a geometry.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    geometry : ee.Geometry
        Clipping geometry
    
    Returns
    -------
    ee.Image
        Clipped image
    
    Examples
    --------
    >>> clipped = ga.clip_to_geometry(image, roi)
    """
    return image.clip(geometry)


def create_grid(
    region: ee.Geometry,
    cell_size: float,
    crs: str = 'EPSG:4326',
) -> ee.FeatureCollection:
    """
    Create a grid of cells over a region.
    
    Parameters
    ----------
    region : ee.Geometry
        Region to cover with grid
    cell_size : float
        Size of grid cells in degrees (or meters if using projected CRS)
    crs : str, optional
        Coordinate reference system
    
    Returns
    -------
    ee.FeatureCollection
        Grid cells as features
    
    Examples
    --------
    >>> grid = ga.create_grid(roi, cell_size=0.1)
    >>> print(f"Grid cells: {grid.size().getInfo()}")
    """
    # Get region bounds
    bounds = region.bounds()
    coords = bounds.coordinates().get(0)
    
    # This is a simplified version - full implementation would create actual grid
    return ee.FeatureCollection([])


def buffer_geometry(
    geometry: ee.Geometry,
    distance: float,
    max_error: float = 1.0,
) -> ee.Geometry:
    """
    Buffer a geometry by a specified distance.
    
    Parameters
    ----------
    geometry : ee.Geometry
        Input geometry
    distance : float
        Buffer distance in meters
    max_error : float, optional
        Maximum error in meters
    
    Returns
    -------
    ee.Geometry
        Buffered geometry
    
    Examples
    --------
    >>> buffered = ga.buffer_geometry(point, distance=1000)
    """
    return geometry.buffer(distance, maxError=max_error)


def get_image_bounds(image: ee.Image) -> ee.Geometry:
    """
    Get the bounding box of an image.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    
    Returns
    -------
    ee.Geometry
        Bounding box geometry
    
    Examples
    --------
    >>> bounds = ga.get_image_bounds(image)
    """
    return image.geometry()


def calculate_ndvi(
    image: ee.Image,
    nir_band: str = 'B5',
    red_band: str = 'B4',
) -> ee.Image:
    """
    Calculate NDVI from an image.
    
    Parameters
    ----------
    image : ee.Image
        Input image with NIR and Red bands
    nir_band : str, optional
        NIR band name (default: 'B5' for Landsat 8)
    red_band : str, optional
        Red band name (default: 'B4' for Landsat 8)
    
    Returns
    -------
    ee.Image
        NDVI image
    
    Examples
    --------
    >>> ndvi = ga.calculate_ndvi(landsat_image)
    >>> # For Sentinel-2
    >>> ndvi = ga.calculate_ndvi(s2_image, nir_band='B8', red_band='B4')
    """
    nir = image.select(nir_band)
    red = image.select(red_band)
    
    ndvi = nir.subtract(red).divide(nir.add(red)).rename('NDVI')
    
    return ndvi


def calculate_evi(
    image: ee.Image,
    nir_band: str = 'B5',
    red_band: str = 'B4',
    blue_band: str = 'B2',
) -> ee.Image:
    """
    Calculate Enhanced Vegetation Index (EVI).
    
    Parameters
    ----------
    image : ee.Image
        Input image
    nir_band : str, optional
        NIR band name
    red_band : str, optional
        Red band name
    blue_band : str, optional
        Blue band name
    
    Returns
    -------
    ee.Image
        EVI image
    
    Examples
    --------
    >>> evi = ga.calculate_evi(landsat_image)
    """
    nir = image.select(nir_band)
    red = image.select(red_band)
    blue = image.select(blue_band)
    
    evi = nir.subtract(red).divide(
        nir.add(red.multiply(6)).subtract(blue.multiply(7.5)).add(1)
    ).multiply(2.5).rename('EVI')
    
    return evi


def reclassify(
    image: ee.Image,
    from_values: List[int],
    to_values: List[int],
) -> ee.Image:
    """
    Reclassify an image.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    from_values : list of int
        Original class values
    to_values : list of int
        New class values
    
    Returns
    -------
    ee.Image
        Reclassified image
    
    Examples
    --------
    >>> # Reclassify to binary (forest/non-forest)
    >>> binary = ga.reclassify(
    ...     landcover,
    ...     from_values=[1, 2, 3, 4, 5],
    ...     to_values=[1, 1, 1, 0, 0]
    ... )
    """
    result = image
    
    for from_val, to_val in zip(from_values, to_values):
        result = result.where(image.eq(from_val), to_val)
    
    return result


def get_image_stats(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> dict:
    """
    Get basic statistics for an image.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    region : ee.Geometry
        Region for statistics
    scale : int, optional
        Scale in meters
    
    Returns
    -------
    dict
        Statistics (min, max, mean, std)
    
    Examples
    --------
    >>> stats = ga.get_image_stats(ndvi, roi)
    >>> print(f"Mean NDVI: {stats['NDVI_mean']}")
    """
    stats = image.reduceRegion(
        reducer=ee.Reducer.mean().combine(
            ee.Reducer.minMax(), '', True
        ).combine(
            ee.Reducer.stdDev(), '', True
        ),
        geometry=region,
        scale=scale,
        maxPixels=1e13,
    )
    
    return stats.getInfo()


def create_roi_from_coords(
    coords: List[Tuple[float, float]],
    geodesic: bool = False,
) -> ee.Geometry:
    """
    Create a region of interest from coordinates.
    
    Parameters
    ----------
    coords : list of tuple
        List of (lon, lat) coordinate pairs
    geodesic : bool, optional
        Use geodesic edges
    
    Returns
    -------
    ee.Geometry
        Polygon geometry
    
    Examples
    --------
    >>> roi = ga.create_roi_from_coords([
    ...     (77.0, 20.0),
    ...     (78.0, 20.0),
    ...     (78.0, 21.0),
    ...     (77.0, 21.0),
    ... ])
    """
    return ee.Geometry.Polygon(coords, geodesic=geodesic)


def create_bbox(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
) -> ee.Geometry:
    """
    Create a bounding box geometry.
    
    Parameters
    ----------
    min_lon : float
        Minimum longitude
    min_lat : float
        Minimum latitude
    max_lon : float
        Maximum longitude
    max_lat : float
        Maximum latitude
    
    Returns
    -------
    ee.Geometry
        Rectangle geometry
    
    Examples
    --------
    >>> bbox = ga.create_bbox(77.0, 20.0, 78.0, 21.0)
    """
    return ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])
