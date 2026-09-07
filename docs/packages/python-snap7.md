# 37 — Siemens S7 PLCs with python-snap7

> `python-snap7` talks the native S7 communication protocol directly to
> Siemens S7-300/400/1200/1500 PLCs — reading/writing data blocks (DBs),
> merkers, inputs and outputs — without needing a Modbus/OPC UA gateway
> in front of the PLC.

---

## install

```bash
pip install python-snap7
```

`python-snap7` wraps the `snap7` C library; the PyPI wheel bundles a
prebuilt binary for common platforms, so usually no separate install step
is needed.

---

## connect and read a data block

```python
import snap7

plc = snap7.client.Client()
plc.connect("192.168.1.50", 0, 1)  # ip, rack, slot

data = plc.db_read(db_number=1, start=0, size=4)  # raw bytes
print(data)
```

`rack`/`slot` identify the CPU on the rack — `0, 1` is the common default
for S7-1200/1500; check your hardware config if reads fail.

---

## decode and write typed values

Raw DB reads return bytes; use the `util` helpers to decode/encode:

```python
from snap7 import util

data = plc.db_read(db_number=1, start=0, size=4)
value = util.get_real(data, 0)      # 32-bit float at byte offset 0
print(value)

util.set_real(data, 0, 42.5)
plc.db_write(db_number=1, start=0, data=data)
```

Other helpers: `get_int`/`set_int` (16-bit), `get_dint`/`set_dint`
(32-bit), `get_bool`/`set_bool` (bit within a byte).

---

## read a single bit (e.g. a merker/flag)

```python
data = plc.mb_read(start=0, size=1)  # merker byte 0
flag = util.get_bool(data, 0, 0)     # byte 0, bit 0
```

---

## error handling basics

```python
import snap7

plc = snap7.client.Client()
try:
    plc.connect("192.168.1.50", 0, 1)
    if not plc.get_connected():
        raise ConnectionError("could not connect to PLC")
    data = plc.db_read(db_number=1, start=0, size=4)
except RuntimeError as e:
    print("snap7 error:", e)
finally:
    plc.disconnect()
```

`RuntimeError` from snap7 usually wraps a native error code — the message
text names the failure (e.g. address out of range, CPU not reachable).

---

## snippets box

```python
# check CPU state before touching data
state = plc.get_cpu_state()
print(state)  # e.g. 'S7CpuStatusRun'
```

```python
# read multiple areas in one round trip
items = [
    snap7.types.S7DataItem(Area=snap7.types.Areas.DB, DBNumber=1, WordLen=snap7.types.WordLen.Byte, Start=0, Amount=4),
]
plc.read_multi_vars(items)
```

---

## when to use what

| Need | Package |
|---|---|
| Native S7 protocol, Siemens CPUs | `python-snap7` |
| PLC also exposes Modbus/OPC UA | `pymodbus` / `asyncua` |
| Beckhoff TwinCAT instead of Siemens | `pyads` |

Next door: decode a full DB layout once with `util.get_*` calls into a
`pydantic` model for typed access.
