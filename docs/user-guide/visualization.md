# Visualization Guide

Visualization is a critical step in landscape ecology to verify that your land cover classifications and region boundaries are correct before running intensive metrics. **GeeAdvance** works seamlessly with **geemap** to provide interactive mapping capabilities.

## Interactive Mapping with geemap

GeeAdvance uses `geemap` as its primary visualization engine choice for Jupyter environments.

### Basic Setup

```python
import geemap
import geeadvance

# Initialize GEE first
geeadvance.initialize(project='your-project')

# Create a map centered on your ROI
roi = geeadvance.create_bbox(75.5, 12.3, 75.7, 12.5)
Map = geemap.Map()
Map.centerObject(roi, zoom=11)
Map.addLayer(roi, {'color': 'red'}, 'Study Area Border')
Map
```

## Visualizing Land Cover

Most land cover products have predefined palettes. You can apply these to make your maps professional.

### Example: ESA WorldCover

```python
lc = geeadvance.load_dataset('ESA/WorldCover/v100', region=roi)

# WorldCover visualization parameters
vis_params = {
    'bands': ['Map'],
    'min': 10,
    'max': 100,
    'palette': [
        '006400', 'ffbb22', 'ffff4c', 'f096ff', 'fa0000',
        'b4b4b4', 'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0'
    ]
}

Map.addLayer(lc, vis_params, 'ESA Land Cover')
```

## Split-Panel Comparison

One of the most powerful visualization tools is the split-panel map, useful for comparing land cover change over time.

```python
# Load MODIS land cover for two different years
lc_2001 = geeadvance.load_dataset('MODIS/006/MCD12Q1', start_date='2001-01-01')
lc_2020 = geeadvance.load_dataset('MODIS/006/MCD12Q1', start_date='2020-01-01')

# Define simple visualization
modis_vis = {'min': 1, 'max': 17, 'palette': 'gist_earth'}

# Create split map
Map = geemap.Map()
left_layer = geemap.ee_tile_layer(lc_2001.select('LC_Type1'), modis_vis, '2001')
right_layer = geemap.ee_tile_layer(lc_2020.select('LC_Type1'), modis_vis, '2020')

Map.split_map(left_layer, right_layer)
Map
```

## Adding Legends and Colorbars

Legends make your analysis interpretable by others.

```python
Map = geemap.Map()
Map.addLayer(lc, vis_params, 'Land Cover')

# Add a categorical legend for ESA WorldCover
# Note: You can customize labels based on gait.get_landcover_classes
Map.add_legend(title="Land Cover Type", builtin_legend='ESA_WorldCover')
Map
```

## Visualizing Patches Locally

After using `calculate_metrics()`, you might want to see the discrete patches identified by the local processing engine.

```python
# This is coming in future updates: 
# The local engine will soon support returning patch-labeled rasters 
# that you can overlay back onto GEE maps.
```

## Summary Table

| Feature | Function | Environment |
| :--- | :--- | :--- |
| Interactive Zoom | `geemap.Map()` | Jupyter / Colab |
| Layer Control | `Map.addLayer()` | Jupyter / Colab |
| Time Slider | `Map.add_time_slider()` | Jupyter / Colab |
| Inspector Tool | `Map.inspector_tool()` | Jupyter / Colab |
| Export Map to HTML | `Map.to_html()` | Local Python |
