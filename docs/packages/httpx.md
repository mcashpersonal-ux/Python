# 50 — Async + sync HTTP with httpx

> `httpx` is a modern HTTP client with a `requests`-like API that also
> supports async/await and HTTP/2. Good drop-in upgrade path when you
> need async without rewriting your whole calling style.

---

## install

```bash
pip install httpx
```

---

## sync GET (requests-compatible API)

```python
import httpx

resp = httpx.get("https://api.example.com/status", timeout=5)
resp.raise_for_status()
print(resp.json())
```

---

## async GET

```python
import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/status", timeout=5)
        resp.raise_for_status()
        print(resp.json())

asyncio.run(main())
```

---

## concurrent requests

```python
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url, timeout=5) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

urls = [f"https://api.example.com/items/{i}" for i in range(10)]
results = asyncio.run(fetch_all(urls))
```

This is the main reason to reach for `httpx` over `requests` — fetching
many endpoints concurrently instead of one at a time.

---

## POST with JSON and a persistent client

```python
async def post_reading():
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        resp = await client.post("/readings", json={"sensor": "line1", "value": 23.4})
        resp.raise_for_status()
```

---

## error handling basics

```python
import httpx

async def safe_get(client, url):
    try:
        resp = await client.get(url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except httpx.TimeoutException:
        print("request timed out")
    except httpx.ConnectError:
        print("could not reach host")
    except httpx.HTTPStatusError as e:
        print("bad status:", e.response.status_code)
```

---

## snippets box

```python
# enable HTTP/2 (requires the h2 extra: pip install httpx[http2])
client = httpx.AsyncClient(http2=True)
```

```python
# retries via a transport
transport = httpx.HTTPTransport(retries=3)
client = httpx.Client(transport=transport)
```

---

## when to use what

| Need | Package |
|---|---|
| Async support, requests-like API | `httpx` |
| Simple sync-only scripts | `requests` |
| Maximum raw async throughput | `aiohttp` |

Next door: pair concurrent fetches with `asyncio.Semaphore` to cap
in-flight requests against rate-limited APIs.
