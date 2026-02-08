# Example: Urban Growth Monitoring

This example demonstrates how to track the spatial expansion and fragmentation of urban areas using MODIS Land Cover data.

## 1. Setup

```python
import ee
import geeadvance

geeadvance.initialize(project='spatialgeography')
```

## 2. Prepare Multi-Temporal Data

We will analyze the expansion of Bangalore, India between 2001 and 2020.

```python
roi = geeadvance.create_bbox(77.4, 12.8, 77.8, 13.1)

# Load MODIS LC for two years
lc_2001 = geeadvance.load_dataset('MODIS/006/MCD12Q1', start_date='2001-01-01')
lc_2020 = geeadvance.load_dataset('MODIS/006/MCD12Q1', start_date='2020-01-01')

# Extract Urban class (ID 13 in MODIS)
urban_2001 = lc_2001.select('LC_Type1').eq(13)
urban_2020 = lc_2020.select('LC_Type1').eq(13)
```

## 3. Calculate Landscape Metrics

Urban growth often leads to **infills** (lower NP) or **sprawls** (higher NP and higher TE).

```python
metrics_2001 = geeadvance.calculate_metrics(urban_2001, roi, scale=500)
metrics_2020 = geeadvance.calculate_metrics(urban_2020, roi, scale=500)

# Compare PLAND (Percent of Landscape) and NP (Number of Patches)
print(f"Urban % 2001: {metrics_2001['pland'].values[1]}%")
print(f"Urban % 2020: {metrics_2020['pland'].values[1]}%")
```

## 4. Analysis

By comparing the `PLAND` and `NP` over time, urban planners can determine if the city is growing compactly or through fragmented sprawl.
