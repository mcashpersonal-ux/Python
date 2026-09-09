# 112 — OT packet analysis with Scapy

> `scapy` is a Python packet-construction and dissection toolkit. It can decode captured traffic, inspect protocol fields, and build test packets for authorized diagnostics without forcing every workflow through a fixed request/response abstraction.

## Install

```bash
python -m pip install scapy
```

Scapy's current documentation supports Python 3.7 and newer for the 2.x series.[1] Basic packet construction and offline dissection do not require a network adapter, a GUI, or proprietary hardware. Live capture and transmission are platform-dependent: Linux can use native packet sockets, while Windows requires an installed Npcap driver; permissions and capture-filter support also vary by operating system.[1] Optional features such as plotting, PDF/PS dumps, and some protocol integrations require additional packages.[1]

## First example: dissect a packet offline

Start with deterministic bytes rather than a live interface. This example creates an Ethernet/IP/UDP packet in memory, serializes it, parses it back, and prints selected fields. It is **offline and demo-safe**: it opens no socket, needs no capture file, and does not transmit anything.

```python
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

original = (
    Ether(src="02:00:00:00:00:01", dst="02:00:00:00:00:02")
    / IP(src="192.0.2.10", dst="198.51.100.20", ttl=32)
    / UDP(sport=4000, dport=502)
    / Raw(load=b"demo-register-read")
)

wire_bytes = bytes(original)
parsed = Ether(wire_bytes)

print(parsed.summary())
print("source:", parsed[IP].src)
print("destination:", parsed[IP].dst)
print("UDP ports:", parsed[UDP].sport, "->", parsed[UDP].dport)
print("payload:", bytes(parsed[Raw].load))
```

The `/` operator stacks protocol layers. Calling `bytes()` forces serialization, which is useful for exercising length and checksum calculation before a packet reaches a test harness. Re-parsing the result models what a receiver or a pcap reader does, but it does not prove that a real device accepts the packet.

## Inspect layers and fields

Use `summary()` for a compact event line, `show()` for a human-readable field tree, and `hexdump()` when byte offsets or an unexpected payload matter.[2] Access a layer with `packet[Layer]` only after checking that the layer is present; heterogeneous captures will not all contain the same protocol stack.

```python
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy.packet import Raw
from scapy.utils import hexdump

packet = (
    Ether()
    / IP(src="203.0.113.7", dst="192.0.2.25")
    / TCP(sport=45000, dport=44818, flags="PA", seq=10, ack=20)
    / Raw(load=b"authorized-lab-payload")
)

print(packet.summary())
packet.show()
hexdump(packet)

if IP in packet and TCP in packet:
    print(f"{packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")
if Raw in packet:
    print("payload length:", len(packet[Raw].load))
```

For industrial protocols, begin by identifying transport and direction before interpreting application bytes. A TCP destination port is only a hint; port assignments can be changed, proxied, or reused. Confirm the protocol specification and the device's documented framing before labeling a payload as a register, command, or alarm.

## Read a pcap without capturing live traffic

`rdpcap()` loads an existing pcap or pcapng file for offline review, and `wrpcap()` can save a selected subset for a test fixture.[2] Keep the input path explicit and treat capture files as sensitive evidence. The following command is runnable when `capture.pcap` exists and reports only packets containing IPv4 and TCP layers.

```python
from pathlib import Path

from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap

capture_path = Path("capture.pcap")
if not capture_path.is_file():
    raise SystemExit(f"capture not found: {capture_path}")

packets = rdpcap(str(capture_path))
for number, packet in enumerate(packets, start=1):
    if IP in packet and TCP in packet:
        print(
            number,
            packet[IP].src,
            packet[TCP].sport,
            "->",
            packet[IP].dst,
            packet[TCP].dport,
            packet[TCP].flags,
            "bytes=",
            len(bytes(packet)),
        )
```

For repeatable analysis, save a small redacted fixture and write assertions over fields such as endpoint, transport flags, payload length, or an application-level checksum. Avoid treating packet counts alone as proof of process health; captures can be incomplete, mirrored in the wrong direction, or affected by offload behavior.

