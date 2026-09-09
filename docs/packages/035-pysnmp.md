# 33 — SNMP with pysnmp

> `pysnmp` reads and writes management data (SNMP v1/v2c/v3) from network
> gear — switches, routers, UPSes, printers. Data is addressed by OID
> (Object Identifier) rather than register number.

---

## install

```bash
pip install pysnmp
```

---

## read a value (SNMP GET, v2c)

```python
from pysnmp.hlapi import (
    getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity,
)

iterator = getCmd(
    SnmpEngine(),
    CommunityData("public", mpModel=1), # v2c
    UdpTransportTarget(("192.168.1.1", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")), # sysDescr
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print(errorStatus.prettyPrint())
else:
    for varBind in varBinds:
        print(" = ".join([x.prettyPrint() for x in varBind]))
```

`1.3.6.1.2.1.1.1.0` (`sysDescr.0`) is a standard OID every SNMP device
implements — a good first thing to poll to confirm connectivity.

---

## walk a subtree (SNMP WALK)

```python
from pysnmp.hlapi import nextCmd

for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
    SnmpEngine(),
    CommunityData("public", mpModel=1),
    UdpTransportTarget(("192.168.1.1", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1")), # ifTable
    lexicographicMode=False,
):
    if errorIndication or errorStatus:
        break
    for varBind in varBinds:
        print(" = ".join([x.prettyPrint() for x in varBind]))
```

---

## write a value (SNMP SET)

```python
from pysnmp.hlapi import setCmd, Integer

errorIndication, errorStatus, errorIndex, varBinds = next(
    setCmd(
        SnmpEngine(),
        CommunityData("private", mpModel=1), # write community
        UdpTransportTarget(("192.168.1.1", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.2.1.1.6.0"), Integer(1)),
    )
)
```

---

## SNMP v3 (authenticated + encrypted)

```python
from pysnmp.hlapi import UsmUserData, usmHMACSHAAuthProtocol, usmAesCfb128Protocol

auth = UsmUserData(
    "admin", "authPasswordHere", "privPasswordHere",
    authProtocol=usmHMACSHAAuthProtocol,
    privProtocol=usmAesCfb128Protocol,
)
```

---

## error handling basics

```python
if errorIndication:
    print("transport/engine error:", errorIndication)
elif errorStatus:
    print("agent reported error:", errorStatus.prettyPrint(), "at", errorIndex)
```

`errorIndication` means the request never got a reply (timeout, wrong
community, unreachable). `errorStatus` means the device replied but
rejected the OID/value.

---

## when to use what

| Need | Package |
|---|---|
| Any SNMP version, full control | `pysnmp` |
| Async-first, actively maintained fork | `pysnmp-lextudio` |

Next door: log walked interface counters into `pandas` for trending.
