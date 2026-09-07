#!/usr/bin/env python3
"""Validate Python examples, Markdown links, and MkDocs navigation."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"
FENCE_RE = re.compile(r"```(?P<language>python|python3|py)\s*\n(?P<code>.*?)```", re.S | re.I)
NAV_TARGET_RE = re.compile(r":\s+(?P<target>[^\s#]+\.md)\s*$", re.M)
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((?P<target>[^)\s]+)(?:\s+['\"][^)]*['\"])?\)")


def python_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [match.group("code") for match in FENCE_RE.finditer(text)]


def validate_python_examples() -> list[str]:
    errors: list[str] = []
    for path in sorted(DOCS.rglob("*.md")):
        for index, code in enumerate(python_blocks(path), start=1):
            try:
                compile(code, f"{path.relative_to(ROOT)}:example-{index}", "exec")
            except SyntaxError as error:
                location = f"{path.relative_to(ROOT)}:example-{index}"
                errors.append(f"{location}: {error.msg} (line {error.lineno})")
    return errors


def validate_navigation() -> list[str]:
    if not MKDOCS.exists():
        return ["mkdocs.yml is missing"]
    errors: list[str] = []
    for target in NAV_TARGET_RE.findall(MKDOCS.read_text(encoding="utf-8")):
        if not (DOCS / target).is_file():
            errors.append(f"mkdocs.yml references missing page: docs/{target}")
    return errors


def validate_internal_links() -> list[str]:
    errors: list[str] = []
    markdown_files = [ROOT / "README.md", *sorted(DOCS.rglob("*.md"))]
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group("target")
            if target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (source.parent / target_path).resolve()
            if not resolved.is_file():
                errors.append(f"{source.relative_to(ROOT)} links to missing file: {target}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="remove legacy corruption markers")
    args = parser.parse_args(argv)

    if args.fix:
        for path in sorted(DOCS.rglob("*.md")):
            original = path.read_text(encoding="utf-8")
            cleaned = original.replace("\uf8cf", "")
            if cleaned != original:
                path.write_text(cleaned, encoding="utf-8")
                print(f"fixed {path.relative_to(ROOT)}")

    errors = validate_python_examples() + validate_navigation() + validate_internal_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1

    examples = sum(len(python_blocks(path)) for path in DOCS.rglob("*.md"))
    pages = len(list(DOCS.rglob("*.md")))
    print(f"Validation passed: {pages} pages, {examples} Python examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
