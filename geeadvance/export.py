"""
Export module for downloading GEE data

Provides utilities for exporting images and data from Google Earth Engine
to various formats including GeoTIFF, GeoJSON, and cloud storage.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
import os
import time
from typing import Optional, Union, List, Dict
from pathlib import Path


def export_tif(
    image: ee.Image,
    region: ee.Geometry,
    filename: str,
    scale: int = 30,
    crs: str = 'EPSG:4326',
    folder: Optional[str] = None,
    max_pixels: int = 1e13,
    file_per_band: bool = False,
) -> str:
    """
    Export an Earth Engine image as GeoTIFF.
    
    Parameters
    ----------
    image : ee.Image
        Image to export
    region : ee.Geometry
        Region to export
    filename : str
        Output filename (without extension)
    scale : int, optional
        Resolution in meters (default: 30)
    crs : str, optional
        Coordinate reference system (default: 'EPSG:4326')
    folder : str, optional
        Google Drive folder name (default: None)
    max_pixels : int, optional
        Maximum number of pixels (default: 1e13)
    file_per_band : bool, optional
        Export each band as separate file (default: False)
    
    Returns
    -------
    str
        Task ID for the export task
    
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
    >>> task_id = geeadvance.export_tif(lc, roi, 'landcover_2020', scale=500)
    >>> print(f"Export started: {task_id}")
    """
    # Create export task
    task = ee.batch.Export.image.toDrive(
        image=image,
        description=filename,
        folder=folder or 'GEE_Exports',
        fileNamePrefix=filename,
        region=region,
        scale=scale,
        crs=crs,
        maxPixels=max_pixels,
        filePerBand=file_per_band,
    )
    
    # Start the task
    task.start()
    
    print(f"✓ Export task started: {filename}")
    print(f"  Task ID: {task.id}")
    print(f"  Check status at: https://code.earthengine.google.com/tasks")
    
    return task.id


def export_geojson(
    feature_collection: ee.FeatureCollection,
    filename: str,
    folder: Optional[str] = None,
) -> str:
    """
    Export a FeatureCollection as GeoJSON.
    
    Parameters
    ----------
    feature_collection : ee.FeatureCollection
        Features to export
    filename : str
        Output filename (without extension)
    folder : str, optional
        Google Drive folder name
    
    Returns
    -------
    str
        Task ID for the export task
    
    Examples
    --------
    >>> features = ee.FeatureCollection('TIGER/2018/States')
    >>> task_id = geeadvance.export_geojson(features, 'us_states')
    """
    task = ee.batch.Export.table.toDrive(
        collection=feature_collection,
        description=filename,
        folder=folder or 'GEE_Exports',
        fileNamePrefix=filename,
        fileFormat='GeoJSON',
    )
    
    task.start()
    
    print(f"✓ Export task started: {filename}")
    print(f"  Task ID: {task.id}")
    
    return task.id


def export_to_asset(
    image: ee.Image,
    asset_id: str,
    region: ee.Geometry,
    scale: int = 30,
    crs: str = 'EPSG:4326',
    max_pixels: int = 1e13,
) -> str:
    """
    Export an image to a GEE Asset.
    
    Parameters
    ----------
    image : ee.Image
        Image to export
    asset_id : str
        Asset ID (e.g., 'users/username/asset_name')
    region : ee.Geometry
        Region to export
    scale : int, optional
        Resolution in meters
    crs : str, optional
        Coordinate reference system
    max_pixels : int, optional
        Maximum number of pixels
    
    Returns
    -------
    str
        Task ID for the export task
    
    Examples
    --------
    >>> task_id = geeadvance.export_to_asset(image, 'users/myuser/landcover', roi)
    """
    task = ee.batch.Export.image.toAsset(
        image=image,
        description=asset_id.split('/')[-1],
        assetId=asset_id,
        region=region,
        scale=scale,
        crs=crs,
        maxPixels=max_pixels,
    )
    
    task.start()
    
    print(f"✓ Export to asset started: {asset_id}")
    print(f"  Task ID: {task.id}")
    
    return task.id


def export_to_drive(
    image: ee.Image,
    description: str,
    folder: str = 'GEE_Exports',
    region: Optional[ee.Geometry] = None,
    scale: int = 30,
    crs: str = 'EPSG:4326',
) -> str:
    """
    Export an image to Google Drive.
    
    Parameters
    ----------
    image : ee.Image
        Image to export
    description : str
        Task description and filename
    folder : str, optional
        Drive folder name
    region : ee.Geometry, optional
        Region to export
    scale : int, optional
        Resolution in meters
    crs : str, optional
        Coordinate reference system
    
    Returns
    -------
    str
        Task ID
    
    Examples
    --------
    >>> task_id = geeadvance.export_to_drive(ndvi_image, 'ndvi_2020', region=roi)
    """
    return export_tif(image, region, description, scale, crs, folder)


def check_task_status(task_id: str) -> Dict:
    """
    Check the status of an export task.
    
    Parameters
    ----------
    task_id : str
        Task ID returned from export function
    
    Returns
    -------
    dict
        Task status information
    
    Examples
    --------
    >>> status = geeadvance.check_task_status(task_id)
    >>> print(f"Status: {status['state']}")
    """
    tasks = ee.batch.Task.list()
    
    for task in tasks:
        if task.id == task_id:
            return {
                'id': task.id,
                'state': task.state,
                'description': task.config.get('description', 'N/A'),
                'creation_time': task.creation_timestamp_ms,
            }
    
    return {'error': 'Task not found'}


def wait_for_task(task_id: str, timeout: int = 3600, check_interval: int = 30) -> bool:
    """
    Wait for a task to complete.
    
    Parameters
    ----------
    task_id : str
        Task ID to monitor
    timeout : int, optional
        Maximum time to wait in seconds (default: 3600)
    check_interval : int, optional
        Time between status checks in seconds (default: 30)
    
    Returns
    -------
    bool
        True if completed successfully, False otherwise
    
    Examples
    --------
    >>> task_id = geeadvance.export_tif(image, roi, 'output')
    >>> success = geeadvance.wait_for_task(task_id)
    >>> if success:
    ...     print("Export completed!")
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        status = check_task_status(task_id)
        
        if status.get('state') == 'COMPLETED':
            print(f"✓ Task completed successfully!")
            return True
        elif status.get('state') == 'FAILED':
            print(f"✗ Task failed!")
            return False
        elif status.get('state') in ['CANCELLED', 'CANCEL_REQUESTED']:
            print(f"✗ Task was cancelled!")
            return False
        
        print(f"  Task status: {status.get('state', 'UNKNOWN')} - waiting...")
        time.sleep(check_interval)
    
    print(f"✗ Timeout reached after {timeout} seconds")
    return False


