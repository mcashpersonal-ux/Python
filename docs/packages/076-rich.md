# Rich — readable terminal output

> Rich provides styled text, tables, tracebacks, progress displays, and logging for terminal applications.

## Install and print

```bash
python -m pip install rich
```

```python
from rich import print

print("[bold green]OK[/bold green] connected")
```

## Tables

```python
from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Readings")
table.add_column("Sensor")
table.add_column("Value", justify="right")
table.add_row("line1", "23.4")
console.print(table)
```

Use Rich for human-facing output. Keep a plain-text or JSON mode for automation, and avoid logging credentials or unrestricted exception details to shared terminals.

## Practical workflow

Rich is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m pip install rich
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

Use human-facing formatting only for interactive terminals. Keep JSON or plain-text output stable for scripts and avoid printing secrets in styled tracebacks.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[Rich documentation](https://rich.readthedocs.io/)

Next door: [structlog](077-structlog.md) for structured application logs.

