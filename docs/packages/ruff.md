# Ruff — fast linting and formatting

> Ruff combines a fast Python linter and formatter with a compact configuration surface.

## Install and run

```bash
python -m pip install ruff
python -m ruff check .
python -m ruff format .
```

Start with `ruff check --fix .` only after reviewing the proposed changes. Pin Ruff in a project environment and run it in CI so local formatting is not the only quality gate.

## Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88

target-version = "py311"
```

Treat lint rules as an executable team convention. Avoid enabling broad automatic fixes without checking changes to imports and behavior.

Next door: [mypy](mypy.md) for static type checking.
