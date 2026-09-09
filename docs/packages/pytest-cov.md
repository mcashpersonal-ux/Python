# pytest-cov — test coverage

> pytest-cov integrates Coverage.py with pytest to show which lines and branches tests execute.

## Install and run

```bash
python -m pip install pytest pytest-cov
python -m pytest --cov=src --cov-report=term-missing
```

Coverage identifies untested code; it does not prove that assertions are meaningful. Review uncovered error paths and add tests for important behavior rather than optimizing only for a percentage.

## Reports

```bash
python -m pytest --cov=src --cov-report=html
```

Open `htmlcov/index.html` locally. Do not publish reports containing source or personal data without checking access controls.

Next door: [pytest](pytest.md).
