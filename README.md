# Python Tutorial Hub

A personal Python tutorial website covering **basic → advanced** topics,
with practical, copy-paste-ready snippets and short explanations. Built with
[MkDocs](https://www.mkdocs.org/)+ [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Local development

```bash
pip install -r requirements.txt
mkdocs serve        # preview at http://127.0.0.1:8000
```

## Build

```bash
mkdocs build
```

Static output goes into `site/` — deploy that folder to GitHub Pages
(`mkdocs gh-deploy`) or any static host.

## Structure

```
docs/
├── index.md              # Homepage
├── cheatsheet.md         # Quick-reference snippets
├── basics/               # 01 – 10
├── intermediate/         # 11 – 18
└── advanced/             # 19 – 25
```

## Adding a page

1. Create `docs/<section>/<name>.md`
2. Add it under `nav:` in `mkdocs.yml`
3. `mkdocs serve` to preview