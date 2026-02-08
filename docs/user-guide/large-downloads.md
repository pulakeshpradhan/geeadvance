# Large Area Downloads

One of the most powerful features of GeeAdvance is its ability to download large areas without encountering size limitations. This is achieved through **automatic tiling** using geemap.

## The Problem

Google Earth Engine has download size limitations:

- Direct downloads are limited to ~32 MB
- Large regions often exceed this limit
- Manual tiling is tedious and error-prone

## The Solution

GeeAdvance automatically:

1. **Splits** large regions into manageable tiles
2. **Downloads** each tile in parallel
3. **Merges** tiles into a single GeoTIFF
4. **Cleans up** temporary files

## Basic Usage

```python
import ee
import geeadvance

# Authenticate and Initialize with project ID
ee.Authenticate()
ee.Initialize(project='your-project-id')

# Define a LARGE region (e.g., entire state)
large_roi = geeadvance.create_bbox(
    min_lon=75.0,
    min_lat=12.0,
    max_lon=78.0,
    max_lat=15.0
)

# Load land cover
landcover = geeadvance.load_dataset('ESA/WorldCover/v100')

# Download large area - automatically handles tiling!
geeadvance.download_large_area(
    image=landcover.select('Map'),
    region=large_roi,
    filename='large_landcover.tif',
    scale=100,
    crs='EPSG:4326'
)
```

## Advanced Options

### Controlling Tile Size

For very large areas, you can control the tile size:

```python
geeadvance.download_large_area(
    image=landcover,
    region=very_large_roi,
    filename='output.tif',
    scale=100,
    tile_size=0.5,  # Smaller tiles for huge areas
    num_threads=8   # More parallel downloads
)
```

### Estimating Download Size

Before downloading, estimate the size and get recommendations:

```python
estimate = geeadvance.estimate_download_size(
    image=landcover,
    region=large_roi,
    scale=100
)

print(f"Estimated size: {estimate['size_mb']} MB")
print(f"Pixel count: {estimate['pixel_count']:,}")
print(f"Recommendation: {estimate['recommendation']}")
```

**Example output:**

```text
Estimated size: 1250.5 MB
Pixel count: 327,680,000
Recommendation: Use tile_size=0.5
```

## Download Strategies

### Small Areas (< 100 MB)

```python
# Direct download works fine
geeadvance.download_large_area(image, small_roi, 'output.tif', scale=30)
```

### Medium Areas (100-500 MB)

```python
# Use default tiling
geeadvance.download_large_area(
    image, medium_roi, 'output.tif',
    scale=30,
    tile_size=1.0  # Default
)
```

### Large Areas (500-2000 MB)

```python
# Use smaller tiles
geeadvance.download_large_area(
    image, large_roi, 'output.tif',
    scale=30,
    tile_size=0.5,
    num_threads=8
)
```

### Very Large Areas (> 2000 MB)

```python
# Use very small tiles and more threads
geeadvance.download_large_area(
    image, huge_roi, 'output.tif',
    scale=30,
    tile_size=0.25,
    num_threads=12
)
```

## Downloading Image Collections

Download all images in a collection:

```python
# Load time series
collection = geeadvance.load_dataset(
    'MODIS/006/MOD13A2',
    start_date='2020-01-01',
    end_date='2020-12-31',
    region=roi
)

# Download all images
files = geeadvance.download_collection(
    collection=collection,
    region=roi,
    output_dir='ndvi_timeseries',
    prefix='ndvi',
    scale=500
)

print(f"Downloaded {len(files)} images")
```

## Performance Tips

### 1. Choose Appropriate Scale

```python
# Higher scale = smaller file size
geeadvance.download_large_area(image, roi, 'output.tif', scale=500)  # Faster
geeadvance.download_large_area(image, roi, 'output.tif', scale=30)   # Slower but detailed
```

### 2. Optimize Thread Count

```python
# More threads = faster download (up to a point)
geeadvance.download_large_area(
    image, roi, 'output.tif',
    num_threads=4   # Good for most systems
)
```

### 3. Use Appropriate CRS

```python
# Use projected CRS for large areas
geeadvance.download_large_area(
    image, roi, 'output.tif',
    crs='EPSG:32643',  # UTM Zone 43N for India
    scale=30
)
```

## Troubleshooting

### Download Fails

**Problem**: Download fails even with tiling

**Solution**: Reduce tile size further

```python
geeadvance.download_large_area(
    image, roi, 'output.tif',
    tile_size=0.1,  # Very small tiles
    num_threads=2   # Fewer parallel downloads
)
```

### Memory Issues

**Problem**: System runs out of memory

**Solution**: Reduce threads and tile size

```python
geeadvance.download_large_area(
    image, roi, 'output.tif',
    tile_size=0.25,
    num_threads=2  # Less memory usage
)
```

### Slow Downloads

**Problem**: Download is very slow

**Solution**: Increase threads and tile size

```python
geeadvance.download_large_area(
    image, roi, 'output.tif',
    tile_size=2.0,   # Larger tiles
    num_threads=12   # More parallelism
)
```

## Comparison with Standard Export

| Method | Max Size | Speed | Complexity |
| :--- | :--- | :--- | :--- |
| `ee.batch.Export` | Limited | Slow | Manual |
| `geemap.download` | Unlimited | Fast | Simple |
| `geeadvance.download_large_area` | Unlimited | Fast | Very Simple |

## Complete Example

```python
import ee
import geeadvance

# Setup
ee.Authenticate()
ee.Initialize(project='your-project-id')

# Define study area (e.g., Western Ghats)
study_area = geeadvance.create_bbox(73.0, 8.0, 77.0, 12.0)

# Estimate size first
landcover = geeadvance.load_dataset('ESA/WorldCover/v100')
estimate = geeadvance.estimate_download_size(landcover, study_area, scale=100)

print(f"Area: {estimate['area_km2']:.0f} km²")
print(f"Size: {estimate['size_mb']:.1f} MB")
print(f"Recommendation: {estimate['recommendation']}")

# Download with recommended settings
if estimate['recommended_tile_size']:
    geeadvance.download_large_area(
        landcover.select('Map'),
        study_area,
        'western_ghats_landcover.tif',
        scale=100,
        tile_size=estimate['recommended_tile_size']
    )
else:
    # Direct download for small areas
    geeadvance.download_large_area(
        landcover.select('Map'),
        study_area,
        'western_ghats_landcover.tif',
        scale=100
    )

print("✓ Download complete!")
```

## Next Steps

- Learn about [Export Options](export-options.md)
- Explore [Visualization](visualization.md) techniques
- See [Complete Workflow](../tutorials/07_complete_workflow.ipynb) example
