# 40 — Serial ports with pyserial

> `pyserial` is the standard cross-platform RS-232/RS-485 serial I/O
> library. It underlies `minimalmodbus` and `modbus-tk`'s RTU transports,
> and is the right tool whenever a device speaks its own line protocol
> instead of Modbus.

---

## install

```bash
pip install pyserial
```

---

## open a port and read/write bytes

```python
import serial

ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)

ser.write(b"MEASURE?\r\n")
response = ser.readline()  # reads until \n or timeout
print(response)

ser.close()
```

On Windows, ports look like `"COM3"`; on Linux/macOS, `/dev/ttyUSB0`,
`/dev/ttyACM0`, or `/dev/cu.usbserial-*`.

---

## use a context manager

```python
with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as ser:
    ser.write(b"STATUS\r\n")
    print(ser.readline())
```

---

## configure framing (parity, stop bits, flow control)

```python
ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    rtscts=False,
    timeout=2,
)
```

Mismatched parity/stop bits is the most common reason a serial device
returns garbage instead of failing outright — check the datasheet.

---

## list available ports

```python
from serial.tools import list_ports

for port in list_ports.comports():
    print(port.device, port.description)
```

Useful for auto-detecting which port a USB-serial adapter landed on,
since it can change between plug-ins.

---

## error handling basics

```python
import serial

try:
    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
except serial.SerialException as e:
    print("could not open port:", e)
else:
    try:
        ser.write(b"PING\r\n")
        line = ser.readline()
        if not line:
            print("timed out waiting for a response")
    finally:
        ser.close()
```

---

## snippets box

```python
# read until a specific terminator instead of newline
ser.read_until(b"\r\n")
```

```python
# non-blocking check for available bytes
if ser.in_waiting:
    data = ser.read(ser.in_waiting)
```

```python
# reconfigure baud rate on an already-open port
ser.baudrate = 115200
```

---

## when to use what

| Need | Package |
|---|---|
| Raw serial I/O, custom/proprietary protocol | `pyserial` |
| Modbus RTU on top of serial | `minimalmodbus` / `pymodbus` |
| CAN bus (not point-to-point serial) | `python-can` |

Next door: wrap a device's line protocol in a small class exposing typed
methods, the same shape as `minimalmodbus`'s `read_register`.
