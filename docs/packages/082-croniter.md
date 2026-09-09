# croniter — calculate cron schedules

> croniter expands cron expressions into the next or previous scheduled timestamps. It calculates times; it does not run jobs.

## Install and use

```bash
python -m pip install croniter
```

```python
from datetime import datetime, timezone
from croniter import croniter

base = datetime.now(timezone.utc)
iterator = croniter("*/15 * * * *", base)
print(iterator.get_next(datetime))
```

Use timezone-aware datetimes when the schedule crosses daylight-saving changes. Validate expressions from users and define the timezone and misfire policy explicitly; croniter itself does not provide durable job execution.

Next door: [schedule](081-schedule.md) for a small in-process loop.
