# loguru — logging with almost no setup

> loguru replaces the standard library's `logging` module's boilerplate
> (handlers, formatters, loggers) with one pre-configured object and a
> much simpler API — useful for scripts and small services where
> `structlog`-level structure would be overkill.

## Install and log

```bash
python -m pip install loguru
```

```python
from loguru import logger

logger.info("starting job")
logger.warning("queue depth is {}", 42)
logger.error("failed to connect to {host}", host="db1")
```

No `getLogger(__name__)`, no handler setup — `logger` works immediately
with sensible colored console output.

## log to a file with rotation

```python
from loguru import logger

logger.add("app.log", rotation="10 MB", retention="14 days", compression="zip")
logger.info("this goes to both the console and app.log")
```

`rotation` and `retention` handle log-file growth for you — no cron job
or logrotate config needed for a single-process script.

## structured (JSON) output

```python
from loguru import logger

logger.add("events.jsonl", serialize=True)
logger.bind(request_id="abc-123").info("request handled", status=200)
```

`serialize=True` writes one JSON object per line — convenient for
shipping logs to something like Elasticsearch or Loki. `bind()` attaches
context to every subsequent call on that logger instance.

## capturing exceptions

```python
from loguru import logger

@logger.catch
def risky():
    return 1 / 0

risky()  # logs the full traceback instead of crashing
```

`logger.catch` is handy for scripts and background jobs; for
request-handling code, prefer an explicit `try/except` so you control
what the caller sees.

## Safety notes

Never log passwords, tokens, session cookies, or full payment/personal
data — redact or omit sensitive fields before calling `logger.info`.
For a codebase with multiple contributors and libraries that already use
the standard `logging` module, `loguru` can intercept those with a small
adapter — check the docs before assuming it will do so automatically.

Next door: [structlog](077-structlog.md) if you need machine-first
structured logging across a larger service, and [Rich](076-rich.md) for
prettier ad hoc terminal output.
