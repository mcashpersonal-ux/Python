# Pydantic — validated data models

> Pydantic validates Python data against type annotations and produces clear errors for invalid input.

## Install and define a model

```bash
python -m pip install pydantic
```

```python
from pydantic import BaseModel, Field

class Reading(BaseModel):
    sensor: str
    value: float = Field(ge=0)

reading = Reading.model_validate({"sensor": "line1", "value": "23.4"})
print(reading.value)  # 23.4
```

Pydantic may coerce compatible input, such as a numeric string to a float. Use strict types when coercion would hide caller mistakes.

## Validation errors

```python
from pydantic import ValidationError

try:
    Reading.model_validate({"sensor": "line1", "value": -1})
except ValidationError as exc:
    print(exc.errors())
```

Treat validation as a boundary. Do not assume that validated input authorizes an operation; authorization and business rules remain separate concerns.

Next door: FastAPI uses Pydantic models for request and response schemas; its
dedicated guide will be added in the web-frameworks section.
