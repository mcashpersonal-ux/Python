# 39 — CAN bus with python-can

> `python-can` reads and writes CAN frames across many interfaces (USB
> adapters, PCAN, SocketCAN on Linux, virtual buses for testing) behind
> one consistent API. Common in automotive, robotics, and industrial
> motion control.

---

## install

```bash
pip install python-can
```

---

## connect and send a frame

```python
import can

bus = can.interface.Bus(channel="can0", interface="socketcan") # Linux SocketCAN

message = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03], is_extended_id=False)
bus.send(message)
```

`arbitration_id` is the CAN ID (priority + identity of the message);
`is_extended_id=False` selects the standard 11-bit ID format (`True` for
29-bit extended IDs).

---

## receive frames

```python
message = bus.recv(timeout=1.0) # blocks up to 1s, returns None on timeout
if message is not None:
    print(message)
```

Listening continuously:

```python
for message in bus:
    print(message.arbitration_id, message.data)
```

---

## filter which IDs you receive

```python
bus.set_filters([
    {"can_id": 0x123, "can_mask": 0x7FF, "extended": False},
])
```

Filtering in the driver/hardware is far cheaper than filtering every
frame in Python on a busy bus.

---

## error handling basics

```python
import can

try:
    bus = can.interface.Bus(channel="can0", interface="socketcan")
    bus.send(can.Message(arbitration_id=0x123, data=[0, 0, 0]))
except can.CanError as e:
    print("CAN error:", e)
finally:
    bus.shutdown()
```

`CanError` covers bus-off states, arbitration loss, and driver-level
failures — a busy or unterminated bus is the usual culprit.

---

## snippets box

```python
# virtual bus for tests, no hardware needed
bus = can.interface.Bus(channel="test", interface="virtual")
```

```python
# decode with a DBC file (signal definitions) via cantools
import cantools

db = cantools.database.load_file("vehicle.dbc")
decoded = db.decode_message(0x123, bytes([0x01, 0x02, 0x03]))
```

```python
# periodic send task instead of manual looping
task = bus.send_periodic(
    can.Message(arbitration_id=0x123, data=[0, 0, 0]), period=0.1
)
# task.stop() when done
```

---

## when to use what

| Need | Package |
|---|---|
| CAN bus, any adapter | `python-can` |
| Decode signal-level meaning from raw frames | `cantools` (pairs with `python-can`) |
| Serial (not CAN) devices | `pyserial` |

Next door: pair with `cantools` to turn raw frame bytes into named,
scaled signals.
