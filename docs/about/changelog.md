# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-08

### Added

- Initial release of GeeAdvance
- Standard GEE authentication module with multiple auth modes
- Comprehensive dataset loading and management
- Landscape metrics implementation:
  - Area and Edge metrics
  - Shape metrics
  - Core area metrics
  - Aggregation metrics
  - Diversity metrics
- Export functionality to GeoTIFF, GeoJSON, Drive, and Assets
- **Large area download support with geemap tiling**
- Automatic tiling and merging for areas exceeding GEE size limits
- Download size estimation and recommendations
- Utility functions for common GEE operations
- Vegetation indices calculation (NDVI, EVI)
- Comprehensive tutorials for beginners:
  - Authentication tutorial
  - Complete workflow example
- Full documentation with MkDocs and Material theme
- GitHub Pages deployment configuration
- 30+ landscape metrics from landscapemetrics R package
- Support for common GEE datasets (MODIS, ESA WorldCover, Sentinel, Landsat)

### Features

- 🔐 Multiple authentication methods (notebook, Colab, gcloud, service account)
- 📥 Download large areas without size errors using geemap
- 📊 Calculate comprehensive landscape metrics
- 🗺️ Direct GEE integration without local downloads
- 📚 Beginner-friendly tutorials and documentation
- 🚀 Fast cloud-based processing

### Documentation

- Complete API reference
- 7 beginner tutorials
- User guides for all major features
- Real-world examples
- Troubleshooting guides

## [Unreleased]

### Planned

- Additional landscape metrics
- Temporal analysis capabilities
- Interactive visualization tools
- More example workflows
- Performance optimizations
- Unit tests and CI/CD

---

[0.1.0]: https://github.com/pulakeshpradhan/geeadvance/releases/tag/v0.1.0
