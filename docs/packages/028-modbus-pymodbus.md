# 26 - Modbus TCP with pymodbus

> pymodbus is the standard all-round Modbus library. Speak Modbus
> TCP (default port 502) or RTU over serial to PLCs, VFDs, meters,
> and SCADA gateways. This page uses a local TCP slave, so every snippet
> is copy-paste runnable.

---

## install

```bash
pip install pymodbus
```

---

## connect and read holding registers

PLCs expose registers as 16-bit words. Holding registers (read/write) hold
the values you usually want. Input registers (read-only) come from sensors.

```python
from pymodbus.client import ModbusTcpClient

with ModbusTcpClient("localhost", port=5020) as client:
    rr = client.read_holding_registers(address=100, count=4, device_id=1)
    if rr.isError():
        raise RuntimeError(rr)
    print(rr.registers) # e.g. [10, ..................
```

`device_id` is the Modbus unit/slave ID, default is 1. `address` is zero-
based: most devices document register addresses as 1-based, so subtract 1
when in doubt.

---

## write a register

```python
wr = client.write_register(address=100, value=12345, device_id=1)
if wr.isError():
    raise RuntimeError(wr)
print(wr) # WriteRegisterResponse
```

Writing coils (on/off) works the same way with bool values:

```python
wc = client.write_coil(address=10, value=True, device_id=1)
wc.isError() # False
```

---

## error handling basics

Modbus can fail silently on the wire, always check `.isError()`. Set a read
timeout so a dead device does not hang you:

```python
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("192.168.1.50", port=502, timeout=5)
if not client.connect():
    raise ConnectionError("PLC not reachable")
try:
    rr = client.read_holding_registers(address=100, count=4, device_id=1)
    if rr.isError():
        print("Modbus error:", rr) # e.g. IllegalAddress
    else:
        print(rr.registers)
finally:
    client.close()
```

Common error values: `IllegalAddress` (register number out of range),
`IllegalValue` (`count` too big), `GatewayTargetDeviceFailed` (device ID
wrong or unreachable).

---

## snippets box

```python
# single register with scaling
reading = client.read_holding_registers(address=10, count=1, device_id=1)
scale = 0.1 # temperature stored as 10x real
temp_c = reading.registers[0] * scale
print(f"{temp_c:.1f} C")
```

```python
# several tags in one call
block = client.read_holding_registers(address=0, count=32, device_id=1)
tags = block.registers if block else []
```

```python
# poll loop
import time

def poll():
    rr = client.read_holding_registers(address=0, count=8, device_id=1)
    if not rr.isError():
        print(rr.registers)
    time.sleep(1)

for _ in range(60):
    poll()
```

---

## when to use what

| Need | Package |
|---|---|---|
| Modbus TCP client/server | `pymodbus` |
| Single sensor over RS-485 | `minimalmodbus` |
| Quick one-shot reads | `pyModbusTCP` |
| SCADA gateway bridge | `pymodbus` + `influxdb-client` |

Next door: make the tags time-series with `pandas` then feed them into InfluxDB,
and explore OPC UA.
