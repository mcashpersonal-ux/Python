# build — standard Python distributions

> The `build` package creates source distributions and wheels through the PEP 517 build interface.

## Install and build

```bash
python -m pip install build
python -m build
```

The command reads `pyproject.toml` and writes artifacts to `dist/`. Inspect the generated wheel contents and test installation in a clean virtual environment before publishing.

## Validate artifacts

```bash
python -m pip install twine
python -m twine check dist/*
```

Uploading is an external, potentially irreversible action. Use TestPyPI first, protect credentials, and confirm the package name and version before publishing.

Next door: [Hatchling](105-hatchling.md) for a build backend.
