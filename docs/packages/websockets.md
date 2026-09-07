# 55 — WebSocket client/server with websockets

> `websockets` is a clean asyncio-native implementation of RFC 6455 —
> live dashboards, push notifications, streaming telemetry. Full-duplex
> and persistent, unlike request/response HTTP.

---

## install

```bash
pip install websockets
```

---

## connect as a client and send/receive

```python
import asyncio
from websockets.asyncio.client import connect

async def main():
    async with connect("ws://localhost:8765") as ws:
        await ws.send("hello")
        response = await ws.recv()
        print(response)

asyncio.run(main())
```

---

## receive a continuous stream

```python
async def listen():
    async with connect("ws://localhost:8765/telemetry") as ws:
        async for message in ws:
            print("received:", message)
```

`async for message in ws` reads messages until the connection closes —
the natural pattern for a live feed.

---

## a minimal server

```python
import asyncio
from websockets.asyncio.server import serve

async def handler(websocket):
    async for message in websocket:
        await websocket.send(f"echo: {message}")

async def main():
    async with serve(handler, "localhost", 8765):
        await asyncio.Future() # run forever

asyncio.run(main())
```

---

## broadcasting to multiple clients

```python
connected = set()

async def handler(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            for client in connected:
                await client.send(message)
    finally:
        connected.remove(websocket)
```

---

## error handling basics

```python
import websockets
from websockets.asyncio.client import connect

async def robust_listen():
    try:
        async with connect("ws://localhost:8765", open_timeout=5) as ws:
            async for message in ws:
                print(message)
    except websockets.exceptions.ConnectionClosed:
        print("connection closed by server")
    except OSError:
        print("could not connect")
```

---

## snippets box

```python
# reconnect loop for a long-running client
async def resilient_client():
    while True:
        try:
            async with connect("ws://localhost:8765") as ws:
                async for message in ws:
                    print(message)
        except Exception:
            await asyncio.sleep(3)
```

```python
async def secure_connect():
    # secure websocket (wss://)
    async with connect("wss://example.com/socket") as ws:
        ...
```

---

## when to use what

| Need | Package |
|---|---|
| Full-duplex, persistent connection | `websockets` |
| Request/response only | `httpx` / `requests` |
| WebSocket endpoint inside a bigger web app | `fastapi` (has built-in WS support) |

Next door: push data read from `pymodbus`/`asyncua` straight out over a
`websockets` server to a live dashboard.
