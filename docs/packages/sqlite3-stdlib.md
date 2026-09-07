# 41 — Built-in SQLite with sqlite3

> `sqlite3` ships in the standard library — no install, no server process.
> A single file (or `:memory:`) holds the whole database. Perfect for
> local tools, caches, and tests; not for concurrent multi-writer apps.

---

## install

```bash
# nothing to install — it's in the standard library
```

---

## connect and run a query

```python
import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY, value REAL)")
cur.execute("INSERT INTO readings (value) VALUES (?)", (23.4,))
conn.commit()

cur.execute("SELECT id, value FROM readings")
print(cur.fetchall())
conn.close()
```

Always use `?` placeholders, never f-strings, to avoid SQL injection and
to let SQLite handle type conversion correctly.

---

## use a context manager

```python
with sqlite3.connect("app.db") as conn:
    conn.execute("INSERT INTO readings (value) VALUES (?)", (25.1,))
    # commits automatically on successful exit; rolls back on exception
```

Note: the connection itself isn't closed by `with` — only the transaction
is committed/rolled back. Close explicitly, or use `closing()` from
`contextlib`.

---

## rows as dicts instead of tuples

```python
conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row

row = conn.execute("SELECT * FROM readings LIMIT 1").fetchone()
print(row["value"])
```

---

## error handling basics

```python
import sqlite3

try:
    conn = sqlite3.connect("app.db")
    conn.execute("INSERT INTO readings (value) VALUES (?)", (23.4,))
    conn.commit()
except sqlite3.IntegrityError as e:
    print("constraint violated:", e)
except sqlite3.OperationalError as e:
    print("db locked or bad SQL:", e)
```

---

## snippets box

```python
# in-memory database — gone when the connection closes, great for tests
conn = sqlite3.connect(":memory:")
```

```python
# WAL mode: better concurrent read/write behavior for multi-threaded apps
conn.execute("PRAGMA journal_mode=WAL")
```

---

## when to use what

| Need | Package |
|---|---|
| Local/embedded, single-process | `sqlite3` (stdlib) |
| Local/embedded but async | `aiosqlite` |
| Real server, many concurrent writers | `psycopg` / `pymysql` |

Next door: swap `sqlite3` for `aiosqlite` once your app moves to asyncio.
