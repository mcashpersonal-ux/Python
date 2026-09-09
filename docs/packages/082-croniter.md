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

## Practical workflow

croniter is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m pip install croniter
```

For a team workflow, run the check on the same paths and Python versions used by the project. Keep configuration in version control, document intentional exclusions, and make failures actionable by printing the file and rule that needs attention.

## Intermediate usage

Use the tool as a boundary between local work and shared automation. Run the check on changed files during development, then run the complete project check in CI. A useful pattern is to keep fast feedback separate from the slower release job:

```bash
python -m pytest -q
```

If the command changes files, use a two-step process: first show the diff, then apply it after review. This keeps automated cleanup from hiding an accidental behavior change.

## Advanced considerations

For larger repositories, define ownership and failure policy explicitly. Decide which directories are source, tests, generated output, examples, or vendored code. Pin the tool version, record the configuration location, and export machine-readable results when a dashboard or pull-request check consumes them.

When the tool runs in a deployment pipeline, distinguish advisory findings from release-blocking findings. A staged rollout is safer than changing every repository at once, especially when the tool can rewrite files or affect packaging metadata.

## Testing and troubleshooting

A reliable test should cover one successful case, one invalid or boundary case, and one failure path. Re-run the command with verbose output when a local result differs from CI. Check the active virtual environment, installed version, configuration discovery path, and ignored-file rules before changing source code.

## Safety notes

Define the timezone explicitly and test daylight-saving transitions. croniter computes times; it does not provide locking, retries, persistence, or a durable worker.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[croniter documentation](https://github.com/pallets-eco/croniter)

Next door: [schedule](081-schedule.md) for a small in-process loop.

