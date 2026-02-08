# 🌍 GeeAdvance

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://pulakeshpradhan.github.io/geeadvance/)

**GeeAdvance** is a Python package for advanced landscape metrics analysis using Google Earth Engine (GEE). It implements landscape ecology metrics similar to the R [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/) package, enabling comprehensive spatial pattern analysis of GEE-derived imagery and datasets.

## 🚀 Features

- **🔐 Standard GEE Authentication** - Seamless integration with Google Earth Engine
- **📊 Comprehensive Landscape Metrics** - Implementation of metrics from landscapemetrics
  - Area & Edge Metrics
  - Shape Metrics
  - Core Area Metrics
  - Aggregation Metrics
  - Diversity Metrics
- **🗺️ GEE Integration** - Direct analysis of GEE imagery and datasets
- **📥 Export Capabilities** - Download results as GeoTIFF and other formats
- **📚 Beginner-Friendly** - Extensive tutorials and documentation

## 📦 Installation

```bash
pip install geeadvance
```

Or install from source:

```bash
git clone https://github.com/pulakeshpradhan/geeadvance.git
cd geeadvance
pip install -e .
```

## 🔑 Quick Start

### 1. Authenticate with Google Earth Engine

```python
import ee
import geeadvance

# Standard GEE authentication
ee.Authenticate()
ee.Initialize(project='your-project-id')
```

### 2. Calculate Landscape Metrics

```python
# Load a land cover dataset
dataset = geeadvance.load_dataset('MODIS/006/MCD12Q1', 
                                  start_date='2020-01-01',
                                  end_date='2020-12-31')

# Define region of interest
roi = ee.Geometry.Rectangle([77.0, 20.0, 78.0, 21.0])

# Calculate landscape metrics
metrics = geeadvance.calculate_metrics(dataset, roi, scale=500)

# Get specific metrics
area_metrics = geeadvance.area_metrics(dataset, roi)
shape_metrics = geeadvance.shape_metrics(dataset, roi)
diversity_metrics = geeadvance.diversity_metrics(dataset, roi)

print(metrics)
```

### 3. Export Results

```python
# Export as GeoTIFF
geeadvance.export_tif(dataset, roi, 'output_landcover.tif')

# Export metrics as CSV
metrics.to_csv('landscape_metrics.csv')
```

## 📖 Documentation

Full documentation is available at: [https://pulakeshpradhan.github.io/geeadvance/](https://pulakeshpradhan.github.io/geeadvance/)

## 🎓 Tutorials

Check out our beginner-friendly tutorials:

1. [Getting Started with GEE Authentication](tutorials/01_authentication.ipynb)
2. [Loading and Visualizing GEE Datasets](tutorials/02_loading_data.ipynb)
3. [Calculating Area and Edge Metrics](tutorials/03_area_edge_metrics.ipynb)
4. [Shape and Core Metrics](tutorials/04_shape_core_metrics.ipynb)
5. [Aggregation and Diversity Metrics](tutorials/05_aggregation_diversity.ipynb)
6. [Exporting Data and Results](tutorials/06_exporting_data.ipynb)
7. [Complete Workflow Example](tutorials/07_complete_workflow.ipynb)

## 🌟 Implemented Metrics

### Area & Edge Metrics

- **CA** - Class Area
- **PLAND** - Percentage of Landscape
- **TE** - Total Edge
- **ED** - Edge Density

### Shape Metrics

- **SHAPE** - Shape Index
- **FRAC** - Fractal Dimension
- **PARA** - Perimeter-Area Ratio
- **CIRCLE** - Related Circumscribing Circle

### Core Area Metrics

- **TCA** - Total Core Area
- **CPLAND** - Core Area Percentage of Landscape
- **CAI** - Core Area Index

### Aggregation Metrics

- **AI** - Aggregation Index
- **CLUMPY** - Clumpiness Index
- **COHESION** - Patch Cohesion Index
- **DIVISION** - Landscape Division Index

### Diversity Metrics

- **SHDI** - Shannon's Diversity Index
- **SHEI** - Shannon's Evenness Index
- **SIDI** - Simpson's Diversity Index

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Pulakesh Pradhan**

- Email: <pulakesh.mid@gmail.com>
- GitHub: [@pulakeshpradhan](https://github.com/pulakeshpradhan)

## 🙏 Acknowledgments

- Inspired by the R [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/) package
- Built on [Google Earth Engine](https://earthengine.google.com/)

## 📚 Citation

If you use this package in your research, please cite:

```bibtex
@software{geeadvance2026,
  author = {Pradhan, Pulakesh},
  title = {GeeAdvance: Landscape Metrics for Google Earth Engine},
  year = {2026},
  url = {https://github.com/pulakeshpradhan/geeadvance}
}
```
