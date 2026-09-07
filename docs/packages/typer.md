# Typer — type-hint-driven CLIs

> Typer turns annotated Python functions into command-line interfaces and uses Click underneath.

## Install

```bash
python -m pip install typer
```

## A typed command

```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str, count: int = typer.Option(1, min=1)) -> None:
    """Print a greeting COUNT times."""
    for _ in range(count):
        typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

Run `python app.py Ada --count 2`. Typer derives conversion and help text from annotations and defaults. Test the generated `--help` output as part of the user interface.

## Validation and secrets

Use enums or constrained values for closed choices. Read tokens from environment variables or a secret manager, not from options that appear in shell history. Typer is an interface layer; keep business logic in ordinary functions so it remains easy to test.

## When to use what

| Need | Package |
|---|---|
| Modern typed CLI | `typer` |
| Decorator CLI with explicit Click APIs | `click` |
| No third-party dependency | `argparse` |

Next door: [Click](click.md).
