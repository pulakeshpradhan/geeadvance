# Quick Start Guide

Get started with GeeAdvance in 5 minutes!

## 1. Install

```bash
pip install geeadvance
```

## 2. Authenticate

```python
import ee
import geeadvance

# Standard GEE authentication
ee.Authenticate()
ee.Initialize(project='your-project-id')
```

This will open a browser for authentication. Sign in with your Google account and grant permissions.

## 3. Your First Analysis

```python
import ee
import geeadvance

# Define a region (example: part of India)
roi = geeadvance.create_bbox(
    min_lon=77.0,
    min_lat=20.0,
    max_lon=78.0,
    max_lat=21.0
)

# Load land cover data
landcover = geeadvance.load_dataset(
    'ESA/WorldCover/v100',
    region=roi
)

# Calculate landscape metrics
metrics = geeadvance.calculate_metrics(
    landcover.select('Map'),
    roi,
    scale=100
)

print(metrics)
```

## 4. Download Data

```python
# Download the land cover (handles large areas automatically)
geeadvance.download_large_area(
    landcover.select('Map'),
    roi,
    'my_landcover.tif',
    scale=100
)
```

## 5. Visualize

```python
import geemap

# Create interactive map
Map = geemap.Map()
Map.centerObject(roi, zoom=9)
Map.addLayer(roi, {'color': 'red'}, 'ROI')
Map.addLayer(
    landcover.select('Map'),
    {'min': 10, 'max': 100},
    'Land Cover'
)
Map
```

## Complete Example

Here's a complete workflow:

```python
import geeadvance as ga
import ee
import geemap

# Setup
ga.quick_setup()

# Define study area
study_area = ga.create_bbox(75.0, 12.0, 76.0, 13.0)

# Load data
lc = ga.load_dataset('ESA/WorldCover/v100', region=study_area)

# Calculate metrics
area_metrics = ga.area_metrics(lc.select('Map'), study_area, scale=100)
diversity_metrics = ga.diversity_metrics(lc.select('Map'), study_area, scale=100)

print("Area Metrics:", area_metrics)
print("Diversity Metrics:", diversity_metrics)

# Download
ga.download_large_area(
    lc.select('Map'),
    study_area,
    'landcover_output.tif',
    scale=100
)

# Visualize
Map = geemap.Map()
Map.centerObject(study_area, 9)
Map.addLayer(lc.select('Map'), {}, 'Land Cover')
Map
```

## Common Datasets

```python
# MODIS Land Cover
modis_lc = ga.load_dataset('MODIS/006/MCD12Q1')

# ESA WorldCover
esa_lc = ga.load_dataset('ESA/WorldCover/v100')

# Sentinel-2
s2 = ga.load_dataset(
    'COPERNICUS/S2_SR',
    start_date='2020-01-01',
    end_date='2020-12-31',
    filter_clouds=True
)

# SRTM Elevation
dem = ga.load_dataset('USGS/SRTMGL1_003')
```

## Next Steps

### Tutorials

1. [Authentication](../tutorials/01_authentication.ipynb)
2. [Loading Data](../tutorials/02_loading_data.md)
3. [Calculating Metrics](../tutorials/03_area_edge_metrics.md)
4. [Complete Workflow](../tutorials/07_complete_workflow.ipynb)

### User Guides

- [Landscape Metrics](../user-guide/landscape-metrics.md)
- [Large Area Downloads](../user-guide/large-downloads.md)
- [Export Options](../user-guide/export-options.md)

### Examples

- [Forest Fragmentation](../examples/forest-fragmentation.md)
- [Urban Growth](../examples/urban-growth.md)
- [Wetland Analysis](../examples/wetland-analysis.md)

## Tips for Beginners

### 1. Start Small

Test with small regions first:

```python
# Small test area
test_roi = ga.create_bbox(77.0, 20.0, 77.1, 20.1)
```

### 2. Check Data Before Downloading

```python
# Estimate download size
estimate = ga.estimate_download_size(image, roi, scale=100)
print(f"Size: {estimate['size_mb']} MB")
```

### 3. Use Appropriate Scale

```python
# Coarse scale for large areas
ga.download_large_area(image, large_roi, 'output.tif', scale=500)

# Fine scale for small areas
ga.download_large_area(image, small_roi, 'output.tif', scale=30)
```

### 4. Visualize First

Always visualize before downloading:

```python
Map = geemap.Map()
Map.addLayer(image, {}, 'Preview')
Map
```

## Troubleshooting

### Authentication Issues

```python
# Check authentication status
if not ga.is_authenticated():
    ga.authenticate()
    ga.initialize()
```

### Download Fails

```python
# Use smaller tiles for large areas
ga.download_large_area(
    image, roi, 'output.tif',
    tile_size=0.5,  # Smaller tiles
    num_threads=4
)
```

### Memory Issues

```python
# Reduce scale and threads
ga.download_large_area(
    image, roi, 'output.tif',
    scale=500,      # Coarser resolution
    num_threads=2   # Fewer threads
)
```

## Getting Help

- 📖 [Full Documentation](https://pulakeshpradhan.github.io/geeadvance/)
- 🐛 [Report Issues](https://github.com/pulakeshpradhan/geeadvance/issues)
- 💬 [Discussions](https://github.com/pulakeshpradhan/geeadvance/discussions)
- 📧 [Email](mailto:pulakesh.mid@gmail.com)

Happy analyzing! 🎉
