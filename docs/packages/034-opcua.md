# 32 — Legacy synchronous OPC UA with opcua

> `opcua` (sometimes called `python-opcua`) is the older, synchronous
> predecessor to `asyncua`. Same protocol, blocking API. Mostly relevant
> for maintaining existing code — new projects should reach for `asyncua`.

---

## install

```bash
pip install opcua
```

---

## connect and read a node

```python
from opcua import Client

client = Client("opc.tcp://192.168.1.50:4840/freeopcua/server/")
client.connect()
try:
    node = client.get_node("ns=2;i=2")
    print(node.get_value())
finally:
    client.disconnect()
```

Everything is blocking here — no `async`/`await`, so it fits naturally
into simple scripts or threads instead of an event loop.

---

## write a value

```python
from opcua import ua

node = client.get_node("ns=2;i=2")
node.set_value(ua.Variant(42, ua.VariantType.Int32))
```

---

## subscribe to changes

```python
class Handler:
    def datachange_notification(self, node, val, data):
        print(f"{node}: {val}")

sub = client.create_subscription(500, Handler())
handle = sub.subscribe_data_change(node)
# ... later:
sub.unsubscribe(handle)
sub.delete()
```

---

## error handling basics

```python
from opcua.ua.uaerrors import UaError

try:
    client.connect()
    node.get_value()
except UaError as e:
    print("OPC UA error:", e)
finally:
    client.disconnect()
```

---

## snippets box

```python
# browse the tree
root = client.get_root_node()
for child in root.get_children():
    print(child.get_browse_name())
```

```python
# username/password auth
client = Client("opc.tcp://192.168.1.50:4840/")
client.set_user("admin")
client.set_password("secret")
client.connect()
```

---

## when to use what

| Need | Package |
|---|---|
| New project, async, active maintenance | `asyncua` |
| Existing codebase already on `opcua` | `opcua` |
| No OPC UA server available | `pymodbus` / `python-snap7` |

Next door: if you're starting fresh, port this to `asyncua` — the node/
subscription API maps over almost 1:1.
