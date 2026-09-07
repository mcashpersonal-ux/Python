# Click — composable CLIs

> Click builds readable command-line interfaces from Python functions. It handles parsing, help text, validation, and nested commands.

## Install

```bash
python -m pip install click
```

## A command with options

```python
import click

@click.command()
@click.option("--count", default=1, show_default=True, type=click.IntRange(min=1))
@click.option("--name", prompt="Your name")
def hello(count: int, name: str) -> None:
    """Print a greeting COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    hello()
```

Run it with `python hello.py --count 2 --name Ada`. The function docstring becomes help text; `python hello.py --help` displays the generated interface.

## Groups and errors

```python
import click

@click.group()
def cli() -> None:
    """Manage readings."""

@cli.command()
@click.argument("sensor")
def show(sensor: str) -> None:
    if sensor not in {"line1", "line2"}:
        raise click.ClickException(f"unknown sensor: {sensor}")
    click.echo(f"Reading for {sensor}: 23.4")

if __name__ == "__main__":
    cli()
```

Use `ClickException` for user-facing failures. Do not print stack traces for ordinary input errors, and avoid putting secrets in command-line arguments because shell history and process listings may expose them.

## When to use what

| Need | Package |
|---|---|
| Decorator-based CLI | `click` |
| Type-hint-driven CLI | `typer` |
| Minimal argument parsing | `argparse` in the standard library |

Next door: [Typer](typer.md) for type-hint-driven commands.
