# 31 — OPC UA with asyncua

> `asyncua` is the modern, actively maintained OPC UA stack for Python —
> async client and server, subscriptions, and security policies. OPC UA
> exposes a structured, self-describing node tree instead of raw
> registers, so browsing matters as much as reading.

---

## install

```bash
pip install asyncua
```

---

## connect and read a node

```python
import asyncio
from asyncua import Client

async def main():
    async with Client(url="opc.tcp://192.168.1.50:4840/freeopcua/server/") as client:
        node = client.get_node("ns=2;i=2")
        value = await node.read_value()
        print(value)

asyncio.run(main())
```

Node IDs (`ns=<namespace>;i=<identifier>`) come from browsing the server —
most OPC UA servers/PLCs ship a way to export their node tree, or you can
browse it live (see snippets box).

---

## write a value

```python
from asyncua import ua

async def write_value():
    async with Client(url="opc.tcp://192.168.1.50:4840/freeopcua/server/") as client:
        node = client.get_node("ns=2;i=2")
        await node.write_value(ua.Variant(42, ua.VariantType.Int32))
```

Explicit `Variant` types matter — OPC UA is strongly typed, unlike
Modbus's untyped 16-bit registers.

---

## subscribe to changes

```python
from asyncua import Client, Node
from asyncua.common.subscription import SubHandler

class Handler(SubHandler):
    def datachange_notification(self, node: Node, val, data):
        print(f"{node}: {val}")

async def subscribe():
    async with Client(url="opc.tcp://192.168.1.50:4840/freeopcua/server/") as client:
        node = client.get_node("ns=2;i=2")
        handler = Handler()
        sub = await client.create_subscription(500, handler) # ms interval
        await sub.subscribe_data_change(node)
        await asyncio.sleep(60)
```

---

## error handling basics

```python
from asyncua.ua.uaerrors import BadNodeIdUnknown, UaStatusCodeError

async def read_safely(node):
    try:
        return await node.read_value()
    except BadNodeIdUnknown:
        print("node id doesn't exist on this server")
    except UaStatusCodeError as e:
        print("OPC UA error:", e)
```

---

## snippets box

```python
async def browse(client):
    # browse children of the root node to discover the tree
    root = client.get_node("i=84")
    children = await root.get_children()
    for child in children:
        print(await child.read_browse_name())
```

```python
# connect with username/password
client = Client(url="opc.tcp://192.168.1.50:4840/")
client.set_user("admin")
client.set_password("secret")
```

---

## when to use what

| Need | Package |
|---|---|
| Modern async OPC UA client/server | `asyncua` |
| Existing sync codebase, legacy stack | `opcua` |
| Register-based PLC (no OPC UA server) | `pymodbus` / `python-snap7` |

Next door: fan subscription callbacks out to `paho-mqtt` for a UA-to-MQTT
bridge.
