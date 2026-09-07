# 48 — Async SQLite with aiosqlite

> `aiosqlite` wraps the stdlib `sqlite3` module in an asyncio-friendly
> API — same SQLite file format and SQL dialect, but non-blocking so it
> fits into an existing asyncio application without stalling the event
> loop.

---

## install

```bash
pip install aiosqlite
```

---

## connect and run a query

```python
import asyncio
import aiosqlite

async def main():
    async with aiosqlite.connect("app.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY, value REAL)")
        await db.execute("INSERT INTO readings (value) VALUES (?)", (23.4,))
        await db.commit()

        async with db.execute("SELECT id, value FROM readings") as cursor:
            async for row in cursor:
                print(row)

asyncio.run(main())
```

---

## rows as dicts

```python
async def query_dicts():
    async with aiosqlite.connect("app.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM readings LIMIT 1") as cursor:
            row = await cursor.fetchone()
            print(row["value"])
```

---

## error handling basics

```python
import aiosqlite

async def safe_insert(value):
    try:
        async with aiosqlite.connect("app.db") as db:
            await db.execute("INSERT INTO readings (value) VALUES (?)", (value,))
            await db.commit()
    except aiosqlite.IntegrityError as e:
        print("constraint violated:", e)
    except aiosqlite.OperationalError as e:
        print("db locked or bad SQL:", e)
```

SQLite only allows one writer at a time — under concurrent asyncio
writes you may still see `OperationalError: database is locked`; WAL mode
(below) reduces but doesn't eliminate this.

---

## snippets box

```python
# WAL mode for better concurrent access
async def enable_wal(db):
    await db.execute("PRAGMA journal_mode=WAL")
```

```python
# fetchall instead of iterating
async def fetch_all():
    async with aiosqlite.connect("app.db") as db:
        cursor = await db.execute("SELECT * FROM readings")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
```

---

## when to use what

| Need | Package |
|---|---|
| Local/embedded db inside asyncio app | `aiosqlite` |
| Local/embedded db, sync code | `sqlite3` (stdlib) |
| Real server with concurrent writers | `psycopg` / `pymysql` |

Next door: use this for a small asyncio job queue or cache backing a
`fastapi` service.
