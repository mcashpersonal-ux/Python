# 113 — Network automation with NAPALM

> `napalm` (Network Automation and Programmability Abstraction Layer with Multivendor support) presents a common Python API for facts, telemetry, configuration diffs, and commits across network operating systems. It is useful for repeatable IT and OT network workflows, but driver coverage and device behavior remain vendor- and version-specific.

## Install

```bash
python -m pip install napalm
```

NAPALM installs its core drivers and transport dependencies. The current PyPI release requires Python 3.10 or newer; pin NAPALM and driver versions in an automation environment, and consult the support matrix before selecting a platform. Core documentation lists Arista EOS, Cisco IOS/IOS-XR/NX-OS, and Juniper JunOS; community drivers extend that list with their own installation and feature caveats.

The first example is **offline and demo-safe**: NAPALM's mock driver reads fixture data from a temporary directory and never opens a socket. The later connection examples are intentionally marked **live-device examples** and require an approved lab or maintenance window, reachable management access, and credentials supplied outside source code.

## First example: test a device workflow offline

A mock driver is valuable for CI and for developing inventory/reporting code before a switch, router, firewall, or OT gateway is available. The fixture filename follows the mock driver's call order: `open()` consumes the first call, so `get_facts()` reads `get_facts.1`.

```python
import json
import tempfile
from pathlib import Path

from napalm import get_network_driver

facts = {
    "hostname": "demo-switch",
    "fqdn": "demo-switch.example.invalid",
    "vendor": "Example Networks",
    "model": "virtual-lab",
    "serial_number": "OFFLINE-0001",
    "os_version": "demo-1.0",
    "uptime": 12345,
    "interface_list": ["mgmt0"],
}

with tempfile.TemporaryDirectory() as directory:
    fixture_path = Path(directory) / "get_facts.1"
    fixture_path.write_text(json.dumps(facts), encoding="utf-8")

    driver = get_network_driver("mock")
    with driver(
        hostname="offline-demo",
        username="unused",
        password="unused",
        optional_args={"path": directory},
    ) as device:
        result = device.get_facts()

print(f"{result['hostname']} — {result['vendor']} {result['model']}")
```

This pattern lets tests assert normalized fields without pretending that a simulated result proves a real device supports a getter. Add fixtures for `get_interfaces`, `get_environment`, or `cli` calls as needed, and test error fixtures as well as successful responses.

## Select a driver and inspect facts

NAPALM separates the driver name from the common operations. On a live device, `get_network_driver("ios")`, `get_network_driver("eos")`, `get_network_driver("nxos")`, or `get_network_driver("junos")` returns a platform driver. Transport details vary: for example, some drivers use SSH and others may use NETCONF or vendor SDKs. Verify the support matrix and platform-specific dependencies before deployment.

**Live-device example — do not run against production without authorization:**

```python
import os

from napalm import get_network_driver

hostname = os.environ["NAPALM_HOST"]
username = os.environ["NAPALM_USERNAME"]
password = os.environ["NAPALM_PASSWORD"]
driver = get_network_driver(os.environ.get("NAPALM_DRIVER", "ios"))

with driver(
    hostname,
    username,
    password,
    optional_args={"port": int(os.environ.get("NAPALM_PORT", "22"))},
) as device:
    facts = device.get_facts()
    interfaces = device.get_interfaces()

print(facts["hostname"], facts["os_version"])
for name, state in sorted(interfaces.items()):
    print(name, "up" if state["is_up"] else "down", state["speed"])
```

Use environment variables or a secret manager rather than putting passwords in a repository. A successful connection does not mean that every getter is supported or returns equally detailed data: normalize only fields whose semantics you have checked for the target driver.

## Compare and commit configuration safely

The usual change workflow is **load, compare, review, commit or discard**. `load_merge_candidate` creates a candidate configuration; `compare_config` returns the device's proposed diff; `commit_config` applies it. Prefer a small, reviewed change and use `discard_config` whenever the diff is unexpected.

**Live-device example — this can change device state:**

