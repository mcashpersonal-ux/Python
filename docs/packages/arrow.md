# Arrow — human-friendly datetimes

> Arrow wraps standard datetime operations with a concise API for parsing, formatting, and timezone conversion.

## Install and use

```bash
python -m pip install arrow
```

```python
import arrow

instant = arrow.get("2026-09-08T02:30:00+06:00")
print(instant.to("UTC").format("YYYY-MM-DD HH:mm:ss ZZ"))
```

Use named timezone identifiers where possible. Keep timezone-aware values at integration boundaries and avoid silently treating naive timestamps as UTC.

## Relative output

```python
past = arrow.get(2026, 1, 1, tzinfo="UTC")
print(past.humanize(arrow.utcnow()))
```

Choose one datetime library per project boundary to reduce conversion surprises; all libraries still rely on a clear timezone and serialization policy.

Next door: [Pendulum](pendulum.md) and [python-dateutil](dateutil.md).
