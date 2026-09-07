# 27 — Serial Modbus RTU with minimalmodbus

> `minimalmodbus` is a tiny, dependency-light client for Modbus RTU/ASCII
> over a serial port. No event loop, no server side — just a single
> instrument you poll synchronously. Great fit for one sensor or meter on
> RS-485.

---

## install

```bash
pip install minimalmodbus
```

---

## connect and read a register

```python
import minimalmodbus

instrument = minimalmodbus.Instrument("/dev/ttyUSB0", 1)  # port, slave address
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1  # seconds

value = instrument.read_register(100, number_of_decimals=1)
print(value)  # e.g. 23.4
```

`number_of_decimals` tells minimalmodbus to divide the raw integer by
`10**n` — many meters store `234` on the wire to mean `23.4`.

---

## write a register

```python
instrument.write_register(100, 25.0, number_of_decimals=1)
```

Reading/writing floats stored across two registers (IEEE-754) uses the
dedicated float helpers instead:

```python
temp = instrument.read_float(102, functioncode=3, number_of_registers=2)
instrument.write_float(102, 25.5, number_of_registers=2)
```

---

## error handling basics

Serial links fail more than TCP ones — always wrap reads and consider a
retry with backoff:

```python
import minimalmodbus
import time

instrument = minimalmodbus.Instrument("/dev/ttyUSB0", 1)
instrument.serial.timeout = 1

for attempt in range(3):
    try:
        print(instrument.read_register(100, number_of_decimals=1))
        break
    except (minimalmodbus.NoResponseError, minimalmodbus.InvalidResponseError) as e:
        print("retrying:", e)
        time.sleep(0.5)
```

Common exceptions: `NoResponseError` (device didn't answer — wiring/baud
rate/address), `InvalidResponseError` (bad CRC — noise on the bus).

---

## snippets box

```python
# RTU framing mode is default; switch to ASCII if the device needs it
instrument.mode = minimalmodbus.MODE_ASCII
```

```python
# read several registers at once
values = instrument.read_registers(0, 8)  # list[int]
```

```python
# read a coil (discrete on/off)
state = instrument.read_bit(10, functioncode=1)
```

---

## when to use what

| Need | Package |
|---|---|
| One instrument over RS-485, sync code | `minimalmodbus` |
| Many devices, TCP or RTU, async | `pymodbus` |
| Quick TCP-only reads | `pyModbusTCP` |

Next door: batch these readings into `pandas` and log them with `structlog`.
