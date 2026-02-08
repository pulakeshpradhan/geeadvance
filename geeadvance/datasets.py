"""
Dataset loading and management module for Google Earth Engine

Provides utilities for loading, filtering, and managing GEE datasets.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
from typing import Optional, Union, Dict, List
from datetime import datetime


# Common GEE datasets for landscape analysis
COMMON_DATASETS = {
    'landcover': {
        'MODIS_LC': 'MODIS/006/MCD12Q1',
        'ESA_WorldCover': 'ESA/WorldCover/v100',
        'COPERNICUS_LC': 'COPERNICUS/Landcover/100m/Proba-V-C3/Global',
        'USGS_NLCD': 'USGS/NLCD_RELEASES/2019_REL/NLCD',
    },
    'elevation': {
        'SRTM': 'USGS/SRTMGL1_003',
        'ASTER_DEM': 'ASTER/GDEM/DEM_V3',
        'ALOS_DSM': 'JAXA/ALOS/AW3D30/V3_2',
    },
    'vegetation': {
        'MODIS_NDVI': 'MODIS/006/MOD13A2',
        'LANDSAT8_NDVI': 'LANDSAT/LC08/C02/T1_L2',
        'SENTINEL2': 'COPERNICUS/S2_SR',
    },
    'climate': {
        'CHIRPS_PRECIP': 'UCSB-CHG/CHIRPS/DAILY',
        'TERRACLIMATE': 'IDAHO_EPSCOR/TERRACLIMATE',
        'ERA5': 'ECMWF/ERA5/DAILY',
    }
}


def load_dataset(
    dataset_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    region: Optional[ee.Geometry] = None,
    bands: Optional[List[str]] = None,
    filter_clouds: bool = False,
) -> Union[ee.Image, ee.ImageCollection]:
    """
    Load a dataset from Google Earth Engine.
    
    Parameters
    ----------
    dataset_id : str
        GEE dataset ID (e.g., 'MODIS/006/MCD12Q1')
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    region : ee.Geometry, optional
        Region of interest to filter the dataset
    bands : list of str, optional
        Specific bands to select
    filter_clouds : bool, optional
        Whether to apply cloud filtering (for optical imagery)
    
    Returns
    -------
    ee.Image or ee.ImageCollection
        Loaded GEE dataset
    
    Examples
    --------
    >>> import geeadvance as ga
    >>> import ee
    >>> 
    >>> # Load MODIS land cover
    >>> lc = ga.load_dataset('MODIS/006/MCD12Q1', 
    ...                      start_date='2020-01-01',
    ...                      end_date='2020-12-31')
    >>> 
    >>> # Load with region filter
    >>> roi = ee.Geometry.Rectangle([77.0, 20.0, 78.0, 21.0])
    >>> lc = ga.load_dataset('MODIS/006/MCD12Q1', region=roi)
    """
    try:
        # Load the dataset
        dataset = ee.ImageCollection(dataset_id)
        
        # Apply date filter if provided
        if start_date and end_date:
            dataset = dataset.filterDate(start_date, end_date)
        
        # Apply region filter if provided
        if region:
            dataset = dataset.filterBounds(region)
        
        # Apply cloud filtering if requested
        if filter_clouds:
            dataset = _apply_cloud_mask(dataset, dataset_id)
        
        # Select specific bands if provided
        if bands:
            dataset = dataset.select(bands)
        
        # Return single image if collection has only one image
        size = dataset.size().getInfo()
        if size == 1:
            return dataset.first()
        
        return dataset
        
    except Exception as e:
        # Try loading as single image
        try:
            image = ee.Image(dataset_id)
            if bands:
                image = image.select(bands)
            if region:
                image = image.clip(region)
            return image
        except:
            raise ValueError(f"Failed to load dataset '{dataset_id}': {str(e)}")


def _apply_cloud_mask(collection: ee.ImageCollection, dataset_id: str) -> ee.ImageCollection:
    """Apply cloud masking based on dataset type."""
    
    if 'LANDSAT' in dataset_id.upper():
        def mask_landsat(image):
            qa = image.select('QA_PIXEL')
            mask = qa.bitwiseAnd(1 << 3).eq(0)  # Cloud shadow
            mask = mask.And(qa.bitwiseAnd(1 << 4).eq(0))  # Cloud
            return image.updateMask(mask)
        return collection.map(mask_landsat)
    
    elif 'S2' in dataset_id or 'SENTINEL' in dataset_id.upper():
        def mask_sentinel2(image):
            qa = image.select('QA60')
            cloudBitMask = 1 << 10
            cirrusBitMask = 1 << 11
            mask = qa.bitwiseAnd(cloudBitMask).eq(0)
            mask = mask.And(qa.bitwiseAnd(cirrusBitMask).eq(0))
            return image.updateMask(mask)
        return collection.map(mask_sentinel2)
    
    else:
        # No cloud masking for other datasets
        return collection


def list_datasets(category: Optional[str] = None) -> Dict:
    """
    List common GEE datasets available in geeadvance.
    
    Parameters
    ----------
    category : str, optional
        Dataset category ('landcover', 'elevation', 'vegetation', 'climate')
        If None, returns all categories.
    
    Returns
    -------
    dict
        Dictionary of available datasets
    
    Examples
    --------
    >>> import geeadvance as ga
    >>> 
    >>> # List all datasets
    >>> datasets = ga.list_datasets()
    >>> 
    >>> # List only land cover datasets
    >>> lc_datasets = ga.list_datasets('landcover')
    >>> print(lc_datasets)
    """
    if category:
        if category in COMMON_DATASETS:
            return COMMON_DATASETS[category]
        else:
            raise ValueError(f"Unknown category '{category}'. "
                           f"Available: {list(COMMON_DATASETS.keys())}")
    return COMMON_DATASETS


def get_dataset_info(dataset_id: str) -> Dict:
    """
    Get information about a GEE dataset.
    
    Parameters
    ----------
    dataset_id : str
        GEE dataset ID
    
    Returns
    -------
    dict
        Dataset information including bands, properties, etc.
    
    Examples
    --------
    >>> import geeadvance as ga
    >>> info = ga.get_dataset_info('MODIS/006/MCD12Q1')
    >>> print(info['bands'])
    """
    try:
        # Try as ImageCollection first
        try:
            collection = ee.ImageCollection(dataset_id)
            first_image = collection.first()
            info = {
                'type': 'ImageCollection',
                'bands': first_image.bandNames().getInfo(),
                'properties': first_image.propertyNames().getInfo(),
                'size': collection.size().getInfo(),
            }
        except:
            # Try as single Image
            image = ee.Image(dataset_id)
            info = {
                'type': 'Image',
                'bands': image.bandNames().getInfo(),
                'properties': image.propertyNames().getInfo(),
            }
        
        return info
        
    except Exception as e:
        raise ValueError(f"Failed to get info for '{dataset_id}': {str(e)}")


def create_composite(
    collection: ee.ImageCollection,
    method: str = 'median',
    region: Optional[ee.Geometry] = None,
) -> ee.Image:
    """
    Create a composite image from an image collection.
    
    Parameters
    ----------
    collection : ee.ImageCollection
        Input image collection
    method : str, optional
        Compositing method ('median', 'mean', 'max', 'min', 'mosaic')
    region : ee.Geometry, optional
        Region to clip the composite
    
    Returns
    -------
    ee.Image
        Composite image
    
    Examples
    --------
    >>> import geeadvance as ga
    >>> import ee
    >>> 
    >>> collection = ga.load_dataset('MODIS/006/MOD13A2',
    ...                              start_date='2020-01-01',
    ...                              end_date='2020-12-31')
    >>> composite = ga.create_composite(collection, method='median')
    """
    if method == 'median':
        composite = collection.median()
    elif method == 'mean':
        composite = collection.mean()
    elif method == 'max':
        composite = collection.max()
    elif method == 'min':
        composite = collection.min()
    elif method == 'mosaic':
        composite = collection.mosaic()
    else:
        raise ValueError(f"Unknown method '{method}'. "
                        "Available: median, mean, max, min, mosaic")
    
    if region:
        composite = composite.clip(region)
    
    return composite


def get_landcover_classes(dataset_id: str) -> Dict[int, str]:
    """
    Get land cover class definitions for common datasets.
    
    Parameters
    ----------
    dataset_id : str
        Land cover dataset ID
    
    Returns
    -------
    dict
        Dictionary mapping class values to class names
    
    Examples
    --------
    >>> import geeadvance as ga
    >>> classes = ga.get_landcover_classes('MODIS/006/MCD12Q1')
    >>> print(classes)
    {1: 'Evergreen Needleleaf Forests', 2: 'Evergreen Broadleaf Forests', ...}
    """
    # MODIS Land Cover Type 1 (IGBP)
    if 'MCD12Q1' in dataset_id:
        return {
            1: 'Evergreen Needleleaf Forests',
            2: 'Evergreen Broadleaf Forests',
            3: 'Deciduous Needleleaf Forests',
            4: 'Deciduous Broadleaf Forests',
            5: 'Mixed Forests',
            6: 'Closed Shrublands',
            7: 'Open Shrublands',
            8: 'Woody Savannas',
            9: 'Savannas',
            10: 'Grasslands',
            11: 'Permanent Wetlands',
            12: 'Croplands',
            13: 'Urban and Built-up Lands',
            14: 'Cropland/Natural Vegetation Mosaics',
            15: 'Permanent Snow and Ice',
            16: 'Barren',
            17: 'Water Bodies',
        }
    
    # ESA WorldCover
    elif 'WorldCover' in dataset_id:
        return {
            10: 'Tree cover',
            20: 'Shrubland',
            30: 'Grassland',
            40: 'Cropland',
            50: 'Built-up',
            60: 'Bare / sparse vegetation',
            70: 'Snow and ice',
            80: 'Permanent water bodies',
            90: 'Herbaceous wetland',
            95: 'Mangroves',
            100: 'Moss and lichen',
        }
    
    else:
        return {}
