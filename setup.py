"""
GeeAdvance - Landscape Metrics for Google Earth Engine
Author: Pulakesh Pradhan
Email: pulakesh.mid@gmail.com
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geeadvance",
    version="0.1.0",
    author="Pulakesh Pradhan",
    author_email="pulakesh.mid@gmail.com",
    description="Advanced landscape metrics analysis using Google Earth Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pulakeshpradhan/geeadvance",
    project_urls={
        "Bug Tracker": "https://github.com/pulakeshpradhan/geeadvance/issues",
        "Documentation": "https://pulakeshpradhan.github.io/geeadvance/",
        "Source Code": "https://github.com/pulakeshpradhan/geeadvance",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "earthengine-api>=0.1.350",
        "geemap>=0.20.0",
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "geopandas>=0.10.0",
        "rasterio>=1.2.0",
        "shapely>=1.8.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "requests>=2.26.0",
        "tqdm>=4.62.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.6b0",
            "flake8>=3.9.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
        "docs": [
            "mkdocs>=1.2.0",
            "mkdocs-material>=8.0.0",
            "mkdocstrings>=0.18.0",
            "mkdocs-jupyter>=0.20.0",
        ],
    },
    keywords="google-earth-engine gee landscape-metrics spatial-analysis remote-sensing",
    include_package_data=True,
)
