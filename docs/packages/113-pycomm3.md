# 95 — EtherNet/IP with pycomm3

> `pycomm3` is a Python 3 library for Allen-Bradley/Rockwell EtherNet/IP communication. Its `LogixDriver` reads and writes symbolic tags on ControlLogix and CompactLogix controllers, including arrays, strings, user-defined types (UDTs), and program-scoped tags.

## Install

```bash
python -m pip install pycomm3
```

`pycomm3` is pure Python and uses the host's normal network sockets; it does not require Studio 5000 or a vendor GUI. The upstream project documents Python 3.6.1 through 3.10 and primarily tests on Windows, although it is intended to be OS-independent. Check the current [PyPI metadata](https://pypi.org/project/pycomm3/) before selecting a newer Python interpreter for production.

## First example: an offline response object

Start by learning the result object without opening an EtherNet/IP connection. This example constructs a successful `Tag` response locally and checks its truth value, so it is safe to run on a laptop or in CI. It needs no PLC, network, or GUI.

```python
from pycomm3 import Tag

result = Tag("DemoCounter", 42, "DINT", None)

if result:
    print(f"{result.tag}: {result.value} ({result.type})")
else:
    print(f"Read failed: {result.error}")
```

A `Tag` is truthy when it has a value and no error. Real reads and writes return the same shape, which makes explicit result checking useful before a value enters an HMI, historian, or control calculation.

## Connect to a ControlLogix or CompactLogix controller

The following is a **live-device example**. It assumes an approved controller is reachable at `192.168.1.50` and that the CPU is in slot `0`. For a controller in another chassis slot, use `192.168.1.50/2`, for example. The tag name must match the Logix project exactly, including case.

```python
from pycomm3 import LogixDriver

controller_path = "192.168.1.50/0"

try:
    with LogixDriver(controller_path) as plc:
        result = plc.read("ProductionCounter")
        if result:
            print(f"{result.tag} = {result.value} ({result.type})")
        else:
            print(f"PLC returned an error for {result.tag}: {result.error}")
except Exception as exc:
    print(f"Could not open the Logix connection: {exc}")
```

`LogixDriver` gathers controller information and uploads tag and data-type definitions when it opens by default. Large projects can therefore take several seconds to initialize. A context manager closes the session even when the read fails; long-lived applications that do not use `with` must call `open()` and `close()` themselves.

## Read several tags and arrays

`read()` accepts multiple tag names and returns a list of `Tag` results. Logix array syntax uses square brackets for the starting index and braces for the number of elements. This live-device example reads two scalar tags and three elements from a `DINT` array.

```python
from pycomm3 import LogixDriver

with LogixDriver("192.168.1.50/0") as plc:
    results = plc.read("LineRunning", "BatchNumber", "RecipeSteps[0]{3}")

for result in results:
    if result:
        print(f"{result.tag}: {result.value}")
    else:
        print(f"{result.tag}: {result.error}")
```

Program-scoped tags use `Program:ProgramName.TagName`. For a two-dimensional array, use the Logix form such as `Matrix[1,0]{4}`; the element count is the total number of values requested across dimensions. BOOL arrays have special packing rules when writing, so test those with a non-production controller first.

## Write a setpoint deliberately

Writes change controller state and may cause equipment to move. The example below is **live-device code** and should only run after the tag, engineering range, and operational approval have been verified. `write()` accepts a tag/value pair and returns a `Tag` result that should be checked.

```python
from pycomm3 import LogixDriver

requested_speed = 35.0
minimum_speed = 0.0
maximum_speed = 60.0

if not minimum_speed <= requested_speed <= maximum_speed:
    raise ValueError("requested speed is outside the approved range")

with LogixDriver("192.168.1.50/0") as plc:
    result = plc.write("LineSpeedSetpoint", requested_speed)
    if not result:
        raise RuntimeError(f"PLC rejected the write: {result.error}")
    print(f"Wrote {result.tag} = {result.value}")
```

For multiple writes, pass separate tuples, such as `plc.write(("EnableRequest", True), ("LineSpeedSetpoint", 35.0))`. Prefer small, explicit writes over replacing a complete structure. For UDTs and AOIs, reads return dictionaries and writes require a complete compatible dictionary when the structure is writable.

## Controller paths and connection behavior

A path with only an IP address is the shortcut for a device in slot 0 in the Logix driver. Use `address/slot` for a CPU in a chassis, or a full CIP route for a bridged topology, for example `10.20.30.100/backplane/2/enet/6.7.8.9/backplane/0`. Confirm the route with the controls engineer; a syntactically valid route can still reach the wrong controller.

`pycomm3` also exposes `CIPDriver` for generic Common Industrial Protocol devices and `SLCDriver` for legacy SLC-500/MicroLogix data files. This page focuses on `LogixDriver`, whose services target ControlLogix, CompactLogix, and Micro800-style tag access. It is not a replacement for a safety-rated controller, an OPC UA server, or Studio 5000 commissioning tools.

## Safety notes

- **Begin offline, then use a simulator or isolated lab controller.** Never paste a production address into an unreviewed example.
- Treat every `write()` as an operational command. Apply application-level authorization, allow-lists, engineering-unit limits, rate limits, and audit logging before exposing it to operators or a web service.
- Read and verify the current mode, interlocks, permissives, and feedback signals before commanding equipment. A successful EtherNet/IP response confirms protocol acceptance, not physical motion or safe completion.
- Use least-privilege network placement and firewall rules. EtherNet/IP commonly uses TCP/UDP 44818 and UDP 2222 for implicit I/O; do not expose these ports directly to an untrusted network.
- Keep tag names, controller slot, route, firmware, and external-access settings under version control with the controls team. A typo or stale tag map can be a valid request for the wrong data.
- Add timeouts, reconnect/backoff limits, stale-data detection, and a defined communications-loss state. Do not let an exception or a disconnected PLC silently become a permissive command.
- `pycomm3` is provided without guarantees for critical production systems. Validate behavior against the exact Logix firmware, communication module, Python version, and network architecture before deployment.

## Next door

For a higher-level, vendor-neutral interface, compare [asyncua](034-opcua.md) when the Rockwell system exposes an approved OPC UA gateway; for native Logix tag access, continue with the [pycomm3 LogixDriver documentation](https://pycomm3.readthedocs.io/en/latest/usage/logixdriver.html).

References: [pycomm3 documentation](https://pycomm3.readthedocs.io/en/latest/), [LogixDriver usage](https://pycomm3.readthedocs.io/en/latest/usage/logixdriver.html), and [PyPI project page](https://pypi.org/project/pycomm3/).

[1]: https://pycomm3.readthedocs.io/en/latest/ "pycomm3 documentation"
[2]: https://pycomm3.readthedocs.io/en/latest/usage/logixdriver.html "pycomm3 LogixDriver usage"
[3]: https://pypi.org/project/pycomm3/ "pycomm3 on PyPI"
[4]: https://www.odva.org/technology-standards/common-industrial-protocol-cip/ "ODVA Common Industrial Protocol overview"

<!-- Sources: [1] [2] [3] [4] -->

[pycomm3 documentation]: https://pycomm3.readthedocs.io/en/latest/ "pycomm3 documentation"
[LogixDriver usage]: https://pycomm3.readthedocs.io/en/latest/usage/logixdriver.html "pycomm3 LogixDriver usage"
[PyPI project page]: https://pypi.org/project/pycomm3/ "pycomm3 on PyPI"
[ODVA Common Industrial Protocol overview]: https://www.odva.org/technology-standards/common-industrial-protocol-cip/ "ODVA Common Industrial Protocol overview"
