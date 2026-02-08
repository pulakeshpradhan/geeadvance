"""
Download module with geemap integration for large area support

Handles downloading large areas by automatically tiling and merging,
preventing download size errors.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
import geemap
import os
from typing import Optional, Union, List
from pathlib import Path


def download_large_area(
    image: ee.Image,
    region: ee.Geometry,
    filename: str,
    scale: int = 30,
    crs: str = 'EPSG:4326',
    tile_size: float = 1.0,
    num_threads: int = 4,
    output_dir: str = '.',
) -> str:
    """
    Download large area imagery using geemap's tiling functionality.
    
    This function automatically splits large regions into tiles, downloads them,
    and merges them into a single GeoTIFF. This prevents download size errors
    that occur with GEE's standard export methods.
    
    Parameters
    ----------
    image : ee.Image
        Image to download
    region : ee.Geometry
        Region of interest (can be very large)
    filename : str
        Output filename (e.g., 'output.tif')
    scale : int, optional
        Resolution in meters (default: 30)
    crs : str, optional
        Coordinate reference system (default: 'EPSG:4326')
    tile_size : float, optional
        Size of each tile in degrees (default: 1.0)
        Smaller values = more tiles = slower but more reliable
    num_threads : int, optional
        Number of parallel download threads (default: 4)
    output_dir : str, optional
        Output directory (default: current directory)
    
    Returns
    -------
    str
        Path to downloaded file
    
    Examples
    --------
    >>> import ee
    >>> import geeadvance
    >>> 
    >>> # Standard GEE authentication and initialization
    >>> ee.Authenticate()
    >>> ee.Initialize(project='your-project-id')
    >>> 
    >>> # Download large area (e.g., entire state)
    >>> large_roi = geeadvance.create_bbox(75.0, 12.0, 78.0, 15.0)
    >>> lc = geeadvance.load_dataset('ESA/WorldCover/v100')
    >>> 
    >>> geeadvance.download_large_area(
    ...     lc.select('Map'),
    ...     large_roi,
    ...     'large_landcover.tif',
    ...     scale=100,
    ...     tile_size=0.5  # Smaller tiles for very large areas
    ... )
    """
    output_path = os.path.join(output_dir, filename)
    
    try:
        print(f"📥 Starting download: {filename}")
        print(f"   Scale: {scale}m | CRS: {crs}")
        print(f"   Tile size: {tile_size}° | Threads: {num_threads}")
        
        # Use geemap's download function with tiling
        geemap.download_ee_image(
            image=image,
            filename=output_path,
            region=region,
            scale=scale,
            crs=crs,
            num_threads=num_threads,
        )
        
        print(f"✓ Download complete: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ Download failed: {str(e)}")
        print("\nTrying alternative method with manual tiling...")
        
        # Fallback: manual tiling
        return _download_with_manual_tiling(
            image, region, filename, scale, crs, tile_size, output_dir
        )


def _download_with_manual_tiling(
    image: ee.Image,
    region: ee.Geometry,
    filename: str,
    scale: int,
    crs: str,
    tile_size: float,
    output_dir: str,
) -> str:
    """
    Fallback method: manually tile, download, and merge.
    """
    import rasterio
    from rasterio.merge import merge
    import numpy as np
    
    print("📦 Creating tiles...")
    
    # Get region bounds
    bounds = region.bounds().coordinates().get(0).getInfo()
    min_lon = min([coord[0] for coord in bounds])
    max_lon = max([coord[0] for coord in bounds])
    min_lat = min([coord[1] for coord in bounds])
    max_lat = max([coord[1] for coord in bounds])
    
    # Create tiles
    tiles = []
    tile_files = []
    
    lon = min_lon
    tile_idx = 0
    
    while lon < max_lon:
        lat = min_lat
        while lat < max_lat:
            tile_region = ee.Geometry.Rectangle([
                lon, lat,
                min(lon + tile_size, max_lon),
                min(lat + tile_size, max_lat)
            ])
            
            tiles.append(tile_region)
            tile_files.append(f"tile_{tile_idx}.tif")
            tile_idx += 1
            
            lat += tile_size
        lon += tile_size
    
    print(f"   Created {len(tiles)} tiles")
    
    # Download each tile
    temp_dir = os.path.join(output_dir, 'temp_tiles')
    os.makedirs(temp_dir, exist_ok=True)
    
    for i, (tile_region, tile_file) in enumerate(zip(tiles, tile_files)):
        print(f"   Downloading tile {i+1}/{len(tiles)}...", end='\r')
        
        tile_path = os.path.join(temp_dir, tile_file)
        
        try:
            geemap.download_ee_image(
                image=image,
                filename=tile_path,
                region=tile_region,
                scale=scale,
                crs=crs,
            )
        except Exception as e:
            print(f"\n   Warning: Tile {i+1} failed: {str(e)}")
            continue
    
    print(f"\n✓ Downloaded {len(tiles)} tiles")
    
    # Merge tiles
    print("🔗 Merging tiles...")
    
    tile_paths = [os.path.join(temp_dir, f) for f in tile_files if os.path.exists(os.path.join(temp_dir, f))]
    
    if not tile_paths:
        raise Exception("No tiles were successfully downloaded")
    
    src_files = [rasterio.open(f) for f in tile_paths]
    mosaic, out_trans = merge(src_files)
    
    # Save merged file
    out_meta = src_files[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "compress": "lzw"
    })
    
    output_path = os.path.join(output_dir, filename)
    
    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(mosaic)
    
    # Cleanup
    for src in src_files:
        src.close()
    
    for tile_path in tile_paths:
        os.remove(tile_path)
    
    os.rmdir(temp_dir)
    
    print(f"✓ Merged and saved: {output_path}")
    
    return output_path


def download_collection(
    collection: ee.ImageCollection,
    region: ee.Geometry,
    output_dir: str,
    prefix: str = 'image',
    scale: int = 30,
    crs: str = 'EPSG:4326',
) -> List[str]:
    """
    Download all images in a collection.
    
    Parameters
    ----------
    collection : ee.ImageCollection
        Image collection to download
    region : ee.Geometry
        Region of interest
    output_dir : str
        Output directory
    prefix : str, optional
        Filename prefix (default: 'image')
    scale : int, optional
        Resolution in meters
    crs : str, optional
        Coordinate reference system
    
    Returns
    -------
    list of str
        List of downloaded file paths
    
    Examples
    --------
    >>> collection = geeadvance.load_dataset('MODIS/006/MOD13A2',
    ...                                      start_date='2020-01-01',
    ...                                      end_date='2020-03-31')
    >>> files = geeadvance.download_collection(collection, roi, 'outputs')
    """
    os.makedirs(output_dir, exist_ok=True)
    
    size = collection.size().getInfo()
    print(f"📥 Downloading {size} images from collection...")
    
    downloaded_files = []
    
    image_list = collection.toList(size)
    
    for i in range(size):
        image = ee.Image(image_list.get(i))
        filename = f"{prefix}_{i:04d}.tif"
        
        print(f"   Downloading {i+1}/{size}: {filename}")
        
        filepath = download_large_area(
            image,
            region,
            filename,
            scale=scale,
            crs=crs,
            output_dir=output_dir,
        )
        
        downloaded_files.append(filepath)
    
    print(f"✓ Downloaded {len(downloaded_files)} images")
    
    return downloaded_files


def download_with_geemap_map(
    Map: geemap.Map,
    layer_name: str,
    filename: str,
    scale: int = 30,
    region: Optional[ee.Geometry] = None,
) -> str:
    """
    Download a layer from a geemap Map object.
    
    Parameters
    ----------
    Map : geemap.Map
        Geemap Map object
    layer_name : str
        Name of the layer to download
    filename : str
        Output filename
    scale : int, optional
        Resolution in meters
    region : ee.Geometry, optional
        Region to download (uses map bounds if None)
    
    Returns
    -------
    str
        Path to downloaded file
    
    Examples
    --------
    >>> Map = geemap.Map()
    >>> Map.addLayer(image, {}, 'My Layer')
    >>> geeadvance.download_with_geemap_map(Map, 'My Layer', 'output.tif')
    """
    # Get the layer
    layers = Map.ee_layers
    
    target_layer = None
    for layer in layers:
        if layer['name'] == layer_name:
            target_layer = layer['ee_object']
            break
    
    if target_layer is None:
        raise ValueError(f"Layer '{layer_name}' not found in map")
    
    # Get region
    if region is None:
        region = Map.user_roi or ee.Geometry.Rectangle(Map.bounds)
    
    # Download
    return download_large_area(
        target_layer,
        region,
        filename,
        scale=scale,
    )


def estimate_download_size(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> dict:
    """
    Estimate the download size and recommend tiling strategy.
    
    Parameters
    ----------
    image : ee.Image
        Image to estimate
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Resolution in meters
    
    Returns
    -------
    dict
        Estimation details including size, pixel count, and recommendations
    
    Examples
    --------
    >>> estimate = geeadvance.estimate_download_size(image, large_roi, scale=100)
    >>> print(f"Estimated size: {estimate['size_mb']} MB")
    >>> print(f"Recommended tile size: {estimate['recommended_tile_size']}")
    """
    # Get region area
    area = region.area().getInfo()
    area_km2 = area / 1e6
    
    # Calculate pixel count
    pixel_count = area / (scale * scale)
    
    # Get number of bands
    num_bands = image.bandNames().size().getInfo()
    
    # Estimate size (assuming 4 bytes per pixel for Float32)
    size_bytes = pixel_count * num_bands * 4
    size_mb = size_bytes / (1024 * 1024)
    size_gb = size_mb / 1024
    
    # Recommend tiling strategy
    if size_mb < 100:
        recommended_tile_size = None  # No tiling needed
        recommendation = "Direct download recommended"
    elif size_mb < 500:
        recommended_tile_size = 1.0
        recommendation = "Use tile_size=1.0"
    elif size_mb < 2000:
        recommended_tile_size = 0.5
        recommendation = "Use tile_size=0.5"
    else:
        recommended_tile_size = 0.25
        recommendation = "Use tile_size=0.25 or smaller"
    
    return {
        'area_km2': area_km2,
        'pixel_count': int(pixel_count),
        'num_bands': num_bands,
        'size_mb': round(size_mb, 2),
        'size_gb': round(size_gb, 2),
        'recommended_tile_size': recommended_tile_size,
        'recommendation': recommendation,
    }
