# Black — opinionated formatting

> Black reformats Python code consistently so style debates and noisy diffs decrease.

## Install and run

```bash
python -m pip install black
python -m black src tests
```

Run Black on a branch and review the diff. It changes formatting, not program intent, but line wrapping can expose places where code should be simplified.

## Check in CI

```bash
python -m black --check src tests
```

Pin the formatter version for stable diffs and avoid running multiple formatters over the same files without a deliberate policy.

Next door: [Ruff](ruff.md), which can format and lint in one tool.
