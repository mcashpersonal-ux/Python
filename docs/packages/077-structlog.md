# structlog — structured logging

> structlog keeps log events as dictionaries while rendering them for developers or machines.

## Install and configure

```bash
python -m pip install structlog
```

```python
import structlog

log = structlog.get_logger()
log.info("reading_received", sensor="line1", value=23.4)
```

The event fields can be rendered as console text during development or JSON for ingestion. Configure processors once at application startup, then pass stable keys rather than assembling log strings manually.

## Context and safety

Bind request or device identifiers with `log.bind(request_id=request_id)`. Never add passwords, bearer tokens, session cookies, or raw personal data to event fields. Use log rotation and retention controls outside the logging library.

Next door: [Rich](076-rich.md) for human-facing terminal output.
