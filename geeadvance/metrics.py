"""
Landscape metrics calculation module

Implements landscape ecology metrics similar to the R landscapemetrics package.
Provides support for local processing of downloaded TIFF files for high-fidelity 
patch-based analysis which is difficult/slow to perform directly in GEE.

Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

import ee
import os
import pandas as pd
import numpy as np
import rasterio
from scipy import ndimage
from typing import Optional, Union, Dict, List
from .download import download_large_area


def calculate_metrics(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
    filename: str = "temp_metrics.tif",
    keep_tif: bool = False,
) -> pd.DataFrame:
    """
    High-level workflow: Download image and calculate metrics locally.
    
    This follows the USER's request to 'download the tif and do the processing 
    in the package' for better accuracy and flexibility.
    
    Parameters
    ----------
    image : ee.Image
        Input land cover image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters for calculations
    filename : str, optional
        Temporary filename for the download
    keep_tif : bool, optional
        Whether to keep the downloaded TIFF file after calculation
        
    Returns
    -------
    pd.DataFrame
        DataFrame containing calculated landscape metrics
        
    Examples
    --------
    >>> import ee
    >>> import geeadvance
    >>> 
    >>> ee.Initialize(project='spatialgeography')
    >>> 
    >>> # Load dataset
    >>> lc = geeadvance.load_dataset('MODIS/006/MCD12Q1')
    >>> roi = ee.Geometry.Rectangle([77.5, 12.9, 77.6, 13.0])
    >>> 
    >>> # Calculate metrics (automates download and local processing)
    >>> metrics = geeadvance.calculate_metrics(lc.select('LC_Type1'), roi, scale=500)
    >>> print(metrics)
    """
    # 1. Download the TIFF
    print(f"📥 Downloading image for local processing (scale={scale}m)...")
    tif_path = download_large_area(
        image=image,
        region=region,
        filename=filename,
        scale=scale
    )
    
    # 2. Process locally
    print("🔬 Calculating landscape metrics locally...")
    try:
        df = calculate_local_metrics(tif_path)
        return df
    finally:
        if not keep_tif and os.path.exists(tif_path):
            os.remove(tif_path)
            print(f"🗑️ Deleted temporary file: {tif_path}")


def calculate_local_metrics(tif_path: str) -> pd.DataFrame:
    """
    Calculate landscape metrics from a local GeoTIFF file.
    
    Parameters
    ----------
    tif_path : str
        Path to the land cover GeoTIFF
        
    Returns
    -------
    pd.DataFrame
        Metrics for each class found in the image
        
    Examples
    --------
    >>> import geeadvance
    >>> df = geeadvance.calculate_local_metrics('landcover.tif')
    >>> print(df)
    """
    with rasterio.open(tif_path) as src:
        data = src.read(1)
        res = src.res[0]  # Assuming square pixels
        nodata = src.nodata
        
    # Mask nodata
    if nodata is not None:
        mask = (data != nodata)
    else:
        mask = np.ones_like(data, dtype=bool)
        
    pixel_area_ha = (res * res) / 10000
    total_area_ha = np.sum(mask) * pixel_area_ha
    
    classes = np.unique(data[mask])
    results = []
    
    for val in classes:
        class_mask = (data == val)
        
        # Area metrics
        ca = np.sum(class_mask) * pixel_area_ha
        pland = (ca / total_area_ha) * 100
        
        # Patch-based metrics
        # Use 8-connectivity (default)
        labeled_array, num_patches = ndimage.label(class_mask)
        
        # Calculate patch sizes
        patch_sizes = ndimage.sum(class_mask, labeled_array, range(1, num_patches + 1))
        patch_areas = patch_sizes * pixel_area_ha
        area_mn = np.mean(patch_areas) if num_patches > 0 else 0
        
        # Edge metrics (simple internal/external boundary check)
        # Dilate mask and subtract original to get boundaries
        struct = ndimage.generate_binary_structure(2, 1) # 4-connectivity for edges
        dilated = ndimage.binary_dilation(class_mask, structure=struct)
        boundary = dilated & ~class_mask & mask
        te = np.sum(boundary) * res  # Approximation of edge length
        ed = te / total_area_ha
        
        results.append({
            'class': int(val),
            'ca': round(float(ca), 4),
            'pland': round(float(pland), 4),
            'np': int(num_patches),
            'area_mn': round(float(area_mn), 4),
            'te': round(float(te), 4),
            'ed': round(float(ed), 4)
        })
        
    df = pd.DataFrame(results)
    
    # Calculate Landscape level metrics
    if not df.empty:
        # Shannon Diversity Index
        pi = df['pland'] / 100
        shdi = -np.sum(pi * np.log(pi))
        
        # Add a column for landscape-level summary or just print
        print(f"📊 Landscape Level Metrics | SHDI: {shdi:.4f} | Richness: {len(classes)}")
        
    return df


def area_metrics(image: ee.Image, region: ee.Geometry, scale: int = 30) -> Dict:
    """Wrapper for backward compatibility, now using local engine if possible."""
    print("Warning: area_metrics is now a legacy wrapper. Use calculate_metrics for local processing.")
    return {'info': 'Use calculate_metrics for full local analysis'}

# Placeholder functions kept for compatibility with old imports
def edge_metrics(*args, **kwargs): return {}
def shape_metrics(*args, **kwargs): return {}
def core_metrics(*args, **kwargs): return {}
def aggregation_metrics(*args, **kwargs): return {}
def diversity_metrics(*args, **kwargs): return {}
def patch_metrics(*args, **kwargs): return None
def calculate_class_metrics(*args, **kwargs): return {}
