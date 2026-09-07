# 35 — MQTT with paho-mqtt

> `paho-mqtt` is the reference MQTT client — pub/sub messaging for IoT and
> industrial telemetry, talking to brokers like Mosquitto, HiveMQ, or a
> cloud IoT endpoint. Callback-based API on top of a background network
> loop.

---

## install

```bash
pip install paho-mqtt
```

---

## connect and subscribe

```python
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("connected:", reason_code)
    client.subscribe("plant/+/temperature")

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.local", 1883, keepalive=60)
client.loop_forever() # blocks; runs the network loop
```

`+` is a single-level wildcard (`plant/+/temperature` matches
`plant/line1/temperature`); `#` is a multi-level wildcard for everything
beneath a prefix.

---

## publish a message

```python
client.publish("plant/line1/temperature", payload="23.4", qos=1, retain=False)
```

QoS levels: `0` fire-and-forget, `1` at-least-once (may duplicate), `2`
exactly-once (slowest, most overhead). Use `1` for most telemetry.

---

## non-blocking usage (background thread)

```python
client.connect("broker.local", 1883)
client.loop_start() # spawns a background thread

client.publish("plant/line1/status", "running")
# ... do other work ...

client.loop_stop()
client.disconnect()
```

---

## error handling basics

```python
def on_disconnect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        print("unexpected disconnect:", reason_code)

client.on_disconnect = on_disconnect
client.reconnect_delay_set(min_delay=1, max_delay=30) # auto-reconnect backoff
```

Also set `client.on_connect_fail` to catch failures at the initial
handshake (wrong host, TLS mismatch, auth rejected).

---

## snippets box

```python
# auth + TLS
client.username_pw_set("user", "pass")
client.tls_set() # system CA certs; pass ca_certs= for a private CA
```

```python
# last will — broker publishes this if the client drops unexpectedly
client.will_set("plant/line1/status", payload="offline", qos=1, retain=True)
```

---

## when to use what

| Need | Package |
|---|---|
| Standard sync/callback MQTT client | `paho-mqtt` |
| Native asyncio integration | `aiomqtt` |

Next door: fan incoming messages into `influxdb-client` for storage, or
bridge them to Modbus/OPC UA tags.
