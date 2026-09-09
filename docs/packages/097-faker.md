# Faker — realistic test data

> Faker generates deterministic-looking names, addresses, dates, and other data for tests and development fixtures.

## Install and use

```bash
python -m pip install faker
```

```python
from faker import Faker

fake = Faker()
print(fake.name())
print(fake.email())
```

## Reproducible data

```python
from faker import Faker

fake = Faker()
Faker.seed(1234)
print(fake.uuid4())
```

Seeds make tests repeatable, but generated data is not a security primitive and is not guaranteed to represent every real-world edge case. Never send fake-looking data to a production system by accident.

Next door: [pytest](095-pytest.md).
