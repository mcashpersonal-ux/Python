# 30 — Lightweight Modbus with uModbus

> `umodbus` is a small, pure-Python Modbus client/server supporting both
> TCP and RTU, aimed at embedded/edge use where a heavy dependency tree
> isn't welcome. API is function-based rather than class-based.

---

## install

```bash
pip install uModbus
```

---

## connect and read holding registers (TCP)

```python
import socket
from umodbus.client import tcp

sock = socket.create_connection(("192.168.1.50", 502), timeout=5)

message = tcp.read_holding_registers(slave_id=1, starting_address=0, quantity=4)
response = tcp.send_message(message, sock)
print(response)  # list[int]
```

`umodbus` builds a raw PDU with `tcp.read_holding_registers(...)` and you
send it yourself over a socket you own — more explicit, less magic.

---

## write a register

```python
message = tcp.write_single_register(slave_id=1, address=100, value=1234)
tcp.send_message(message, sock)
```

```python
message = tcp.write_multiple_registers(slave_id=1, starting_address=100, values=[1, 2, 3, 4])
tcp.send_message(message, sock)
```

---

## RTU (serial) client

```python
import serial
from umodbus.client import rtu

serial_port = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)

message = rtu.read_holding_registers(slave_id=1, starting_address=0, quantity=4)
response = rtu.send_message(message, serial_port)
print(response)
```

---

## error handling basics

```python
from umodbus.exceptions import ModbusError

try:
    response = tcp.send_message(message, sock)
except ModbusError as e:
    print("modbus exception response:", e)
except (socket.timeout, ConnectionError) as e:
    print("transport error:", e)
```

---

## snippets box

```python
# read coils
message = tcp.read_coils(slave_id=1, starting_address=0, quantity=8)
coils = tcp.send_message(message, sock)
```

```python
# always close what you open
try:
    ...
finally:
    sock.close()
```

---

## when to use what

| Need | Package |
|---|---|
| Minimal footprint, own the socket | `umodbus` |
| Batteries-included client/server | `pymodbus` |
| Zero-dep TCP-only quick reads | `pyModbusTCP` |

Next door: wrap the socket handling in a small class and expose it behind
`fastapi` for a REST-to-Modbus bridge.