## Filter a capture for an authorized live diagnostic

Live capture is a **device- and permission-dependent example**. Run it only on an approved interface, segment, and maintenance scope. A BPF filter reduces traffic delivered to Scapy; it is not an authorization boundary and it does not replace network ACLs. Stop after a bounded count or timeout rather than leaving an uncontrolled collector running.

```python
from scapy.layers.inet import IP, UDP
from scapy.sendrecv import sniff


def report(packet):
    if IP in packet and UDP in packet:
        print(
            f"{packet[IP].src}:{packet[UDP].sport} -> "
            f"{packet[IP].dst}:{packet[UDP].dport} "
            f"len={len(bytes(packet))}"
        )


packets = sniff(
    iface=None,  # Replace with an approved interface name when required.
    filter="udp",
    count=10,
    timeout=30,
    prn=report,
    store=False,
)
print("observed packets:", len(packets))
```

On systems where `iface=None` does not select the intended interface, replace it with an explicit interface name. A live capture may require elevated privileges, libpcap/Npcap, and OS-specific configuration. Prefer a switch mirror, SPAN session, or approved tap when observing an OT segment so the diagnostic host does not become an inline dependency.

## Build a test corpus for protocol decoders

Packet layers make useful fixtures for a decoder that should be tested without a PLC, gateway, or field network. Keep the fixture's addresses in documentation ranges, use a clearly marked payload, and verify both expected and malformed cases. For real protocol support, use the relevant Scapy layer when one exists; otherwise parse only the documented application framing and preserve unknown bytes.

```python
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.packet import Raw

frames = [
    Ether() / IP(src="192.0.2.1", dst="198.51.100.1") / UDP(sport=1000, dport=2000) / Raw(load=b"OK"),
    Ether() / IP(src="192.0.2.2", dst="198.51.100.2") / UDP(sport=1001, dport=2001) / Raw(load=b"BAD"),
]

for frame in frames:
    payload = bytes(frame[Raw].load) if Raw in frame else b""
    result = "accepted" if payload == b"OK" else "review"
    print(frame[IP].src, result, payload.hex())
```

A fixture is a model of bytes, not a device certification. Add tests for truncation, duplicate messages, unexpected sequence values, endian choices, and invalid lengths before using a decoder in an operational report.

## Package and platform caveats

Scapy's core is pure Python, but live I/O depends on the host networking stack and capture backend. Linux commonly uses native packet sockets and may use libpcap for BPF compilation; macOS can use native support or libpcap; Windows needs Npcap for supported capture and send workflows.[1] Root or administrator privileges may be required for transmission and some capture operations.[2] GUI-free operation is the safer default for servers and jump hosts; plotting and graphical packet dumps are optional features and should not be assumed available in headless environments.[1]

## Safety notes

Use Scapy only on networks, hosts, and captures for which you have explicit authorization. Prefer offline pcaps and synthetic packets while developing, and use documentation-range addresses in fixtures. Do not send crafted packets, probes, ARP requests, DHCP discovers, or industrial control messages into a production or safety-related segment merely to see what happens. Packet capture can expose credentials, process data, topology, and personal information; restrict file permissions, encrypt storage, minimize retention, and redact exports. Apply bounded counts and timeouts, narrow BPF filters, and a read-only observation point. Never infer that an observed packet means a command was executed or that an absent packet means equipment is safe. Validate interpretations against protocol specifications and device documentation, and coordinate live diagnostics with the site's change-control, incident-response, and process-safety procedures.

## Next door

Next door: use the [Scapy usage guide](https://scapy.readthedocs.io/en/latest/usage.html) for layer and capture details, then pair offline packet fixtures with a protocol-specific decoder and a structured evidence log.

## References

[1]: https://scapy.readthedocs.io/en/latest/installation.html "Scapy installation and platform requirements"
[2]: https://scapy.readthedocs.io/en/latest/usage.html "Scapy usage, packet dissection, pcap, and capture examples"

<!-- Sources: [1] [2] -->
