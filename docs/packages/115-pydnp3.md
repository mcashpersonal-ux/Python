# 97 — DNP3 with pydnp3

> `pydnp3` exposes the open-source opendnp3 stack to Python. DNP3 is common in utility SCADA: a master polls an outstation for timestamped measurements and can issue carefully controlled commands to field equipment. This page starts with an offline point-model exercise, then shows the shape of a real master connection.

---

## Install

```bash
python -m pip install pydnp3
```

The package on PyPI is an old release (the latest listed release is `0.1.0`, published in 2018). Its published wheels target CPython 2.7, and the upstream project documents Linux and macOS support. On a current Python 3 installation, `pip` may therefore report that no compatible wheel exists. Building from source requires a C++14 compiler, CMake, and the repository's `dnp3` and `pybind11` submodules. Test the import in an isolated environment before planning a deployment; do not install an unverified binary into a production SCADA host.

---

## First example: an offline point model

This example does **not** import the native extension and does not open a socket. It is a safe way to rehearse how an electric, water, or wastewater gateway can normalize DNP3-style point data before sending it to a historian. It runs on any supported Python installation and uses a small, explicit data set.

```python
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass(frozen=True)
class AnalogPoint:
    index: int
    name: str
    value: float
    unit: str
    timestamp: datetime
    quality: str

raw_points = [
    {"index": 0, "name": "reservoir_level", "value": 4.82, "unit": "m", "quality": "ONLINE"},
    {"index": 1, "name": "pump_discharge", "value": 318.0, "unit": "kPa", "quality": "ONLINE"},
]

now = datetime.now(timezone.utc)
points = [AnalogPoint(timestamp=now, **point) for point in raw_points]
for point in points:
    print(f"{point.timestamp.isoformat()} {point.name}={point.value:g} {point.unit} [{point.quality}]")
```

Keep the point index, engineering unit, timestamp, and quality together. DNP3 measurements may arrive as binary, double-bit binary, counter, analog, or output-status points; the index is meaningful only within its point group and outstation configuration.

---

## What the binding provides

DNP3 separates a **master** (the SCADA side) from an **outstation** (RTU, PLC, protection relay, pump-station controller, or substation gateway). The master asks for scans or receives unsolicited responses; the outstation owns the points. `pydnp3` is a thin binding around opendnp3 classes, including `opendnp3`, `openpal`, and `asiodnp3` namespaces. The binding does not discover a device's point map for you: obtain the outstation's database and group/variation assignments from the controls engineer or device documentation.

A typical deployment has these layers:

| Layer | DNP3 responsibility | Utility example |
|---|---|---|
| Transport | TCP or serial link, timeout, reconnect policy | Cellular TCP link to a remote lift station |
| Master | Scans, class polling, time sync, command callbacks | Electric distribution SCADA server |
| Outstation | Measurement database and command execution | Feeder RTU or wastewater pump PLC |
| Application | Validation, alarm handling, historian/HA gateway | Store level and pump status in a historian |

---

## Inspect the installed binding

Because this project has changed little and is generated from C++ bindings, inspect the actual module installed in your environment rather than assuming that a newer opendnp3 API is present. This snippet is local and read-only; it does not connect to a device.

```python
import pydnp3
from pydnp3 import opendnp3

print("pydnp3 module:", pydnp3.__file__)
print("opendnp3 module:", opendnp3.__file__)
print("has GroupVariationID:", hasattr(opendnp3, "GroupVariationID"))
print("has TaskConfig:", hasattr(opendnp3, "TaskConfig"))
```

If the import fails with an extension or ABI error, stop there and resolve the interpreter/platform mismatch. Do not work around it by copying `.so` files between hosts.

---

## Master workflow (live device — lab only)

The following is a compact version of the upstream master pattern. It assumes a **reachable DNP3 outstation**, a known TCP endpoint, and helper callback classes that implement the opendnp3 interfaces. It is intentionally not an offline example: adapt it only in a test network or simulator, and confirm the endpoint, DNP3 link addresses, and point ranges with the device owner.

