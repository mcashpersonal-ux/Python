# python-dotenv — local environment files

> python-dotenv loads key-value pairs from a `.env` file into `os.environ`, which is useful for local development.

## Install and load

```bash
python -m pip install python-dotenv
```

```python
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.environ["DATABASE_URL"]
```

Keep `.env` out of version control and commit a `.env.example` containing names but no real values. In production, prefer the deployment platform's secret store and make missing required values fail fast.

## Explicit path

```python
from dotenv import load_dotenv

load_dotenv(".env.local", override=False)
```

The default does not overwrite an already-set environment variable. Treat environment variables as strings and validate or convert them at the application boundary.

Next door: [Pydantic](pydantic.md) for typed settings validation.
