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

Next door: [structlog](structlog.md) for structured application logs.