```python
import os

from napalm import get_network_driver

candidate = """interface Loopback99
description NAPALM-approved-lab-test
"""

driver = get_network_driver(os.environ.get("NAPALM_DRIVER", "ios"))
with driver(
    os.environ["NAPALM_HOST"],
    os.environ["NAPALM_USERNAME"],
    os.environ["NAPALM_PASSWORD"],
) as device:
    device.load_merge_candidate(config=candidate)
    diff = device.compare_config()
    print(diff or "No change")

    if not diff:
        device.discard_config()
    elif os.environ.get("NAPALM_APPROVE") == "yes":
        device.commit_config()
    else:
        device.discard_config()
        raise SystemExit("Change not approved; candidate discarded")
```

The exact configuration syntax, merge semantics, rollback behavior, commit-confirm support, and candidate handling differ by driver. Treat the printed diff as a review aid, not as a proof that the resulting operational state is correct. When supported by the platform, use commit-confirm or an equivalent rollback safeguard and verify the post-change state with getters.

## Inventory multiple vendors without coupling the report

A useful operational pattern is to keep inventory data (host, driver, and credential reference) separate from reporting code. One failed device should be recorded with an error and a bounded timeout rather than stopping an entire fleet report. For OT networks, run collection from an approved management zone and consider a read-only account and a maintenance-aware polling schedule.

```python
import os

from napalm import get_network_driver

inventory = [
    {"host": "edge-eos.example.invalid", "driver": "eos"},
    {"host": "core-ios.example.invalid", "driver": "ios"},
]

for item in inventory:
    try:
        driver = get_network_driver(item["driver"])
        with driver(
            item["host"],
            os.environ["NAPALM_USERNAME"],
            os.environ["NAPALM_PASSWORD"],
            optional_args={"timeout": 10},
        ) as device:
            facts = device.get_facts()
        print({"host": item["host"], "hostname": facts["hostname"], "model": facts["model"]})
    except Exception as error:
        print({"host": item["host"], "error": type(error).__name__})
```

For production, replace the simple print statements with structured, access-controlled logs. Record the driver, software version, timestamp, collection result, and error class, but do not log passwords, private keys, or full sensitive configurations.

## Package and platform caveats

NAPALM's unified API is an abstraction, not a compatibility guarantee. The support matrix documents getter and configuration coverage, and its caveats are as important as the list of supported operating systems. Some platforms require additional libraries, NETCONF enablement, vendor SDKs, or OS-specific packages; Linux, macOS, Windows, and BSD environments may differ in dependency and transport support. Pin a tested Python/driver combination and test against the exact NOS release and hardware family.

## Safety notes

- Treat all connection and configuration snippets after the mock example as **live-device operations**. Use an isolated lab, a read-only account for discovery, least-privilege credentials, and an explicit change approval process.
- Never embed passwords, API tokens, private keys, or enable secrets in source code. Use a secret manager or environment injection, restrict file permissions, and redact them from logs and diffs.
- Validate host keys, TLS or NETCONF trust settings, management ACLs, and timeouts. Do not disable certificate or host-key verification just to make a connection work.
- Review `compare_config()` output manually and test rollback before using `commit_config()`. Do not assume that an empty diff, a successful commit, or a returned getter proves the physical or control process is safe.
- In OT and safety-related networks, separate monitoring from control, use an approved jump host or management zone, avoid scanning control traffic, and schedule polling and changes around process constraints. Never automate a field action merely because a network configuration change succeeded.
- Confirm driver support for every getter and configuration method on the exact device and NOS version. Catch and audit exceptions; do not silently interpret an unsupported or stale result as healthy.
- Keep configuration backups, candidate diffs, approvals, timestamps, and post-change verification under access control. Test upgrades in a lab because transport libraries and vendor APIs can change behavior.

## Next door

Next door: read the [NAPALM documentation](https://napalm.readthedocs.io/) and its [support matrix](https://napalm.readthedocs.io/en/latest/support/index.html), then consider [Paramiko](107-paramiko.md) when you need lower-level SSH/SFTP control rather than a normalized network-device API.

## References

[1]: https://napalm.readthedocs.io/ "NAPALM documentation"
[2]: https://napalm.readthedocs.io/en/latest/installation/ "NAPALM installation"
[3]: https://napalm.readthedocs.io/en/latest/support/index.html "NAPALM supported devices and caveats"
[4]: https://napalm.readthedocs.io/en/latest/tutorials/mock_driver.html "NAPALM mock driver"
[5]: https://pypi.org/project/napalm/ "NAPALM on PyPI"

<!-- Sources: [1] [2] [3] [4] [5] -->
