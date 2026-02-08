# GEE Datasets Guide

Google Earth Engine (GEE) provides petabytes of geospatial data. **GeeAdvance** simplifies the process of loading and preparing these datasets for landscape analysis.

## Commonly Used Datasets

While GeeAdvance can load any GEE dataset via its ID, the following are specifically recommended for landscape analysis.

### 1. Global Land Cover (High Resolution)

| Dataset ID | Resolution | Period | Best For |
| :--- | :--- | :--- | :--- |
| `ESA/WorldCover/v100` | 10m | 2020 | High-detail local fragmentation studies. |
| `ESA/WorldCover/v200` | 10m | 2021 | Comparing with 2020 for recent changes. |
| `GOOGLE/DYNAMICWORLD/V1` | 10m | 2015-Present | Near real-time land cover monitoring. |

### 2. Global Land Cover (Long Term)

| Dataset ID | Resolution | Period | Best For |
| :--- | :--- | :--- | :--- |
| `MODIS/006/MCD12Q1` | 500m | 2001-Present | Regional/Continental trend analysis. |
| `COPERNICUS/Landcover/100m/Proba-V-C3/Global` | 100m | 2015-2019 | Intermediate resolution time-series. |

---

## Loading Data with `load_dataset`

The `geeadvance.load_dataset()` function is a versatile tool for fetching data. It handles common tasks like filtering by date and clipping to a region.

### Basic Loading

```python
import geeadvance

# Load latest MODIS Land Cover
lc = geeadvance.load_dataset('MODIS/006/MCD12Q1')
```

### Advanced Loading with Filters

```python
# Load Sentinel-2 SR imagery for a specific area and time
s2 = geeadvance.load_dataset(
    'COPERNICUS/S2_SR',
    start_date='2022-01-01',
    end_date='2022-06-30',
    region=roi,
    filter_clouds=True  # Automatically masks out cloudy pixels
)
```

---

## Understanding Class Schemes

Different land cover products use different numeric schemes. GeeAdvance provides a utility to look up these schemes.

```python
classes = geeadvance.get_landcover_classes('ESA/WorldCover/v100')
print(classes)
# Output: {10: 'Trees', 20: 'Shrubland', 30: 'Grassland', ...}
```

### Standard WorldCover Scheme (Value -> Name)

- **10**: Trees
- **20**: Shrubland
- **30**: Grassland
- **40**: Cropland
- **50**: Built-up
- **60**: Bare / sparse vegetation
- **70**: Snow and ice
- **80**: Permanent water bodies
- **90**: Herbaceous wetland
- **95**: Mangroves
- **100**: Moss and lichen

---

## Tips for Landscape Ecology

1. **Temporal Consistency**: When comparing two time periods, ensure you use the same dataset (e.g., MODIS 2005 vs MODIS 2020). Never mix WorldCover and MODIS for trend analysis.
2. **Resolution Masking**: High-resolution datasets (10m) will capture many more small patches than coarse datasets (500m). This significantly impacts metrics like `NP` and `TE`.
3. **Projections**: GeeAdvance utilities like `get_projection()` can help you verify that your data is in a suitable coordinate system for area calculations (though GEE handles most area math in spherical coordinates natively).
