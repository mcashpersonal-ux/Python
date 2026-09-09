# Starlette — lightweight ASGI toolkit

> Starlette supplies routing, middleware, requests, responses, WebSockets, and background-task primitives for ASGI applications.

## Install and run

```bash
python -m pip install starlette uvicorn
```

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def health(request):
    return JSONResponse({"status": "ok"})

app = Starlette(routes=[Route("/health", health)])
```

Run with `python -m uvicorn main:app`. Add authentication, validation, trusted-host checks, and error handling as middleware or at the application boundary; Starlette intentionally stays small.

Next door: [FastAPI](086-fastapi.md) for typed validation and generated API schemas.
