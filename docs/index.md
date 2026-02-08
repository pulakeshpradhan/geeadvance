# Welcome to GeeAdvance

<div align="center">

![GeeAdvance Logo](assets/logo.png)

**Advanced Landscape Metrics for Google Earth Engine**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/pulakeshpradhan/geeadvance/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg)](https://pulakeshpradhan.github.io/geeadvance/)

</div>

## Overview

**GeeAdvance** is a comprehensive Python package that brings advanced landscape ecology metrics to Google Earth Engine. Inspired by the R [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/) package, it enables researchers, students, and practitioners to perform sophisticated spatial pattern analysis on GEE-derived imagery and datasets.

## Key Features

### 🔐 **Seamless GEE Authentication**

Standard authentication methods that work across different environments (local, Colab, cloud).

### 📊 **Comprehensive Landscape Metrics**

Implementation of metrics from the landscapemetrics R package:

- **Area & Edge Metrics**: CA, PLAND, TE, ED
- **Shape Metrics**: SHAPE, FRAC, PARA, CIRCLE
- **Core Area Metrics**: TCA, CPLAND, CAI
- **Aggregation Metrics**: AI, CLUMPY, COHESION, DIVISION
- **Diversity Metrics**: SHDI, SHEI, SIDI

### 🗺️ **Direct GEE Integration**

Work directly with GEE ImageCollections and Images without downloading data first.

### 📥 **Smart Downloads with Geemap**

Download large areas without size errors using automatic tiling and merging.

### 📚 **Beginner-Friendly**

Extensive tutorials and documentation designed for users new to GEE and landscape ecology.

## Quick Example

```python
import ee
import geeadvance

# Authenticate and initialize
ee.Authenticate()
ee.Initialize(project='your-project-id')

# Define region of interest
roi = geeadvance.create_bbox(77.0, 20.0, 78.0, 21.0)

# Load land cover data
landcover = geeadvance.load_dataset('ESA/WorldCover/v100', region=roi)

# Calculate landscape metrics
metrics = geeadvance.calculate_metrics(landcover, roi, scale=100)

# Download large area (with automatic tiling)
geeadvance.download_large_area(
    landcover,
    roi,
    'landcover.tif',
    scale=100
)

print(metrics)
```

## Installation

```bash
pip install geeadvance
```

Or install from source:

```bash
git clone https://github.com/pulakeshpradhan/geeadvance.git
cd geeadvance
pip install -e .
```

## Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation and setup
- **[Tutorials](tutorials/01_authentication.ipynb)**: Step-by-step guides for beginners
- **[User Guide](user-guide/landscape-metrics.md)**: In-depth explanations
- **[API Reference](api/auth.md)**: Complete API documentation
- **[Examples](examples/forest-fragmentation.md)**: Real-world use cases

## Use Cases

### 🌲 Forest Fragmentation Analysis

Analyze forest patch connectivity and fragmentation patterns.

### 🏙️ Urban Growth Monitoring

Track urban expansion and landscape transformation.

### 🌾 Agricultural Landscape Assessment

Evaluate agricultural landscape diversity and structure.

### 💧 Wetland Characterization

Assess wetland patch dynamics and connectivity.

## Why GeeAdvance?

| Feature | GeeAdvance | Traditional Approach |
|---------|------------|---------------------|
| **Data Access** | Direct GEE integration | Manual download required |
| **Large Areas** | Automatic tiling | Size limitations |
| **Metrics** | 30+ landscape metrics | Manual calculation |
| **Learning Curve** | Beginner-friendly | Steep |
| **Speed** | Cloud computing | Local processing |

## Author

**Pulakesh Pradhan**

- Email: [pulakesh.mid@gmail.com](mailto:pulakesh.mid@gmail.com)
- GitHub: [@pulakeshpradhan](https://github.com/pulakeshpradhan)

## Acknowledgments

- Inspired by the R [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/) package
- Built on [Google Earth Engine](https://earthengine.google.com/)
- Uses [geemap](https://geemap.org/) for enhanced functionality

## Citation

If you use GeeAdvance in your research, please cite:

```bibtex
@software{geeadvance2026,
  author = {Pradhan, Pulakesh},
  title = {GeeAdvance: Landscape Metrics for Google Earth Engine},
  year = {2026},
  url = {https://github.com/pulakeshpradhan/geeadvance}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](about/license.md) file for details.

## Support

- 📖 [Documentation](https://pulakeshpradhan.github.io/geeadvance/)
- 🐛 [Issue Tracker](https://github.com/pulakeshpradhan/geeadvance/issues)
- 💬 [Discussions](https://github.com/pulakeshpradhan/geeadvance/discussions)

---

<div align="center">

**Made with ❤️ for the landscape ecology community**

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[View on GitHub](https://github.com/pulakeshpradhan/geeadvance){ .md-button }

</div>
