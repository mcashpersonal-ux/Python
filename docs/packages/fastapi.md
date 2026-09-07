# FastAPI — typed HTTP APIs

> FastAPI builds ASGI APIs from Python type hints, with validation and OpenAPI documentation generated from the route definitions.

## Install and run

```bash
python -m pip install fastapi uvicorn
```

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Reading(BaseModel):
    sensor: str
    value: float

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/readings", response_model=Reading)
def create_reading(reading: Reading) -> Reading:
    return reading
```

Save as `main.py`, then run `python -m uvicorn main:app --reload` for local development. Visit `/docs` to inspect the generated OpenAPI UI. Disable reload and configure a production process manager for deployment.

## Boundaries and safety

Validate input models, authenticate requests, authorize each resource, and set request-size and timeout limits at the deployment layer. Never expose development debug settings or secrets in response models.

Next door: [Uvicorn](uvicorn.md), [Pydantic](pydantic.md), and [SQLAlchemy](sqlalchemy.md).
