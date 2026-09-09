# 43 — Modern PostgreSQL with psycopg (v3)

> `psycopg` (v3, sometimes called "psycopg3") is the next-generation
> PostgreSQL adapter — native async support, better type adaptation, and
> a cleaner API than psycopg2, while keeping the same SQL-first
> philosophy.

---

## install

```bash
python -m pip install "psycopg[binary]"
```

The `[binary]` extra bundles a prebuilt libpq like psycopg2's `-binary`
package did.

---

## connect and run a query (sync)

```python
import os
import psycopg

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id, value FROM readings WHERE value > %s", (20,))
        for row in cur.fetchall():
            print(row)
```

Both the connection and cursor are context managers here, and the
connection's `with` block commits on success / rolls back on exception —
no separate `conn.commit()` needed for the common case.

---

## async connection

```python
import asyncio
import os
import psycopg

async def main():
    async with await psycopg.AsyncConnection.connect(
        os.environ["DATABASE_URL"]
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, value FROM readings")
            rows = await cur.fetchall()
            print(rows)

asyncio.run(main())
```

---

## rows as dicts

```python
from psycopg.rows import dict_row

with psycopg.connect("...", row_factory=dict_row) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM readings LIMIT 1")
        row = cur.fetchone()
        print(row["value"])
```

---

## error handling basics

```python
import psycopg

try:
    with psycopg.connect("...") as conn:
        conn.execute("INSERT INTO readings (value) VALUES (%s)", (23.4,))
except psycopg.errors.UniqueViolation as e:
    print("duplicate:", e)
except psycopg.OperationalError as e:
    print("connection problem:", e)
```

The `with conn:` block auto-rolls-back on exception, so you don't need a
manual `conn.rollback()` like in psycopg2.

---

## snippets box

```python
# efficient bulk insert with executemany
import os
import psycopg

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO readings (value) VALUES (%s)",
            [(1.1,), (2.2,), (3.3,)],
        )
```

```python
# connection pool (separate package: python -m pip install psycopg-pool)
import os
from psycopg_pool import ConnectionPool

with ConnectionPool(os.environ["DATABASE_URL"]) as pool:
    with pool.connection() as conn:
        conn.execute("SELECT 1")
```

Set `DATABASE_URL` outside the source code. The examples assume a `readings`
table and a least-privilege database user; do not use a production password in
documentation or shell history.

---

## when to use what

| Need | Package |
|---|---|
| New project, async support, modern API | `psycopg` |
| Existing codebase, maximum ecosystem compatibility | `psycopg2-binary` |
| ORM layer on top | `sqlalchemy` |

Next door: use `psycopg_pool` for connection pooling under real
concurrent load.
