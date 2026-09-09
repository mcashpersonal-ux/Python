# 96 — BACnet with bacpypes3

> `bacpypes3` is an asyncio-based Python library for building BACnet applications. It models devices and objects used by building-automation systems—such as HVAC setpoints, lighting states, and access-control points—and can communicate over BACnet/IP without requiring a vendor GUI.

## Install

```bash
python -m pip install bacpypes3
```

The current project documents Python 3.8 and newer and supports Linux, macOS, and Windows. The core package has no required third-party dependencies. Install `ifaddr` when you want interface discovery, `websockets` for BACnet/SC experiments, and `PyYAML` for YAML-based configuration. BACpypes3 speaks BACnet/IP and BACnet/IPv6; an MSTP field bus normally needs a BACnet router or another suitable interface.

## First example: an offline point model

Begin by exercising BACnet object classes without opening a socket. This demo creates an analog HVAC setpoint and a binary lighting point, changes their present values, and prints the resulting local model. It is safe for a laptop or CI runner: it does not contact a controller, require a GUI, or transmit BACnet packets.

```python
from bacpypes3.local.analog import AnalogValueObject
from bacpypes3.local.binary import BinaryValueObject

hvac_setpoint = AnalogValueObject(
    objectIdentifier=("analogValue", 1),
    objectName="office-cooling-setpoint",
    presentValue=24.0,
    statusFlags=[0, 0, 0, 0],
    covIncrement=0.5,
    units="degreesCelsius",
    description="Simulated HVAC cooling setpoint",
)

lobby_lights = BinaryValueObject(
    objectIdentifier=("binaryValue", 1),
    objectName="lobby-lights",
    presentValue="inactive",
    statusFlags=[0, 0, 0, 0],
    description="Simulated lobby lighting command",
)

hvac_setpoint.presentValue = 23.5
lobby_lights.presentValue = "active"

print(f"{hvac_setpoint.objectName}: {hvac_setpoint.presentValue:.1f} C")
print(f"{lobby_lights.objectName}: {lobby_lights.presentValue}")
```

BACnet object identifiers are an object type plus an instance number, such as `("analogValue", 1)`. Keep the instance numbers and engineering units in a point list shared with the controls engineer; a valid BACnet message aimed at the wrong object is still an operational error.

## Expose simulated points on BACnet/IP

For an integration test, expose local objects through a small BACnet device. The following is adapted from the project's device samples. It binds the application using BACpypes3's argument parser, so run it only on an isolated lab network or with an explicitly selected loopback/lab address. It does not need a proprietary controller, but it does open a BACnet/IP UDP socket (normally port 47808) and waits until interrupted.

```python
import asyncio

from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.local.analog import AnalogValueObject
from bacpypes3.local.binary import BinaryValueObject


async def main() -> None:
    parser = SimpleArgumentParser()
    args = parser.parse_args(
        ["--name", "BuildingLab", "--instance", "9001", "--address", "127.0.0.1/24"]
    )
    app = Application.from_args(args)

    app.add_object(
        AnalogValueObject(
            objectIdentifier=("analogValue", 1),
            objectName="ahu-1-supply-air-setpoint",
            presentValue=18.0,
            statusFlags=[0, 0, 0, 0],
            covIncrement=0.5,
            units="degreesCelsius",
        )
    )
    app.add_object(
        BinaryValueObject(
            objectIdentifier=("binaryValue", 1),
            objectName="access-door-release-request",
            presentValue="inactive",
            statusFlags=[0, 0, 0, 0],
        )
    )

    print("Lab device is listening on loopback; press Ctrl-C to stop")
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
```

The exact address syntax can vary with the installed BACpypes3 release and platform. If the explicit loopback address is rejected, consult the package's address documentation and choose an unused address on a dedicated test interface rather than discovering or binding a production interface. A real device would also need a unique BACnet device instance, a planned network number, and an approved BBMD or foreign-device design when crossing subnets.

## HVAC, lighting, and access-control patterns

BACnet objects are a useful boundary between equipment semantics and transport. Typical mappings include an `analogInput` for a supply-air temperature, an `analogValue` for a simulated or supervisory setpoint, a `binaryInput` for an occupancy contact, and a `binaryOutput` or commandable `binaryValue` for a lighting or door-release request. Preserve `units`, `statusFlags`, descriptions, and relinquish/priority behavior so a supervisory system can distinguish a healthy reading from an overridden or unavailable one.

For commandable points, use the priority array rather than silently overwriting another operator or sequence. A small commandable class can be defined from the package's local object and commandable mixin:

```python
from bacpypes3.local.analog import AnalogValueObject
from bacpypes3.local.cmd import Commandable


class CommandableSetpoint(Commandable, AnalogValueObject):
    """An HVAC setpoint whose priority array accepts BACnet commands."""


setpoint = CommandableSetpoint(
    objectIdentifier=("analogValue", 10),
    objectName="conference-room-setpoint",
    presentValue=22.0,
    statusFlags=[0, 0, 0, 0],
    covIncrement=0.5,
    units="degreesCelsius",
)

print(f"Initial setpoint: {setpoint.presentValue:.1f} C")
```

For lighting, expose occupancy and commanded state separately so a schedule does not erase a manual override. For access control, treat a BACnet command as a request—not proof that a lock physically opened—and publish a separate status/alarm point from the door controller. HVAC writes should be bounded by comfort and equipment limits, while lighting and door commands should be authorized and auditable.

## Reading and writing live devices

BACpypes3 applications are commonly both clients and servers. The official samples include discovery, `read-property`, `write-property`, change-of-value, and custom-client examples. Use those samples as the starting point for a client that targets an approved controller, then add connection supervision, timeouts, retries with backoff, and logging of device/object/property identifiers. Do not copy a live address into the loopback demo above.

A practical commissioning workflow is to discover devices first, read `objectName`, `objectType`, `objectList`, `units`, `statusFlags`, and present values, and only then map points into an HVAC, lighting, or access-control service. Treat `writeProperty` as a controlled operation: verify the current value, issue the smallest permitted change at an explicit priority, and confirm the resulting value and equipment feedback.

## Safety notes

- **Do not point an unreviewed example at a live building network.** Start with object-only tests, then loopback, then an isolated lab VLAN with a simulator or test controller.
- BACnet/IP commonly uses UDP port 47808. Segment and firewall it; do not disable a host firewall as a debugging shortcut. Restrict peers and use BACnet/SC or an approved secure architecture where appropriate.
- BACnet is not an authorization system. Enforce operator identity, least privilege, command allow-lists, HVAC range checks, lighting schedules, door interlocks, and audit records in the surrounding application.
- Never infer physical completion from an accepted protocol write. Confirm a door position, fan status, valve feedback, alarm state, and fail-safe behavior from independent status points.
- Give each device a unique instance and document object identifiers, units, priorities, network numbers, and timezone/clock assumptions. Test stale data, duplicate devices, reconnects, malformed peers, and loss of communications before deployment.
- Platform backends matter: BACnet/IP needs a usable network interface, while BACnet/SC needs the optional WebSocket dependency and a certificate/trust design. BACpypes3 does not replace a certified controller, safety system, or building cybersecurity review.

## Next door

For a higher-level building-automation API with local objects and scanning helpers, compare [BAC0](https://bac0.readthedocs.io/) after learning the underlying BACpypes3 object and priority model. The [BACpypes3 samples](https://bacpypes3.readthedocs.io/en/stable/samples/) are the best next step for discovery and read/write clients.

References: [BACpypes3 documentation](https://bacpypes3.readthedocs.io/) and the [PyPI project page](https://pypi.org/project/bacpypes3/).
