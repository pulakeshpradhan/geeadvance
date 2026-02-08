# GeeAdvance Tutorials

Welcome to the GeeAdvance tutorial series! These tutorials are designed for beginners and will guide you through all aspects of landscape metrics analysis using Google Earth Engine.

## Tutorial Series

### 1. [Authentication](01_authentication.ipynb)

**Duration**: 10 minutes  
**Level**: Beginner

Learn how to:

- Authenticate with Google Earth Engine
- Initialize the GEE API
- Verify your connection
- Troubleshoot common issues

### 2. Loading and Visualizing Data

**Duration**: 15 minutes  
**Level**: Beginner

Topics covered:

- Loading GEE datasets
- Filtering by date and region
- Common land cover datasets
- Visualizing with geemap

### 3. Area and Edge Metrics

**Duration**: 20 minutes  
**Level**: Beginner

Learn to calculate:

- Class Area (CA)
- Percentage of Landscape (PLAND)
- Total Edge (TE)
- Edge Density (ED)

### 4. Shape and Core Metrics

**Duration**: 20 minutes  
**Level**: Intermediate

Topics:

- Shape Index (SHAPE)
- Fractal Dimension (FRAC)
- Core Area metrics
- Perimeter-Area Ratio

### 5. Aggregation and Diversity Metrics

**Duration**: 25 minutes  
**Level**: Intermediate

Learn about:

- Aggregation Index (AI)
- Clumpiness (CLUMPY)
- Shannon's Diversity (SHDI)
- Simpson's Diversity (SIDI)

### 6. Exporting Data

**Duration**: 15 minutes  
**Level**: Beginner

Export methods:

- Export to Google Drive
- Export to GEE Assets
- Direct downloads
- Batch exports

### 7. [Complete Workflow](07_complete_workflow.ipynb)

**Duration**: 30 minutes  
**Level**: All levels

A complete end-to-end example:

- Define study area
- Load land cover data
- Calculate all metrics
- Download large areas with geemap
- Visualize results
- Export everything

## Running the Tutorials

### Option 1: Jupyter Notebook

```bash
# Install Jupyter
pip install jupyter

# Navigate to tutorials directory
cd tutorials

# Start Jupyter
jupyter notebook
```

### Option 2: JupyterLab

```bash
# Install JupyterLab
pip install jupyterlab

# Start JupyterLab
jupyter lab
```

### Option 3: Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. File → Open Notebook → GitHub
3. Enter: `pulakeshpradhan/geeadvance`
4. Select a tutorial

### Option 4: VS Code

1. Install Python extension
2. Install Jupyter extension
3. Open `.ipynb` file
4. Click "Run All"

## Prerequisites

Before starting the tutorials:

1. **Python 3.8+** installed
2. **GeeAdvance** installed: `pip install geeadvance`
3. **Google Earth Engine access** (sign up at <https://earthengine.google.com/>)
4. **Jupyter** installed (for local use)

## Learning Path

### For Complete Beginners

1. Start with Tutorial 1 (Authentication)
2. Follow tutorials in order
3. Complete all exercises
4. Review the complete workflow (Tutorial 7)

### For GEE Users

1. Quick review of Tutorial 1
2. Focus on Tutorials 3-5 (metrics)
3. Learn about large downloads (Tutorial 6)
4. Study the complete workflow

### For Landscape Ecologists

1. Skim Tutorial 1-2
2. Deep dive into Tutorials 3-5
3. Compare with R landscapemetrics
4. Adapt workflows to your needs

## Additional Resources

### Documentation

- [Full Documentation](https://pulakeshpradhan.github.io/geeadvance/)
- [API Reference](https://pulakeshpradhan.github.io/geeadvance/api/auth/)
- [User Guide](https://pulakeshpradhan.github.io/geeadvance/user-guide/landscape-metrics/)

### Examples

- [Forest Fragmentation](../docs/examples/forest-fragmentation.md)
- [Urban Growth Analysis](../docs/examples/urban-growth.md)
- [Wetland Assessment](../docs/examples/wetland-analysis.md)

### External Resources

- [Google Earth Engine Guides](https://developers.google.com/earth-engine/guides)
- [Geemap Documentation](https://geemap.org/)
- [Landscapemetrics R Package](https://r-spatialecology.github.io/landscapemetrics/)

## Exercises

Each tutorial includes exercises. Solutions are provided in the `solutions/` directory.

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/pulakeshpradhan/geeadvance/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pulakeshpradhan/geeadvance/discussions)
- **Email**: <pulakesh.mid@gmail.com>

## Contributing

Found an error or have a suggestion? Please:

1. Open an issue
2. Submit a pull request
3. Share your own tutorials

## License

These tutorials are part of the GeeAdvance project and are licensed under the MIT License.

---

**Happy Learning!** 🎓🌍
