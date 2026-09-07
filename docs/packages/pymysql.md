# 44 — MySQL with PyMySQL

> `PyMySQL` is a pure-Python MySQL/MariaDB client — no C extension to
> compile, easy to install anywhere Python runs. Slightly slower than
> C-backed drivers but simpler to deploy.

---

## install

```bash
pip install PyMySQL
```

---

## connect and run a query

```python
import pymysql

conn = pymysql.connect(host="localhost", user="app", password="secret", database="app", charset="utf8mb4")
cur = conn.cursor()

cur.execute("SELECT id, value FROM readings WHERE value > %s", (20,))
for row in cur.fetchall():
    print(row)

conn.close()
```

Always set `charset="utf8mb4"` explicitly — MySQL's historic `utf8`
default is actually a 3-byte subset that can't store full Unicode
(emoji, some CJK characters).

---

## insert and commit

```python
with conn.cursor() as cur:
    cur.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
conn.commit()
```

PyMySQL doesn't autocommit by default — always call `conn.commit()`, or
pass `autocommit=True` to `pymysql.connect(...)`.

---

## rows as dicts

```python
import pymysql.cursors

conn = pymysql.connect(host="localhost", user="app", password="secret",
                        database="app", cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute("SELECT * FROM readings LIMIT 1")
print(cur.fetchone()["value"])
```

---

## error handling basics

```python
import pymysql

try:
    cur.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
    conn.commit()
except pymysql.err.IntegrityError as e:
    conn.rollback()
    print("constraint violated:", e)
except pymysql.err.OperationalError as e:
    print("connection problem:", e)
```

---

## snippets box

```python
# bulk insert
cur.executemany("INSERT INTO readings (value) VALUES (%s)", [(1.1,), (2.2,), (3.3,)])
conn.commit()
```

```python
# use as a context manager for the connection too
with pymysql.connect(host="localhost", user="app", password="secret", database="app") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
```

---

## when to use what

| Need | Package |
|---|---|
| Pure-Python, easiest install | `PyMySQL` |
| ORM on top | `sqlalchemy` (works with PyMySQL as a driver) |
| PostgreSQL instead | `psycopg` |

Next door: layer `sqlalchemy` on top for connection pooling and a query
builder.
