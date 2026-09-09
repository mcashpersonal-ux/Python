# isort — import ordering

> isort sorts and groups Python imports according to a consistent convention.

## Install and run

```bash
python -m pip install isort
python -m isort src tests
```

Use `python -m isort --check-only src tests` in CI. Configure the project profile to match the formatter, for example `profile = "black"`, and review changes to first-party module detection.

Import sorting does not validate unused imports or runtime availability; pair it with a linter and tests.

Next door: [Black](101-black.md) and [Ruff](099-ruff.md).
