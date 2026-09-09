# 51 — Low-level HTTP with urllib3

> `urllib3` is the connection-pooling HTTP engine that `requests` and
> `httpx` build on. Reach for it directly when you want fine-grained
> control (custom pooling, retries, SSL contexts) without a higher-level
> wrapper's opinions.

---

## install

```bash
pip install urllib3
```

---

## a pooled GET request

```python
import urllib3

http = urllib3.PoolManager()
resp = http.request("GET", "https://api.example.com/status", timeout=5.0)
print(resp.status)
print(resp.json()) # urllib3 2.x has a convenience .json() helper
```

`PoolManager` maintains a pool of connections per host — create one and
reuse it across requests instead of a new one each time.

---

## POST with a JSON body

```python
import json

resp = http.request(
    "POST",
    "https://api.example.com/readings",
    body=json.dumps({"sensor": "line1", "value": 23.4}).encode(),
    headers={"Content-Type": "application/json"},
)
print(resp.status)
```

Unlike `requests`, there's no automatic JSON encoding — you serialize and
set headers yourself.

---

## retries and timeouts

```python
from urllib3.util import Retry, Timeout

retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
timeout = Timeout(connect=2.0, read=5.0)

http = urllib3.PoolManager(retries=retries, timeout=timeout)
```

---

## error handling basics

```python
import urllib3

try:
    resp = http.request("GET", "https://api.example.com/status", timeout=5.0)
    if resp.status >= 400:
        print("bad status:", resp.status)
except urllib3.exceptions.MaxRetryError as e:
    print("all retries failed:", e)
except urllib3.exceptions.TimeoutError:
    print("request timed out")
```

---

## snippets box

```python
# streaming a large response instead of loading it all into memory
resp = http.request("GET", "https://example.com/large-file.csv", preload_content=False)
for chunk in resp.stream(1024):
    process(chunk)
resp.release_conn()
```

```python
# custom SSL context for private CAs
import ssl
ctx = ssl.create_default_context(cafile="internal-ca.pem")
http = urllib3.PoolManager(ssl_context=ctx)
```

---

## when to use what

| Need | Package |
|---|---|
| Fine-grained pooling/retry control | `urllib3` |
| Everyday scripts, readable API | `requests` |
| Async | `httpx` / `aiohttp` |

Next door: most projects should use `requests` on top of this rather than
`urllib3` directly — drop down here only when you need the extra control.
