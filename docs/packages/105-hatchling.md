# Hatchling — modern build backend

> Hatchling builds Python wheels and source distributions from PEP 621 metadata in `pyproject.toml`.

## Minimal project metadata

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "example-package"
version = "0.1.0"
description = "An example package"
requires-python = ">=3.11"
```

Build with `python -m build`. Use a unique distribution name, include a license and README, and test the wheel in a clean environment. Do not place credentials or local absolute paths in package metadata.

## Release checklist

Run the test suite, inspect `dist/`, run `python -m twine check dist/*`, and publish to TestPyPI before the real index. Version changes should be reviewed because released versions cannot be replaced safely.

## Practical workflow

Hatchling is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m build --wheel --sdist
```

For a team workflow, run the check on the same paths and Python versions used by the project. Keep configuration in version control, document intentional exclusions, and make failures actionable by printing the file and rule that needs attention.

## Intermediate usage

Use the tool as a boundary between local work and shared automation. Run the check on changed files during development, then run the complete project check in CI. A useful pattern is to keep fast feedback separate from the slower release job:

```bash
python -m twine check dist/*
```

If the command changes files, use a two-step process: first show the diff, then apply it after review. This keeps automated cleanup from hiding an accidental behavior change.

## Advanced considerations

For larger repositories, define ownership and failure policy explicitly. Decide which directories are source, tests, generated output, examples, or vendored code. Pin the tool version, record the configuration location, and export machine-readable results when a dashboard or pull-request check consumes them.

When the tool runs in a deployment pipeline, distinguish advisory findings from release-blocking findings. A staged rollout is safer than changing every repository at once, especially when the tool can rewrite files or affect packaging metadata.

## Testing and troubleshooting

A reliable test should cover one successful case, one invalid or boundary case, and one failure path. Re-run the command with verbose output when a local result differs from CI. Check the active virtual environment, installed version, configuration discovery path, and ignored-file rules before changing source code.

## Safety notes

Inspect the built archive before publishing. Test installation from the wheel in a clean virtual environment and publish to a staging index first.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[Hatchling documentation](https://hatch.pypa.io/latest/)

Next door: [build](104-build.md).