def download_image(
    image: ee.Image,
    region: ee.Geometry,
    filename: str,
    scale: int = 30,
    crs: str = 'EPSG:4326',
) -> str:
    """
    Download an image directly (for small regions).
    
    Note: This uses getDownloadURL which has size limitations.
    For large areas, use export_tif instead.
    
    Parameters
    ----------
    image : ee.Image
        Image to download
    region : ee.Geometry
        Region to download
    filename : str
        Output filename
    scale : int, optional
        Resolution in meters
    crs : str, optional
        Coordinate reference system
    
    Returns
    -------
    str
        Download URL
    
    Examples
    --------
    >>> url = geeadvance.download_image(small_image, small_roi, 'output.tif')
    >>> print(f"Download from: {url}")
    """
    url = image.getDownloadURL({
        'region': region,
        'scale': scale,
        'crs': crs,
        'format': 'GEO_TIFF',
    })
    
    print(f"✓ Download URL generated:")
    print(f"  {url}")
    print(f"\nNote: URL expires after a short time. Download immediately.")
    
    return url


def batch_export(
    images: List[ee.Image],
    regions: List[ee.Geometry],
    filenames: List[str],
    scale: int = 30,
    folder: str = 'GEE_Exports',
) -> List[str]:
    """
    Export multiple images in batch.
    
    Parameters
    ----------
    images : list of ee.Image
        Images to export
    regions : list of ee.Geometry
        Regions for each image
    filenames : list of str
        Filenames for each export
    scale : int, optional
        Resolution in meters
    folder : str, optional
        Drive folder name
    
    Returns
    -------
    list of str
        List of task IDs
    
    Examples
    --------
    >>> task_ids = geeadvance.batch_export(
    ...     images=[img1, img2, img3],
    ...     regions=[roi1, roi2, roi3],
    ...     filenames=['out1', 'out2', 'out3']
    ... )
    """
    if not (len(images) == len(regions) == len(filenames)):
        raise ValueError("images, regions, and filenames must have same length")
    
    task_ids = []
    
    for image, region, filename in zip(images, regions, filenames):
        task_id = export_tif(image, region, filename, scale=scale, folder=folder)
        task_ids.append(task_id)
    
    print(f"\n✓ Started {len(task_ids)} export tasks")
    
    return task_ids
