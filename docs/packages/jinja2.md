# Jinja2 — template rendering

> Jinja2 renders text or HTML from templates and explicitly separates presentation from Python application logic.

## Install and render

```bash
python -m pip install jinja2
```

```python
from jinja2 import Environment, StrictUndefined

env = Environment(undefined=StrictUndefined, autoescape=True)
template = env.from_string("Hello, {{ name }}!")
print(template.render(name="Ada"))
```

Use an application integration's configured autoescaping for HTML. Never render untrusted text as a template source, and do not mark untrusted HTML as safe without sanitizing it.

## File templates

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
html = env.get_template("report.html").render(title="Daily report")
```

Restrict template loaders to intended directories and keep business rules out of templates.

Next door: [Flask](flask.md) and [Django](django.md).
