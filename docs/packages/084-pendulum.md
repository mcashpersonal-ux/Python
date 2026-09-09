# Pendulum — timezone-aware datetimes

> Pendulum provides a higher-level datetime API with explicit timezone handling and human-friendly durations.

## Install and use

```bash
python -m pip install pendulum
```

```python
import pendulum

now = pendulum.now("UTC")
later = now.add(hours=2)
print(later.diff_for_humans(now))
```

Name timezones such as `America/New_York` instead of using fixed offsets when civil-time behavior matters. Convert to UTC at system boundaries when storing or exchanging instants.

## Parsing

```python
value = pendulum.parse("2026-09-08T02:30:00+06:00")
print(value.in_timezone("UTC"))
```

Validate external timestamps and preserve whether an input represented a date, local time, or absolute instant.

Next door: [python-dateutil](083-dateutil.md).
