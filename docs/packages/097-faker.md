# Faker — realistic test data

> Faker generates deterministic-looking names, addresses, dates, and other data for tests and development fixtures.

## Install and use

```bash
python -m pip install faker
```

```python
from faker import Faker

fake = Faker()
print(fake.name())
print(fake.email())
```

## Reproducible data

```python
from faker import Faker

fake = Faker()
Faker.seed(1234)
print(fake.uuid4())
```

Seeds make tests repeatable, but generated data is not a security primitive and is not guaranteed to represent every real-world edge case. Never send fake-looking data to a production system by accident.

## Practical workflow

Faker is most useful when its output is part of a repeatable project workflow rather than a one-off local command. Start with the smallest command below, then put the same check into the project task runner or continuous-integration job.

```bash
python -m pip install faker
```

For a team workflow, run the check on the same paths and Python versions used by the project. Keep configuration in version control, document intentional exclusions, and make failures actionable by printing the file and rule that needs attention.

## Intermediate usage

Use the tool as a boundary between local work and shared automation. Run the check on changed files during development, then run the complete project check in CI. A useful pattern is to keep fast feedback separate from the slower release job:

```bash
pytest -q
```

If the command changes files, use a two-step process: first show the diff, then apply it after review. This keeps automated cleanup from hiding an accidental behavior change.

## Advanced considerations

For larger repositories, define ownership and failure policy explicitly. Decide which directories are source, tests, generated output, examples, or vendored code. Pin the tool version, record the configuration location, and export machine-readable results when a dashboard or pull-request check consumes them.

When the tool runs in a deployment pipeline, distinguish advisory findings from release-blocking findings. A staged rollout is safer than changing every repository at once, especially when the tool can rewrite files or affect packaging metadata.

## Testing and troubleshooting

A reliable test should cover one successful case, one invalid or boundary case, and one failure path. Re-run the command with verbose output when a local result differs from CI. Check the active virtual environment, installed version, configuration discovery path, and ignored-file rules before changing source code.

## Safety notes

Use a fixed seed when a test needs reproducibility, but do not mistake synthetic data for privacy protection when values resemble real identities.

Do not commit generated credentials, private endpoints, production identifiers, or unreviewed automatic rewrites. Treat CI output as potentially visible to other users and redact sensitive values before uploading logs.

## References

[Faker documentation](https://faker.readthedocs.io/)

Next door: [pytest](095-pytest.md).

