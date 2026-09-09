# 36 — Asyncio-native MQTT with aiomqtt

> `aiomqtt` wraps the Paho C client in an asyncio-friendly API: connect
> once, `async for` incoming messages. No callbacks, no manual loop
> management — fits naturally into an existing asyncio application.

---

## install

```bash
pip install aiomqtt
```

---

## connect and receive messages

```python
import asyncio
import aiomqtt

async def main():
    async with aiomqtt.Client("broker.local") as client:
        await client.subscribe("plant/+/temperature")
        async for message in client.messages:
            print(message.topic, message.payload.decode())

asyncio.run(main())
```

The `async with` block owns the connection lifecycle — it connects on
entry and disconnects cleanly on exit, including on exceptions.

---

## publish a message

```python
async def publish():
    async with aiomqtt.Client("broker.local") as client:
        await client.publish("plant/line1/temperature", payload="23.4", qos=1)
```

---

## reconnect handling

`aiomqtt` doesn't auto-reconnect — wrap the connection in a retry loop for
long-running services:

```python
import aiomqtt

async def run():
    while True:
        try:
            async with aiomqtt.Client("broker.local") as client:
                await client.subscribe("plant/#")
                async for message in client.messages:
                    print(message.topic, message.payload)
        except aiomqtt.MqttError as e:
            print(f"connection lost: {e}; reconnecting in 5s")
            await asyncio.sleep(5)
```

---

## publish and subscribe concurrently

```python
import asyncio
import aiomqtt

async def publisher(client):
    while True:
        await client.publish("plant/line1/status", "alive")
        await asyncio.sleep(10)

async def subscriber(client):
    await client.subscribe("plant/+/status")
    async for message in client.messages:
        print(message.topic, message.payload.decode())

async def main():
    async with aiomqtt.Client("broker.local") as client:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(publisher(client))
            tg.create_task(subscriber(client))

asyncio.run(main())
```

---

## error handling basics

```python
async def connect_once():
    try:
        async with aiomqtt.Client("broker.local", timeout=10) as client:
            ...
    except aiomqtt.MqttError as e:
        print("mqtt error:", e)
```

---

## snippets box

```python
# TLS + auth
client = aiomqtt.Client(
    "broker.local", port=8883, username="user", password="pass", tls_context=ssl.create_default_context()
)
```

---

## when to use what

| Need | Package |
|---|---|
| Existing asyncio codebase | `aiomqtt` |
| Sync code, or need callback-style hooks | `paho-mqtt` |

Next door: pair with `asyncua`'s subscription callbacks for an OPC UA to
MQTT bridge running entirely on one event loop.
