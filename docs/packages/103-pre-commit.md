# pre-commit — repeatable local checks

> pre-commit runs configured hooks before commits so formatting and fast checks happen consistently across contributors.

## Install and configure

```bash
python -m pip install pre-commit
pre-commit install
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
```

Run all hooks with `pre-commit run --all-files`. Pin hook revisions, review automatic fixes, and update hooks deliberately; hooks execute third-party code on your machine.

Next door: [Ruff](099-ruff.md) and [Black](101-black.md).
