# Python Tutorial Hub

A personal Python tutorial website covering **basic → advanced** topics,
with practical, copy-paste-ready snippets and short explanations. Built with
[MkDocs](https://www.mkdocs.org/)+ [Material theme](https://squidfunk.github.io/mkdocs-material/).

## Local development

```bash
python -m pip install -r requirements.txt
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
├── 000-index.md          # Homepage
├── 001-cheatsheet.md     # Quick-reference snippets
├── basics/               # Core lessons continue the global sequence
├── intermediate/
├── advanced/
└── packages/             # Package guides continue the global sequence
```

Every Markdown filename starts with a unique three-digit sequence number, so
file listings sort in the same order as the navigation. Use the navigation
entry rather than guessing a filename when linking to a page.

## Adding a page

1. Create `docs/<section>/<NNN>-<name>.md` with the next available number.
2. Add it under `nav:` in `mkdocs.yml`
3. `mkdocs serve` to preview
