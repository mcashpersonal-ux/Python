# build — standard Python distributions

> The `build` package creates source distributions and wheels through the PEP 517 build interface.

## Install and build

```bash
python -m pip install build
python -m build
```

The command reads `pyproject.toml` and writes artifacts to `dist/`. Inspect the generated wheel contents and test installation in a clean virtual environment before publishing.

## Validate artifacts

```bash
python -m pip install twine
python -m twine check dist/*
```

Uploading is an external, potentially irreversible action. Use TestPyPI first, protect credentials, and confirm the package name and version before publishing.

## Practical workflow

build is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m build
```

For a team workflow, run the check on the same paths and Python versions used by the project. Keep configuration in version control, document intentional exclusions, and make failures actionable by printing the file and rule that needs attention.

## Intermediate usage

Use the tool as a boundary between local work and shared automation. Run the check on changed files during development, then run the complete project check in CI. A useful pattern is to keep fast feedback separate from the slower release job:

```bash
python -m build --sdist --wheel
```

If the command changes files, use a two-step process: first show the diff, then apply it after review. This keeps automated cleanup from hiding an accidental behavior change.

## Advanced considerations

For larger repositories, define ownership and failure policy explicitly. Decide which directories are source, tests, generated output, examples, or vendored code. Pin the tool version, record the configuration location, and export machine-readable results when a dashboard or pull-request check consumes them.

When the tool runs in a deployment pipeline, distinguish advisory findings from release-blocking findings. A staged rollout is safer than changing every repository at once, especially when the tool can rewrite files or affect packaging metadata.

## Testing and troubleshooting

A reliable test should cover one successful case, one invalid or boundary case, and one failure path. Re-run the command with verbose output when a local result differs from CI. Check the active virtual environment, installed version, configuration discovery path, and ignored-file rules before changing source code.

## Safety notes

Build in a clean environment and inspect the archive contents. Never include `.env` files, private keys, credentials, or local machine paths.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[build documentation](https://build.pypa.io/)

Next door: [Hatchling](105-hatchling.md) for a build backend.

