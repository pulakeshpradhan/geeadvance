# Installation

## Requirements

- Python 3.8 or higher
- Google account with Earth Engine access
- pip package manager

## Step 1: Install Python

If you don't have Python installed:

### Windows

Download from [python.org](https://www.python.org/downloads/) and run the installer.

### macOS

```bash
brew install python3
```

### Linux

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## Step 2: Get Earth Engine Access

1. Go to [https://earthengine.google.com/](https://earthengine.google.com/)
2. Click "Sign Up"
3. Sign in with your Google account
4. Wait for approval (usually instant for non-commercial use)

## Step 3: Install GeeAdvance

### Using pip (Recommended)

```bash
pip install geeadvance
```

### From Source

```bash
git clone https://github.com/pulakeshpradhan/geeadvance.git
cd geeadvance
pip install -e .
```

### In a Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv geeadvance-env

# Activate it
# On Windows:
geeadvance-env\Scripts\activate
# On macOS/Linux:
source geeadvance-env/bin/activate

# Install geeadvance
pip install geeadvance
```

## Step 4: Verify Installation

```python
import geeadvance as ga
print(f"GeeAdvance version: {ga.__version__}")
```

Expected output:

```
GeeAdvance version: 0.1.0
```

## Optional Dependencies

### For Jupyter Notebooks

```bash
pip install jupyter notebook
```

### For Development

```bash
pip install geeadvance[dev]
```

### For Documentation

```bash
pip install geeadvance[docs]
```

## Troubleshooting

### Import Error

**Problem**: `ModuleNotFoundError: No module named 'geeadvance'`

**Solution**:

```bash
pip install --upgrade geeadvance
```

### Permission Error

**Problem**: `Permission denied` during installation

**Solution**:

```bash
pip install --user geeadvance
```

### Dependency Conflicts

**Problem**: Conflicts with existing packages

**Solution**: Use a virtual environment (see above)

## Next Steps

- [Authenticate with GEE](authentication.md)
- [Quick Start Guide](quickstart.md)
- [First Tutorial](../tutorials/01_authentication.ipynb)

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.10+ |
| RAM | 4 GB | 8 GB+ |
| Disk Space | 500 MB | 2 GB+ |
| Internet | Required | High-speed |
