# Contributing to airport-data-python

Thank you for your interest in contributing! This guide covers how to set up your development environment, submit changes, and publish new versions.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Git

### Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/airport-data-python.git
   cd airport-data-python
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate   # Windows
   ```

3. **Install development dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests for any new functionality.

3. Regenerate the compressed data file if you modified `airports/data/airports.json`:
   ```bash
   python scripts/generate_airports_gz.py
   ```

4. Run the test suite:
   ```bash
   python -m pytest tests/ -v --cov=airports --cov-report=term-missing
   ```

5. Build and validate the package:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   python -m build
   twine check dist/*
   ```

6. Commit your changes and push:
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```

7. Open a Pull Request against the `main` branch.

## Code Guidelines

- Follow existing code style and patterns.
- Add unit tests for all new functions and bug fixes.
- Update the README if you add or change public API methods.
- Add an entry to `CHANGELOG.md` under an `[Unreleased]` section.

## Reporting Issues

- Use the [GitHub Issues](https://github.com/aashishvanand/airport-data-python/issues) page.
- Include steps to reproduce, expected behaviour, and actual behaviour.
- Mention your Python version and operating system.

## Publishing a New Version

Publishing is handled by the repository maintainers. The process is as follows:

### 1. Prepare the release

1. Update the version number in `setup.py`:
   ```python
   version="X.Y.Z",
   ```

2. Update `CHANGELOG.md` with the new version, date, and a summary of changes.

3. Commit the version bump:
   ```bash
   git add setup.py CHANGELOG.md
   git commit -m "Bump version to X.Y.Z"
   ```

4. Push to `main` and ensure CI passes.

### 2. Publish to TestPyPI (optional dry run)

1. Trigger the publish workflow manually from the GitHub Actions UI (`workflow_dispatch`).
2. This publishes to [TestPyPI](https://test.pypi.org/p/airports-py).
3. Verify the package installs correctly:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ airports-py==X.Y.Z
   ```

### 3. Publish to PyPI

There are two ways to trigger a production release:

- **GitHub Release (recommended):** Create a new release on GitHub with a tag matching the version (e.g. `v3.1.0`). The publish workflow runs automatically when the release is published.
- **Push to `release` branch:** Merge `main` into the `release` branch. The publish workflow runs automatically on push to `release`.

Both paths run the full test suite across Python 3.10-3.14, build the package, and publish to [PyPI](https://pypi.org/p/airports-py) using trusted publishing (no API tokens needed).

### 4. Verify the release

```bash
pip install --upgrade airports-py
python -c "from airports import airport_data; print(f'Version installed, loaded {len(airport_data.airports)} airports')"
```

## License

By contributing, you agree that your contributions will be licensed under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.
