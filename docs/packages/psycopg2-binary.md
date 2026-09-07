# 42 — PostgreSQL with psycopg2-binary

> `psycopg2` is the long-standing, battle-tested PostgreSQL adapter. The
> `-binary` wheel bundles the C library so there's no local build step —
> the pragmatic default for most projects still on psycopg2.

---

## install

```bash
pip install psycopg2-binary
```

---

## connect and run a query

```python
import psycopg2

conn = psycopg2.connect(host="localhost", dbname="app", user="app", password="secret")
cur = conn.cursor()

cur.execute("SELECT id, value FROM readings WHERE value > %s", (20,))
for row in cur.fetchall():
    print(row)

conn.close()
```

Placeholders are `%s` regardless of the underlying column type — psycopg2
adapts Python types (str, int, datetime, ...) to SQL automatically.

---

## insert and commit

```python
with conn.cursor() as cur:
    cur.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
conn.commit()
```

`conn` itself is a context manager for the transaction (commit on
success, rollback on exception) — the cursor context manager only closes
the cursor:

```python
with conn:
    with conn.cursor() as cur:
        cur.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
```

---

## rows as dicts

```python
from psycopg2.extras import RealDictCursor

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SELECT * FROM readings LIMIT 1")
print(cur.fetchone()["value"])
```

---

## error handling basics

```python
import psycopg2

try:
    cur.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
    conn.commit()
except psycopg2.IntegrityError as e:
    conn.rollback()
    print("constraint violated:", e)
except psycopg2.OperationalError as e:
    print("connection problem:", e)
```

Always `rollback()` after a failed statement — psycopg2 leaves the
transaction in a failed state until you do, and subsequent queries will
raise until it's cleared.

---

## snippets box

```python
# bulk insert efficiently
from psycopg2.extras import execute_values

execute_values(cur, "INSERT INTO readings (value) VALUES %s", [(1.1,), (2.2,), (3.3,)])
```

```python
# connection pooling for a multi-threaded app
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(1, 10, host="localhost", dbname="app")
conn = connection_pool.getconn()
# ... use it ...
connection_pool.putconn(conn)
```

---

## when to use what

| Need | Package |
|---|---|
| Stable, widely deployed, sync | `psycopg2-binary` |
| New project, async support | `psycopg` (v3) |
| ORM instead of raw SQL | `sqlalchemy` (works atop either) |

Next door: layer `sqlalchemy` on top for a query builder/ORM instead of
raw `%s` SQL.
