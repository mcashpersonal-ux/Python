# Hatchling — modern build backend

> Hatchling builds Python wheels and source distributions from PEP 621 metadata in `pyproject.toml`.

## Minimal project metadata

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example-package"
version = "0.1.0"
description = "An example package"
requires-python = ">=3.11"
```

Build with `python -m build`. Use a unique distribution name, include a license and README, and test the wheel in a clean environment. Do not place credentials or local absolute paths in package metadata.

## Release checklist

Run the test suite, inspect `dist/`, run `python -m twine check dist/*`, and publish to TestPyPI before the real index. Version changes should be reviewed because released versions cannot be replaced safely.

Next door: [build](104-build.md).
