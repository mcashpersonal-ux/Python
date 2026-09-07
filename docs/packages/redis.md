# 46 — Redis with redis-py

> `redis` (the official `redis-py` client) talks to Redis — an in-memory
> key-value store used for caching, session storage, rate limiting, and
> pub/sub messaging. Fast because it's memory-resident; not a primary
> database for data you can't afford to lose.

---

## install

```bash
pip install redis
```

---

## connect and set/get a key

```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.set("sensor:line1:value", "23.4")
print(r.get("sensor:line1:value"))
```

`decode_responses=True` returns `str` instead of `bytes` — convenient
unless you're storing raw binary data.

---

## expiring keys (caching)

```python
r.set("cache:report", "...", ex=300) # expires in 300 seconds
r.setex("cache:report", 300, "...") # equivalent, explicit form
print(r.ttl("cache:report")) # seconds remaining, -1 if no expiry
```

---

## hashes, lists, and sets

```python
r.hset("sensor:line1", mapping={"value": 23.4, "unit": "C"})
print(r.hgetall("sensor:line1"))

r.lpush("events", "started")
r.rpush("events", "running")
print(r.lrange("events", 0, -1))

r.sadd("active_sensors", "line1", "line2")
print(r.smembers("active_sensors"))
```

---

## pub/sub

```python
def subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("alerts")
    for message in pubsub.listen():
        if message["type"] == "message":
            print(message["data"])

# elsewhere:
r.publish("alerts", "temperature high on line1")
```

---

## error handling basics

```python
import redis

try:
    r = redis.Redis(host="localhost", port=6379, socket_connect_timeout=3)
    r.ping()
except redis.ConnectionError as e:
    print("could not reach redis:", e)
except redis.TimeoutError as e:
    print("redis timed out:", e)
```

---

## snippets box

```python
# atomic increment — great for counters/rate limiting
r.incr("requests:count")
r.incrby("requests:count", 5)
```

```python
# pipeline: batch commands into one round trip
pipe = r.pipeline()
pipe.set("a", 1)
pipe.set("b", 2)
pipe.execute()
```

---

## when to use what

| Need | Package |
|---|---|
| Cache, sessions, pub/sub, rate limiting | `redis` |
| Durable time-series storage | `influxdb-client` |
| Durable relational storage | `psycopg` / `pymysql` |

Next door: use Redis as a broker for a task queue, or as a rate limiter
in front of `fastapi`.
