# 47 — Time-series storage with influxdb-client

> `influxdb-client` is the official Python client for InfluxDB 2.x — a
> database purpose-built for time-series data. A natural home for
> telemetry polled from Modbus/OPC UA/MQTT sources elsewhere in this
> catalog.

---

## install

```bash
pip install influxdb-client
```

---

## connect and write a point

```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

point = Point("readings").tag("sensor", "line1").field("value", 23.4)
write_api.write(bucket="telemetry", record=point)
```

Tags (`sensor=line1`) are indexed and used for filtering; fields
(`value=23.4`) are the actual measured data — this split matters for
query performance at scale.

---

## write several points at once

```python
points = [
    Point("readings").tag("sensor", "line1").field("value", 23.4),
    Point("readings").tag("sensor", "line2").field("value", 24.1),
]
write_api.write(bucket="telemetry", record=points)
```

---

## query with Flux

```python
query_api = client.query_api()

query = '''
from(bucket: "telemetry")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "readings" and r.sensor == "line1")
'''
tables = query_api.query(query)
for table in tables:
    for record in table.records:
        print(record.get_time(), record.get_value())
```

---

## query into a pandas DataFrame

```python
df = query_api.query_data_frame(query)
print(df.head())
```

---

## error handling basics

```python
from influxdb_client.rest import ApiException

try:
    write_api.write(bucket="telemetry", record=point)
except ApiException as e:
    print("influx write failed:", e.status, e.reason)
```

Also wrap client creation in a try/except for connection issues (wrong
URL, expired token, org mismatch) — those surface at the first request.

---

## snippets box

```python
# async write buffering for high-frequency polling
from influxdb_client.client.write_api import ASYNCHRONOUS

write_api = client.write_api(write_options=ASYNCHRONOUS)
```

```python
# close the client when your app shuts down
client.close()
```

---

## when to use what

| Need | Package |
|---|---|
| Time-series telemetry, dashboards | `influxdb-client` |
| General relational data | `psycopg` / `pymysql` |
| Fast ephemeral cache | `redis` |

Next door: feed points from a `pymodbus` polling loop straight into
`write_api.write(...)`.
