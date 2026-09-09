# Uvicorn — ASGI server

> Uvicorn runs ASGI applications such as FastAPI and Starlette using an event loop and HTTP protocol implementation.

## Install and run

```bash
python -m pip install uvicorn
python -m uvicorn myapp:app --host 127.0.0.1 --port 8000
```

`myapp:app` means the `app` object in `myapp.py`. Use `--reload` only for local development. Bind to `0.0.0.0` only when a trusted reverse proxy or network policy protects the service.

## Configuration

```python
# myapp.py
from fastapi import FastAPI

app = FastAPI()
```

Production deployments should define worker, proxy, TLS, access-log, health-check, and graceful-shutdown policies explicitly. Uvicorn is a server, not an authentication or authorization layer.

## Practical workflow

Uvicorn is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m uvicorn myapp:app --host 127.0.0.1 --port 8000
```

For a team workflow, run the check on the same paths and Python versions used by the project. Keep configuration in version control, document intentional exclusions, and make failures actionable by printing the file and rule that needs attention.

## Intermediate usage

Use the tool as a boundary between local work and shared automation. Run the check on changed files during development, then run the complete project check in CI. A useful pattern is to keep fast feedback separate from the slower release job:

```bash
python -m uvicorn myapp:app --workers 2
```

If the command changes files, use a two-step process: first show the diff, then apply it after review. This keeps automated cleanup from hiding an accidental behavior change.

## Advanced considerations

For larger repositories, define ownership and failure policy explicitly. Decide which directories are source, tests, generated output, examples, or vendored code. Pin the tool version, record the configuration location, and export machine-readable results when a dashboard or pull-request check consumes them.

When the tool runs in a deployment pipeline, distinguish advisory findings from release-blocking findings. A staged rollout is safer than changing every repository at once, especially when the tool can rewrite files or affect packaging metadata.

## Testing and troubleshooting

A reliable test should cover one successful case, one invalid or boundary case, and one failure path. Re-run the command with verbose output when a local result differs from CI. Check the active virtual environment, installed version, configuration discovery path, and ignored-file rules before changing source code.

## Safety notes

Uvicorn is not an authentication, TLS, rate-limit, or process-supervision layer. Put it behind an appropriate proxy and define graceful shutdown and health checks.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[Uvicorn documentation](https://www.uvicorn.org/)

Next door: [FastAPI](086-fastapi.md) and [Starlette](090-starlette.md).