```python
import logging
import sys

from pydnp3 import asiodnp3, opendnp3, openpal

class ChannelListener(asiodnp3.IChannelListener):
    def __init__(self):
        super().__init__()

    def OnStateChange(self, state):
        print("channel state:", opendnp3.ChannelStateToString(state))

class MasterApplication(opendnp3.IMasterApplication):
    def __init__(self):
        super().__init__()

    def AssignClassDuringStartup(self):
        return False

    def OnClose(self):
        print("master channel closed")

    def OnOpen(self):
        print("master channel opened")

    def OnReceiveIIN(self, iin):
        print("received IIN:", iin)

    def OnTaskComplete(self, info):
        print("task complete:", info)

class SOEHandler(opendnp3.ISOEHandler):
    def __init__(self):
        super().__init__()

    def Start(self):
        pass

    def End(self):
        pass

    def Process(self, info, values):
        print("received:", info.gv, type(values).__name__)

log_handler = openpal.ConsoleLogger()
manager = asiodnp3.DNP3Manager(1, log_handler)
channel = manager.AddTCPClient(
    "utility-master",
    openpal.LogFilters(opendnp3.levels.NORMAL),
    "192.0.2.10",  # documentation address; replace only in a lab
    20000,
    ChannelListener(),
)
master = channel.AddMaster(
    "station-1",
    SOEHandler(),
    MasterApplication(),
    opendnp3.MasterParams(),
)
master.ScanRange(
    opendnp3.GroupVariationID(30, 1),
    0,
    7,
    opendnp3.TaskConfig().Default(),
)

input("Press Enter to shut down the lab connection... ")
manager.Shutdown()
```

The exact constructor signatures can vary across old wheels and source builds; use `help(asiodnp3.DNP3Manager)` and the upstream examples for the installed build. `192.0.2.10` is a documentation-only address and will not reach a real device. Replace it only after establishing an approved lab route. A scan of group 30, variation 1 is merely an example; a real outstation may use different groups, variations, and index ranges.

---

## Read, classify, and store measurements

A production `ISOEHandler.Process` should turn each received collection into application records and preserve DNP3 quality flags and event time. Do not treat a numeric value as valid merely because the callback ran: an outstation can report `COMM_LOST`, `REMOTE_FORCED`, `LOCAL_FORCED`, or other quality conditions. Record the raw group/variation and index alongside the normalized value so an operator can audit the mapping.

For polling strategy, use class scans deliberately. Class 1 events are commonly used for high-priority changes such as breaker trips, pump faults, or high-high tank levels; Class 2/3 can carry less urgent telemetry; a periodic Class 0 scan establishes a complete snapshot. Rate-limit scans and reconnects so a cellular or radio link is not overwhelmed.

---

## Commands and control points

DNP3 supports select-before-operate and direct operate commands. For a pump start, feeder switch, or valve command, prefer select-before-operate when the device and operating procedure require a two-step authorization. Verify the returned command status in the callback, enforce interlocks in the control system, and require an explicit operator action for hazardous equipment. A successful protocol response is not proof that a motor, breaker, or valve reached the desired physical state; read back the associated status point.

The upstream examples use objects such as `ControlRelayOutputBlock`, `ControlCode.LATCH_ON`, `AnalogOutputInt32`, `CommandSet`, and `master.SelectAndOperate(...)`. Treat those examples as API references, not as safe defaults for a live plant. Never copy a command index from a sample into an operating station without validating the point list and testing with outputs inhibited.

---

## Safety notes

- **Use a simulator or isolated test outstation first.** The page's first example is offline; the live master example is not. Never aim an exploratory scan or command at a production electric, water, or wastewater controller.
- **Commands can create physical consequences.** Keep command code disabled by default, use least privilege, validate ranges and quality, and require select-before-operate or a separate approval path where the operating procedure calls for it.
- **Protect the control network.** DNP3/TCP is not automatically encrypted or authenticated by this old binding. Use a segmented OT network, firewall allow-lists, VPN/TLS-capable gateways where approved, and monitoring consistent with the utility's security policy.
- **Bound failure behavior.** Configure finite timeouts, reconnect backoff, scan periods, and queue limits. On stale data or `COMM_LOST`, alarm and fail safe; do not silently substitute zero for an unavailable measurement.
- **Plan lifecycle support.** Pin the tested interpreter, compiler, package commit, and opendnp3 version. The PyPI package is old and may not support current Python versions or Windows; build and security-review it before deployment.

---

Next door: use [`asyncua`](033-asyncua.md) when the site already exposes an OPC UA gateway, or pair a tested DNP3 adapter with `pandas`/`influxdb-client` for auditable time-series telemetry.

References: [pydnp3 on PyPI](https://pypi.org/project/pydnp3/) · [ChargePoint/pydnp3 source and examples](https://github.com/ChargePoint/pydnp3) · [opendnp3 documentation](https://dnp3.github.io/)
