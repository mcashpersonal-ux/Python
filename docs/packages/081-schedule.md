# schedule — simple in-process jobs

> `schedule` provides a readable API for recurring jobs inside a long-running Python process.

## Install and run

```bash
python -m pip install schedule
```

```python
import schedule
import time

def poll() -> None:
    print("polling")

schedule.every(10).minutes.do(poll)
while True:
    schedule.run_pending()
    time.sleep(1)
```

The loop is in-process and does not survive a process restart. Jobs run serially by default, and a slow job delays later jobs. Add locking or an external queue when overlapping work is unsafe.

## Cancellation

```python
job = schedule.every().hour.do(poll)
schedule.cancel_job(job)
```

For durable production scheduling, consider the operating system scheduler, a workflow system, or a task queue with persistence and retry semantics.

Next door: [croniter](082-croniter.md) for calculating cron occurrences.
