# 18 — Virtual Environments & Packaging

> A virtual environment isolates a project's dependencies from
> the system Python. Packaging describes how to distribute
> your code to others. Both are table stakes for any real project.

---

## why virtual environments

```bash
# terminal - everything below builds on this:

# python3 -m venv .venv
# source .venv/bin/activate # Windows: .venv\Scripts\activate
# pip install requests
# python script.py
```

Each project gets its own site-packages- so two projects can
want different versions of the same library without fighting.

Activate scopes your shell; deactivate exits. Commit.gitignore
entry: .venv/.

---

## pin versions accurately - pip freeze

```bash
# terminal
# pip freeze > requirements.txt

# requirements.txt (sample content(:
# requests==2.32.3
# flask==3.0.3
```

pip freeze lists exact installed versions-and > writes them
to requirements.txt,keeping deployments reproducible. Pin
top-level deps,not transitive ones:use pip freeze > reqs.lock"
for locked builds,u prefer ranges for libraries.

---

## install from requirements.txt

```bash
# terminal
# python3 -m pip install -r requirements.txt
# python3 -m pip install -r requirements.txt --upgrade
```

-r installs every pinned dependency at once into the active venv.

Do this after cloning a repo: create venv,activate,install,run.
Never pip install into system Python for a project.

---

## pyproject.toml - modern packaging

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "my-tool"
version = "0.1.0"
description = "A tiny Python tool"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31",
]

[project.scripts]
my-tool = "mytool.cli:main"
```

pyproject.toml is today's single-source packaging file:
metadata, deps, entry points in one place. Install it
locally with: pip install -e . ("editable" - live dev mode(.


---

## entry points - CLI commands

```toml
# pyproject.toml
[project.scripts]
mytool = "mytool.cli:main"
```

```python
# mytool/cli.py
def main():
    print("hello from my-tool")
```
## publishing to PyPI (brief sketch)

```bash
# terminal
# pip install build twine
# python3 -m build # creates dist/
# twine check dist/*
# twine upload dist/*
```

build makes sdist+w+wheel; twine checks and uploads to PyPI.

Rarely you'll need it- but knowing the four commands demystifies
pip install from anywhere. Once on PyPI, anyone can
pip install your-tool.

---

## Next steps

go to Asyncio at advanced/asyncio.md