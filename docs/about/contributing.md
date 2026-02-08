# Contributing to GeeAdvance

Thank you for your interest in contributing to GeeAdvance! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Report Bugs

Found a bug? Please create an issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 2. Suggest Features

Have an idea? Open an issue with:

- Clear description of the feature
- Use case and benefits
- Possible implementation approach

### 3. Improve Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples
- Improve tutorials
- Translate documentation

### 4. Submit Code

#### Getting Started

1. Fork the repository
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/geeadvance.git
   cd geeadvance
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

5. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to all functions
- Include type hints where appropriate

Example:

```python
def calculate_metric(
    image: ee.Image,
    region: ee.Geometry,
    scale: int = 30,
) -> Dict:
    """
    Calculate a landscape metric.
    
    Parameters
    ----------
    image : ee.Image
        Input image
    region : ee.Geometry
        Region of interest
    scale : int, optional
        Scale in meters (default: 30)
    
    Returns
    -------
    dict
        Calculated metrics
    """
    # Implementation
    pass
```

#### Testing

Before submitting:

1. Test your code:

   ```bash
   pytest tests/
   ```

2. Check code style:

   ```bash
   flake8 geeadvance/
   black geeadvance/
   ```

3. Update documentation if needed

#### Commit Messages

Use clear, descriptive commit messages:

```
Add feature: implement SHDI diversity metric

- Implement Shannon's Diversity Index calculation
- Add unit tests for SHDI
- Update documentation with examples
```

#### Pull Request Process

1. Update the README.md if needed
2. Update documentation
3. Ensure all tests pass
4. Submit pull request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if applicable)

### 5. Add Examples

Real-world examples are valuable:

- Create Jupyter notebooks
- Document use cases
- Share workflows

## Development Setup

### Project Structure

```
geeadvance/
├── geeadvance/          # Main package
│   ├── __init__.py
│   ├── auth.py          # Authentication
│   ├── datasets.py      # Dataset management
│   ├── metrics.py       # Landscape metrics
│   ├── export.py        # Export functions
│   ├── download.py      # Large area downloads
│   └── utils.py         # Utilities
├── docs/                # Documentation
├── tutorials/           # Tutorial notebooks
├── tests/               # Unit tests
├── setup.py            # Package setup
└── mkdocs.yml          # Documentation config
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_metrics.py

# Run with coverage
pytest --cov=geeadvance tests/
```

### Building Documentation

```bash
# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing others' private information
- Other unprofessional conduct

## Questions?

- Open an issue for questions
- Email: <pulakesh.mid@gmail.com>
- Discussions: [GitHub Discussions](https://github.com/pulakeshpradhan/geeadvance/discussions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be acknowledged in:

- README.md
- Documentation
- Release notes

Thank you for contributing to GeeAdvance! 🎉
