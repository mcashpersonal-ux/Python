# 49 — HTTP client with requests

> `requests` is the de-facto standard HTTP client for Python — simple,
> readable API for REST calls, file uploads, and auth. Synchronous only;
> reach for `httpx` or `aiohttp` when you need async.

---

## install

```bash
pip install requests
```

---

## GET a JSON API

```python
import requests

resp = requests.get("https://api.example.com/status", timeout=5)
resp.raise_for_status()
data = resp.json()
print(data)
```

`raise_for_status()` turns 4xx/5xx responses into an exception instead of
silently returning bad data — always call it (or check `.ok`) before
using the response.

---

## POST with JSON body and headers

```python
resp = requests.post(
    "https://api.example.com/readings",
    json={"sensor": "line1", "value": 23.4},
    headers={"Authorization": "Bearer TOKEN"},
    timeout=5,
)
resp.raise_for_status()
```

`json=` serializes the dict and sets `Content-Type: application/json`
automatically — no manual `json.dumps` needed.

---

## sessions for repeated calls

```python
session = requests.Session()
session.headers.update({"Authorization": "Bearer TOKEN"})

for i in range(5):
    resp = session.get(f"https://api.example.com/items/{i}", timeout=5)
    print(resp.json())
```

A `Session` reuses the underlying TCP connection (connection pooling) —
noticeably faster than calling `requests.get` repeatedly.

---

## error handling basics

```python
import requests

try:
    resp = requests.get("https://api.example.com/status", timeout=5)
    resp.raise_for_status()
except requests.Timeout:
    print("request timed out")
except requests.ConnectionError:
    print("could not reach host")
except requests.HTTPError as e:
    print("bad status code:", e.response.status_code)
```

Always pass `timeout=` — without it, `requests` will hang indefinitely on
a dead connection.

---

## snippets box

```python
# file upload
with open("report.csv", "rb") as f:
    requests.post("https://api.example.com/upload", files={"file": f})
```

```python
# retries with backoff
from requests.adapters import HTTPAdapter, Retry

session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=Retry(total=3, backoff_factor=0.5)))
```

---

## when to use what

| Need | Package |
|---|---|
| Simple sync HTTP calls | `requests` |
| Async, or need HTTP/2 | `httpx` |
| Scraping at scale, many concurrent requests | `aiohttp` |

Next door: parse the HTML/JSON you fetch with `beautifulsoup4` or
`pydantic`.
