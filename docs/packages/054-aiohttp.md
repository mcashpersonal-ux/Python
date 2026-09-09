# 52 — Async HTTP client/server with aiohttp

> `aiohttp` provides both an asyncio HTTP client and a full server
> framework in one package. Historically the go-to for high-concurrency
> scraping and simple async web services, before FastAPI/Starlette took
> over server-side use cases.

---

## install

```bash
pip install aiohttp
```

---

## async GET

```python
import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com/status") as resp:
            data = await resp.json()
            print(data)

asyncio.run(main())
```

Always create one `ClientSession` and reuse it for many requests — it
owns the connection pool, so creating a new session per request defeats
the point.

---

## many concurrent requests

```python
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

urls = [f"https://api.example.com/items/{i}" for i in range(50)]
results = asyncio.run(fetch_all(urls))
```

---

## POST JSON

```python
async def post_reading(session):
    async with session.post(
        "https://api.example.com/readings", json={"sensor": "line1", "value": 23.4}
    ) as resp:
        return await resp.json()
```

---

## a minimal server

```python
from aiohttp import web

async def handle(request):
    return web.json_response({"status": "ok"})

app = web.Application()
app.router.add_get("/status", handle)

web.run_app(app, port=8080)
```

---

## error handling basics

```python
import asyncio
import aiohttp

async def safe_fetch(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            resp.raise_for_status()
            return await resp.json()
    except asyncio.TimeoutError:
        print("request timed out")
    except aiohttp.ClientResponseError as e:
        print("bad status:", e.status)
    except aiohttp.ClientConnectionError:
        print("could not connect")
```

---

## snippets box

```python
# limit concurrency with a semaphore
sem = asyncio.Semaphore(10)

async def bounded_fetch(session, url):
    async with sem:
        async with session.get(url) as resp:
            return await resp.json()
```

---

## when to use what

| Need | Package |
|---|---|
| High-concurrency async client, optional server | `aiohttp` |
| Async client with a requests-like sync API too | `httpx` |
| New server projects | `fastapi` (built on Starlette) |

Next door: cap concurrency with a semaphore before hammering a
rate-limited third-party API.
