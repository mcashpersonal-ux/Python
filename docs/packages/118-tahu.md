# 100 — Sparkplug B with tahu

> `tahu` is a small Python implementation of Sparkplug B, the MQTT payload and topic convention used to move stateful industrial telemetry between edge nodes, devices, brokers, and SCADA applications. It is useful for constructing and decoding protobuf payloads before connecting them to a real MQTT client.

## Install

```bash
python -m pip install tahu
```

The package on PyPI is version `0.1.2`, released in 2022, and declares Python 3.8 through 3.10 support. It is a platform-independent wheel, but its generated protobuf code can be sensitive to the installed `protobuf` runtime. Pin and test dependencies in the same environment as the gateway that will run them. `tahu` creates Sparkplug payloads; it does not provide an MQTT broker or an MQTT client transport.

## Build and inspect a payload offline

The safest first step is to create a payload locally. This example needs no PLC, broker, network, or GUI. It adds a temperature metric, serializes the Sparkplug B protobuf, and parses it again so the result can be inspected before publishing.

```python
from tahu import sparkplug_b

payload = sparkplug_b.sparkplug_b_pb2.Payload()
sparkplug_b.addMetric(
    payload,
    name="Line1/Temperature",
    alias=None,
    type=sparkplug_b.MetricDataType.Double,
    value=72.4,
)

wire_bytes = payload.SerializeToString()
received = sparkplug_b.sparkplug_b_pb2.Payload()
received.ParseFromString(wire_bytes)

metric = received.metrics[0]
print(f"encoded={len(wire_bytes)} bytes")
print(metric.name, metric.double_value, metric.datatype)
```

`addMetric` sets the metric datatype and a millisecond timestamp. The resulting bytes are a Sparkplug B payload, not JSON; an MQTT client publishes those bytes as the message body.

## Map a node to Sparkplug topics

Sparkplug topic names carry the namespace, message type, group, edge node, and optional device. A typical edge-node telemetry topic is:

```text
spBv1.0/<group>/DDATA/<edge_node>/<device>
```

For example, `spBv1.0/FactoryA/DDATA/BoilerGateway/Boiler01` can carry a device-data payload. Birth and death messages establish lifecycle state, so a SCADA subscriber can distinguish a current value from a node that has gone offline. Use the topic and lifecycle rules from the [Sparkplug specification][2] rather than inventing application-specific topic variants.

## Add multiple telemetry points

A single payload can carry several metrics from one sampling cycle. Keeping the values together makes a timestamped scan easier for a downstream historian or SCADA adapter to process.

```python
from tahu import sparkplug_b

payload = sparkplug_b.sparkplug_b_pb2.Payload()
metrics = [
    ("Pump01/Running", sparkplug_b.MetricDataType.Boolean, True),
    ("Pump01/SpeedRpm", sparkplug_b.MetricDataType.Double, 1450.0),
    ("Pump01/Mode", sparkplug_b.MetricDataType.String, "AUTO"),
]

for name, data_type, value in metrics:
    sparkplug_b.addMetric(payload, name, None, data_type, value)

for metric in payload.metrics:
    print(metric.name, metric.datatype)
```

Use aliases only when the receiving Sparkplug implementation has agreed on the alias-to-name mapping. Prefer stable metric names for initial commissioning because they are easier to audit in a tag database.

## Publish through an MQTT client

`tahu` is the payload layer. For a live broker, pair it with an MQTT library such as `paho-mqtt`, configure TLS and credentials, and publish the serialized bytes with the correct QoS. The following pattern shows the boundary between payload construction and transport; it assumes a reachable broker and deliberately does not connect when run as written.

```python
from tahu import sparkplug_b

mqtt_topic = "spBv1.0/FactoryA/DDATA/BoilerGateway/Boiler01"
payload = sparkplug_b.sparkplug_b_pb2.Payload()
sparkplug_b.addMetric(
    payload,
    "Boiler01/OutletPressureKpa",
    None,
    sparkplug_b.MetricDataType.Double,
    318.6,
)

wire_bytes = payload.SerializeToString()
print(f"publish {len(wire_bytes)} bytes to {mqtt_topic}")
# In a configured gateway, pass mqtt_topic and wire_bytes to an MQTT client's publish().
```

For a real Sparkplug node, implement the complete lifecycle: publish node/device birth messages after connecting, send data messages, publish death messages when shutting down, and configure the MQTT last-will message so unexpected loss is visible to SCADA subscribers. Test with a disposable broker and a non-production group before connecting to plant systems.

## Decode incoming telemetry

A subscriber that already receives Sparkplug B bytes can parse them with the same protobuf module. The value field to read depends on `metric.datatype`; do not assume every metric is a `double_value`.

```python
from tahu import sparkplug_b

incoming = sparkplug_b.sparkplug_b_pb2.Payload()
sparkplug_b.addMetric(
    incoming,
    "Tank01/LevelPercent",
    None,
    sparkplug_b.MetricDataType.Double,
    63.5,
)

encoded = incoming.SerializeToString()
received = sparkplug_b.sparkplug_b_pb2.Payload()
received.ParseFromString(encoded)

for metric in received.metrics:
    if metric.datatype == sparkplug_b.MetricDataType.Double:
        print(metric.name, metric.double_value, metric.timestamp)
```

In production, validate topic namespace, group, node, device, datatype, timestamp, and metric name before writing to a historian or using a value in control logic. Treat malformed or unexpected messages as input validation failures.

## Safety notes

- **Do not connect the first test to a live PLC or plant broker.** Generate and decode payloads offline, then use a private test broker and a non-production namespace.
- **Sparkplug birth/death state is operational data.** A missing death message or an incorrect last-will configuration can make an edge node appear healthy when it is not. Test reconnects, broker restarts, and abrupt process termination.
- **Use MQTT security.** Require TLS, verify the broker certificate, use unique credentials, and grant publish/subscribe permissions only to the required Sparkplug topics. Never put passwords in source code.
- **Validate telemetry before control use.** Check datatype, timestamp freshness, range, quality/status conventions, and metric identity before a value reaches alarms, historians, or closed-loop control.
- **Check compatibility before deployment.** The PyPI `tahu` package is an older, small distribution and is separate from the broader [Eclipse Tahu reference repository][1]. Pin the package and protobuf versions that pass your integration tests.

Next door: pair `tahu` with [`paho-mqtt`](https://pypi.org/project/paho-mqtt/) for broker transport, and consult the [Eclipse Tahu examples][1] when implementing full Sparkplug lifecycle behavior.

## References

[1]: https://github.com/eclipse-tahu/tahu "Eclipse Tahu reference implementations"
[2]: https://www.eclipse.org/tahu/spec/sparkplug_spec.pdf "Sparkplug Specification 3.0.0"
[3]: https://pypi.org/project/tahu/ "tahu on PyPI"
