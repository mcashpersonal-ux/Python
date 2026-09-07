# 38 — Beckhoff TwinCAT with pyads

> `pyads` speaks Beckhoff's ADS (Automation Device Specification) protocol
> — the native way to read/write PLC variables by symbolic name on
> TwinCAT 2/3 systems, instead of raw addresses.

---

## install

```bash
pip install pyads
```

---

## connect and read a symbolic variable

```python
import pyads

plc = pyads.Connection("5.24.37.144.1.1", pyads.PORT_TC3PLC1, "192.168.1.50")
plc.open()

value = plc.read_by_name("MAIN.temperature", pyads.PLCTYPE_REAL)
print(value)

plc.close()
```

The first argument is the AMS Net ID (identifies the target device on the
ADS network), not an IP address — find it in TwinCAT's target settings.
The third argument is the actual IP to connect over.

---

## write a symbolic variable

```python
with pyads.Connection("5.24.37.144.1.1", pyads.PORT_TC3PLC1, "192.168.1.50") as plc:
    plc.write_by_name("MAIN.setpoint", 42.5, pyads.PLCTYPE_REAL)
```

Using `with` is preferred — it guarantees `open()`/`close()` even on
exceptions.

---

## read a struct

```python
import pyads
from ctypes import Structure, c_float, c_bool

class Recipe(Structure):
    _fields_ = [("temperature", c_float), ("active", c_bool)]

with pyads.Connection(net_id, port, ip) as plc:
    recipe = plc.read_structure_by_name("MAIN.recipe", Recipe)
    print(recipe.temperature, recipe.active)
```

---

## subscribe to variable changes (notifications)

```python
def callback(handle, name, timestamp, value):
    print(name, value)

with pyads.Connection(net_id, port, ip) as plc:
    attr = pyads.NotificationAttrib(4) # size in bytes, PLCTYPE_INT here
    plc.add_device_notification("MAIN.counter", attr, callback)
    import time; time.sleep(60)
```

---

## error handling basics

```python
import pyads

try:
    with pyads.Connection(net_id, port, ip) as plc:
        value = plc.read_by_name("MAIN.temperature", pyads.PLCTYPE_REAL)
except pyads.ADSError as e:
    print("ADS error:", e.err_code, e.msg)
```

Common `err_code`s: `1808` (symbol not found — check the variable name and
that it's not optimized away), `1861` (target port not found — check
`PORT_TC3PLC1` matches your runtime).

---

## snippets box

```python
# read multiple variables efficiently in one round trip
with pyads.Connection(net_id, port, ip) as plc:
    handles = plc.multi_read(
        [("MAIN.temperature", pyads.PLCTYPE_REAL), ("MAIN.pressure", pyads.PLCTYPE_REAL)]
    )
```

---

## when to use what

| Need | Package |
|---|---|
| Beckhoff TwinCAT PLC | `pyads` |
| Siemens S7 PLC | `python-snap7` |
| PLC exposes Modbus/OPC UA instead | `pymodbus` / `asyncua` |

Next door: push notification callbacks into `paho-mqtt` for a plant-wide
event bus.
