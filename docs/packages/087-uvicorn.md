# Uvicorn — ASGI server

> Uvicorn runs ASGI applications such as FastAPI and Starlette using an event loop and HTTP protocol implementation.

## Install and run

```bash
python -m pip install uvicorn
python -m uvicorn myapp:app --host 127.0.0.1 --port 8000
```

`myapp:app` means the `app` object in `myapp.py`. Use `--reload` only for local development. Bind to `0.0.0.0` only when a trusted reverse proxy or network policy protects the service.

## Configuration

```python
# myapp.py
from fastapi import FastAPI

app = FastAPI()
```

Production deployments should define worker, proxy, TLS, access-log, health-check, and graceful-shutdown policies explicitly. Uvicorn is a server, not an authentication or authorization layer.

Next door: [FastAPI](086-fastapi.md) and [Starlette](090-starlette.md).
