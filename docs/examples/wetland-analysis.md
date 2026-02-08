# Example: Wetland Connectivity Analysis

This example demonstrates how to evaluate the connectivity and aggregation of herbaceous wetlands using the ESA WorldCover dataset.

## 1. Setup

```python
import ee
import geeadvance

geeadvance.initialize(project='spatialgeography')
```

## 2. Define Wetland Region

We will focus on the Chilika Lake region in Odisha, India.

```python
roi = geeadvance.create_bbox(85.0, 19.5, 85.6, 20.0)
landcover = geeadvance.load_dataset('ESA/WorldCover/v100', region=roi)

# Herbaceous wetland is class 90
wetlands = landcover.select('Map').eq(90)
```

## 3. Connectivity Metrics

For wetlands, metrics like **AREA_MN** (Mean Patch Area) and **ED** (Edge Density) are vital indicators of habitat health.

```python
metrics = geeadvance.calculate_metrics(wetlands, roi, scale=100)
print(metrics)
```

---
*Note: This is a simplified example. For professional wetland analysis, consider integrating seasonal surface water data from the JRC Global Surface Water dataset.*
