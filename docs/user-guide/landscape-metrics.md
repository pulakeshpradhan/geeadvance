# Landscape Metrics

Landscape metrics are quantitative indices used to characterize the spatial structure and patterns of land cover patches within a landscape. **GeeAdvance** implements a subset of metrics inspired by the R `landscapemetrics` package, optimized for Google Earth Engine.

## Metric Levels

GeeAdvance supports metrics at two levels:

1. **Class Level**: Metrics calculated for each individual land cover class (e.g., Forest, Urban, Water).
2. **Landscape Level**: Metrics that describe the entire study area as a single unit (e.g., Shannon's Diversity Index).

## Core Metrics

The current version of GeeAdvance (v0.1.0) provides the following core metrics through its local processing engine.

### Area & Composition Metrics

These metrics describe the quantity and proportion of different land cover types.

| Metric | Name | Description | Level |
| :--- | :--- | :--- | :--- |
| **CA** | Class Area | Total area of a specific class in hectares. | Class |
| **PLAND** | Percentage of Landscape | The percentage of the total landscape area occupied by a class. | Class |
| **TA** | Total Area | The total area of the study region. | Landscape |

### Patch Metrics

These metrics describe the configuration and number of discrete patches.

| Metric | Name | Description | Level |
| :--- | :--- | :--- | :--- |
| **NP** | Number of Patches | Total number of discrete patches of a specific class. | Class |
| **AREA_MN** | Mean Patch Area | The average size of patches for a specific class. | Class |

### Edge Metrics

These metrics quantify the boundaries between different land cover types.

| Metric | Name | Description | Level |
| :--- | :--- | :--- | :--- |
| **TE** | Total Edge | Total length of all edges for a class in meters. | Class |
| **ED** | Edge Density | Total edge length relative to the total landscape area (m/ha). | Class |

### Diversity Metrics

These metrics describe the variety and evenness of land cover types across the whole landscape.

| Metric | Name | Description | Level |
| :--- | :--- | :--- | :--- |
| **SHDI** | Shannon's Diversity Index | Measures both richness and evenness of classes. | Landscape |

---

## How it Works: Local Processing Engine

Standard GEE operations are excellent for pixel-level math, but calculating **patch-based metrics** (like Number of Patches) can be extremely slow or hit memory limits on GEE servers because it requires connected-component analysis on large grids.

**GeeAdvance** solves this by:

1. Downloading a temporary GeoTIFF of your study area using `download_large_area`.
2. Using **`rasterio`** and **`scipy.ndimage`** to perform fast, local patch labeling and geometry calculations.
3. Returning the results as a clean **Pandas DataFrame**.

### Basic Usage

```python
import ee
import geeadvance

# Initialize
geeadvance.initialize(project='your-project-id')

# Load your land cover
lc = ee.Image("ESA/WorldCover/v100").select('Map')
roi = ee.Geometry.BBox(77.5, 12.9, 77.6, 13.0)

# Calculate all available metrics
# This handles the download and local processing automatically
df = geeadvance.calculate_metrics(lc, roi, scale=100)

print(df)
```

### Understanding the Output

The output is a DataFrame where each row represents a land cover class:

| class | ca | pland | np | area_mn | te | ed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | 450.2 | 45.0 | 12 | 37.5 | 12400 | 12.4 |
| 20 | 549.8 | 55.0 | 8 | 68.7 | 10200 | 10.2 |

- **class**: The pixel value from the GEE image.
- **ca**: Class Area (ha).
- **pland**: Percentage of Landscape (%).
- **np**: Number of Patches.
- **area_mn**: Mean Patch Area (ha).
- **te**: Total Edge (m).
- **ed**: Edge Density (m/ha).

---

## Metric Selection

By default, `calculate_metrics` computes all available metrics. You can select specific categories if needed (coming in future updates).

## Tips for Better Results

1. **Scale Matters**: Metics are highly sensitive to resolution. Calculating metrics at 30m vs 100m will yield very different results for `NP` (Number of Patches) and `TE` (Total Edge). Always report your scale!
2. **Region Size**: For very large regions, the temporary TIFF download might take a few minutes. Use a coarser `scale` if appropriate for your research goals.
3. **NoData Values**: GeeAdvance automatically masks out NoData values during calculation to ensure they don't affect `PLAND` or `SHDI`.
