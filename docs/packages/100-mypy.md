# mypy — static type checking

> mypy checks whether annotated Python code is used consistently before runtime.

## Install and run

```bash
python -m pip install mypy
python -m mypy src
```

```python
from typing import Sequence

def total(values: Sequence[float]) -> float:
    return sum(values)
```

Use annotations at module and service boundaries first. Treat `Any` as an explicit escape hatch and keep third-party stubs current when possible.

## Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
```

Adopt strictness incrementally for an existing codebase. Static checks complement runtime validation; they do not replace it.

Next door: [Ruff](099-ruff.md).
