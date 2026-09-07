# 34 — Maintained SNMP fork: pysnmp-lextudio

> The original `pysnmp` project stalled; `pysnmp-lextudio` is the
> community-maintained continuation with the same API plus ongoing bug
> fixes and Python compatibility updates. Install this one for new work.

---

## install

```bash
pip install pysnmp-lextudio
```

Note the import name is unchanged — code stays `import pysnmp..`, only
the PyPI package name differs. If both `pysnmp` and `pysnmp-lextudio` end
up installed, uninstall the abandoned one to avoid version conflicts.

---

## read a value (SNMP GET, v2c)

```python
from pysnmp.hlapi import (
    getCmd, SnmpEngine, CommunityData, UdpTransportTarget,
    ContextData, ObjectType, ObjectIdentity,
)

iterator = getCmd(
    SnmpEngine(),
    CommunityData("public", mpModel=1),
    UdpTransportTarget(("192.168.1.1", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
if not errorIndication and not errorStatus:
    for varBind in varBinds:
        print(" = ".join([x.prettyPrint() for x in varBind]))
```

---

## async client (v3 stack)

The lextudio fork adds a cleaner asyncio-native entry point in newer
releases:

```python
import asyncio
from pysnmp.hlapi.v3arch.asyncio import (
    get_cmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData,
    ObjectType, ObjectIdentity,
)

async def main():
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        SnmpEngine(),
        CommunityData("public", mpModel=1),
        await UdpTransportTarget.create(("192.168.1.1", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),
    )
    for varBind in varBinds:
        print(" = ".join([x.prettyPrint() for x in varBind]))

asyncio.run(main())
```

Check your installed version's docs — the asyncio-native module path has
shifted across releases as the fork matured.

---

## error handling basics

Same shape as classic `pysnmp`: check `errorIndication` (transport-level)
before `errorStatus` (agent-level rejection).

```python
if errorIndication:
    print("no reply:", errorIndication)
elif errorStatus:
    print("device rejected request:", errorStatus.prettyPrint())
```

---

## snippets box

```python
# walk a table asynchronously in the newer API
from pysnmp.hlapi.v3arch.asyncio import next_cmd

async def walk():
    obj = ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1"))
    target = await UdpTransportTarget.create(("192.168.1.1", 161))
    while True:
        errorIndication, errorStatus, errorIndex, varBinds = await next_cmd(
            SnmpEngine(), CommunityData("public", mpModel=1), target, ContextData(), obj
        )
        if errorIndication or errorStatus or not varBinds:
            break
        for varBind in varBinds:
            print(varBind)
        obj = ObjectType(ObjectIdentity(varBinds[0][0]))
```

---

## when to use what

| Need | Package |
|---|---|
| New projects — actively maintained | `pysnmp-lextudio` |
| Legacy code already pinned to classic `pysnmp` | `pysnmp` |

Next door: expose walked metrics over `fastapi` for a lightweight
monitoring endpoint.
