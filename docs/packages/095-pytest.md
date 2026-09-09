# pytest — Python testing

> pytest discovers tests, provides fixtures and parametrization, and reports failures with concise context.

## Install and run

```bash
python -m pip install pytest
python -m pytest
```

```python
# test_math.py
def add(a: int, b: int) -> int:
    return a + b

def test_add() -> None:
    assert add(2, 3) == 5
```

Keep production code and tests in separate modules. Prefer behavior-focused tests and run the complete suite before publishing a change.

## Fixtures and approximate values

```python
import pytest

@pytest.mark.parametrize("value", [0.1, 0.2])
def test_value(value: float) -> None:
    assert value == pytest.approx(value)
```

Use `tmp_path`, `monkeypatch`, and fixtures for isolated setup. Do not make unit tests depend on live databases or external APIs unless they are explicitly marked integration tests.

Next door: [pytest-cov](096-pytest-cov.md) for coverage.
