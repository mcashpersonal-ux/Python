# 29 — Minimal Modbus TCP with pyModbusTCP

> `pyModbusTCP` is a small, dependency-free Modbus TCP client. No RTU
> support, no server framework baggage — just fast one-shot reads/writes
> against a TCP Modbus device. Good pick for scripts and lightweight
> polling daemons.

---

## install

```bash
pip install pyModbusTCP
```

---

## connect and read holding registers

```python
from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192.168.1.50", port=502, unit_id=1, auto_open=True)

regs = client.read_holding_registers(0, 4)
print(regs) # list[int] or None on failure
```

`auto_open=True` reconnects automatically before each request — handy for
long-running pollers on flaky links.

---

## write a register

```python
ok = client.write_single_register(100, 1234)
print(ok) # True/False
```

```python
ok = client.write_multiple_registers(100, [1, 2, 3, 4])
```

---

## error handling basics

`pyModbusTCP` returns `None` (or `False` for writes) instead of raising,
so always check the return value:

```python
regs = client.read_holding_registers(0, 4)
if regs is None:
    print("read failed:", client.last_error_as_txt)
else:
    print(regs)
```

`client.last_error_as_txt` and `client.last_except_as_txt` give a
human-readable reason (timeout, connection refused, illegal address, ..).

---

## snippets box

```python
# read coils / discrete inputs
coils = client.read_coils(0, 8)
inputs = client.read_discrete_inputs(0, 8)
```

```python
# explicit connect/close instead of auto_open
client = ModbusClient(host="192.168.1.50", port=502, unit_id=1)
if client.open():
    print(client.read_holding_registers(0, 4))
    client.close()
```

```python
# polling loop with a timeout guard
import time

client = ModbusClient(host="192.168.1.50", port=502, unit_id=1, timeout=2, auto_open=True)
for _ in range(60):
    regs = client.read_holding_registers(0, 8)
    print(regs or f"error: {client.last_error_as_txt}")
    time.sleep(1)
```

---

## when to use what

| Need | Package |
|---|---|
| Simplest possible TCP client, no RTU | `pyModbusTCP` |
| TCP + RTU, server side, async | `pymodbus` |
| Serial-only single instrument | `minimalmodbus` |

Next door: push the polled values straight into `influxdb-client` for
time-series storage.
