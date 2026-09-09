# PyYAML — YAML configuration

> PyYAML parses YAML documents into Python values and can serialize supported values back to YAML.

## Install and load safely

```bash
python -m pip install pyyaml
```

```python
from pathlib import Path
import yaml

config = yaml.safe_load(Path("config.yml").read_text(encoding="utf-8"))
print(config.get("environment", "development"))
```

Use `safe_load()` for configuration supplied by users or files. Do not use `yaml.load()` with an unrestricted loader on untrusted content because YAML tags can construct Python objects.

## Write configuration

```python
from pathlib import Path
import yaml

settings = {"environment": "development", "retries": 3}
Path("config.yml").write_text(
    yaml.safe_dump(settings, sort_keys=False), encoding="utf-8"
)
```

Validate required keys after parsing, and keep credentials in environment variables or a secret manager rather than YAML committed to source control.

Next door: [python-dotenv](079-python-dotenv.md) for local environment files.
