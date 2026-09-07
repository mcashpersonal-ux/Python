# 28 — Modbus toolkit with modbus-tk

> `modbus-tk` is an older but still-used generic Modbus toolkit covering
> TCP, RTU and ASCII with lower-level framing control than `pymodbus`.
> Useful when you need a custom master/slave setup or non-standard framing.

---

## install

```bash
pip install modbus-tk
```

---

## connect and read holding registers (TCP)

```python
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import socket

master = modbus_tcp.TcpMaster(host="192.168.1.50", port=502)
master.set_timeout(5.0)

values = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4)
print(values) # tuple of ints
```

The `execute` signature is `(slave_id, function_code, starting_address,
quantity)`. Function codes live in `modbus_tk.defines` (`cst`).

---

## write a register

```python
master.execute(1, cst.WRITE_SINGLE_REGISTER, 100, output_value=1234)
```

Writing multiple registers at once:

```python
master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=[1, 2, 3, 4])
```

---

## RTU (serial) master

```python
import serial
import modbus_tk.modbus_rtu as modbus_rtu

master = modbus_rtu.RtuMaster(
    serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity="N", stopbits=1)
)
master.set_timeout(2.0)
values = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4)
```

---

## error handling basics

```python
import modbus_tk.exceptions as mte

try:
    values = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4)
except mte.ModbusInvalidResponseError as e:
    print("bad response:", e)
except socket.timeout:
    print("device did not respond in time")
```

---

## snippets box

```python
# read coils
coils = master.execute(1, cst.READ_COILS, 0, 8)
```

```python
# spin up a minimal TCP slave for local testing
import modbus_tk.modbus_tcp as modbus_tcp

server = modbus_tcp.TcpServer(port=5020)
server.start()
slave = server.add_slave(1)
slave.add_block("holding", cst.HOLDING_REGISTERS, 0, 100)
```

---

## when to use what

| Need | Package |
|---|---|
| Fine-grained framing control, legacy codebases | `modbus-tk` |
| Modern, actively maintained, async-capable | `pymodbus` |
| One serial instrument, minimal API | `minimalmodbus` |

Next door: wrap the polling loop with `schedule` for periodic reads.
