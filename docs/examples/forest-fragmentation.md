# Example: Forest Fragmentation Analysis

This example demonstrates how to use **GeeAdvance** to analyze forest fragmentation patterns in the Western Ghats of India using ESA WorldCover data.

## Setup

First, import the necessary libraries and initialize Earth Engine with your project ID.

```python
import ee
import geeadvance
import geemap
import pandas as pd
import matplotlib.pyplot as plt

# Authenticate and initialize
geeadvance.initialize(project='spatialgeography')
```

## 1. Define Study Area

We will select a 10km x 10km area in the Western Ghats, a biodiversity hotspot known for its complex forest fragments.

```python
# Center coordinates: 75.6, 12.4 (Kodagu region)
study_area = geeadvance.create_bbox(75.55, 12.35, 75.65, 12.45)

# Visualize location
Map = geemap.Map()
Map.centerObject(study_area, 12)
Map.addLayer(study_area, {'color': 'red'}, 'Study Area')
Map
```

## 2. Load Land Cover Data

We will use the ESA WorldCover dataset (10m resolution).

```python
# Load ESA WorldCover
landcover = geeadvance.load_dataset('ESA/WorldCover/v100', region=study_area)

# Extract only the Tree Cover class (Value 10 in WorldCover)
forest_mask = landcover.select('Map').eq(10)
Map.addLayer(forest_mask.selfMask(), {'palette': ['green']}, 'Forest Mask')
```

## 3. Calculate Fragmentation Metrics

We will use the **GeeAdvance Local Engine** to calculate patch-based metrics. This is much more reliable than GEE server-side operations for counting discrete patches.

```python
# Calculate metrics at 30m resolution for a balance of detail and speed
# GeeAdvance will download a temporary TIF for local processing
metrics_df = geeadvance.calculate_metrics(
    image=landcover.select('Map'),
    region=study_area,
    scale=30
)

# Filter for Forest class (ID 10)
forest_metrics = metrics_df[metrics_df['class'] == 10]
print("--- Forest Fragmentation Profile ---")
print(forest_metrics)
```

## 4. Interpret the Results

A typical fragmentation analysis focuses on these indicators:

1. **NP (Number of Patches)**: A high number of patches relative to total area indicates fragmentation.
2. **AREA_MN (Mean Patch Area)**: Smaller average patch sizes suggest higher disconnection between habitats.
3. **PLAND (Percent of Landscape)**: Shows the total forest cover.
4. **ED (Edge Density)**: Higher edge density indicates more forest "interface" with human-modified land, which can lead to edge effects.

### Visualization of Metrics

```python
# Compare Forest (10) vs Grassland (30) or Cropland (40)
plt.figure(figsize=(10, 6))
metrics_df.set_index('class')['np'].plot(kind='bar', color='forestgreen')
plt.title('Number of Patches per Land Cover Class')
plt.ylabel('NP')
plt.xlabel('Class ID')
plt.show()
```

## 5. Download for Desktop GIS

If you want to perform further analysis in QGIS or ArcGIS, you can download the high-resolution clipped forest map.

```python
geeadvance.download_large_area(
    image=forest_mask,
    region=study_area,
    filename='kodagu_forest.tif',
    scale=10
)
```

## Conclusion

Using **GeeAdvance**, we transformed a raw GEE image into a structured dataset of landscape indices in just a few lines of code. This workflow is reproducible and can be easily scaled to multiple years to track fragmentation trends over time.
