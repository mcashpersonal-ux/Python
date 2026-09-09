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
ANY_FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
NAV_TARGET_RE = re.compile(r":\s+(?P<target>[^\s#]+\.md)\s*$", re.M)
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((?P<target>[^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
COMMA_SPACING_RE = re.compile(r",(?=[A-Za-z])")
PACKAGE_HUB_ROW_RE = re.compile(r"\| ([^|]+) \| `([^`]+)` \|")
PACKAGE_ALIASES = {"pymodbus": "modbus-pymodbus", "python-dateutil": "dateutil"}


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


def validate_prose_comma_spacing() -> list[str]:
    """Regression guard for the 'meangyou'-style corruption fixed in the past:
    a comma immediately followed by a letter, outside of fenced code blocks
    and inline code spans (where such a pattern can be legitimate example
    data, e.g. "cat,dog,cat,bird")."""
    errors: list[str] = []
    for path in sorted(DOCS.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        prose = ANY_FENCE_RE.sub("", text)
        prose = INLINE_CODE_RE.sub("", prose)
        for match in COMMA_SPACING_RE.finditer(prose):
            snippet = prose[max(0, match.start() - 20):match.start() + 20]
            errors.append(f"{path.relative_to(ROOT)}: missing space after comma near {snippet!r}")
    return errors


def validate_package_hub_coverage() -> list[str]:
    """Every package listed in the packages hub table should have a
    corresponding tutorial page in docs/packages/, and vice versa is not
    required (a page may cover more than the hub summarizes)."""
    package_dir = DOCS / "packages"
    hub_candidates = sorted(package_dir.glob("[0-9][0-9][0-9]-index.md"))
    if not hub_candidates:
        return ["docs/packages/*-index.md hub page is missing"]
    hub = hub_candidates[0]
    existing = {re.sub(r"^\d{3}-", "", p.stem) for p in package_dir.glob("*.md")}
    errors: list[str] = []
    for label, package in PACKAGE_HUB_ROW_RE.findall(hub.read_text(encoding="utf-8")):
        slug = PACKAGE_ALIASES.get(package, package.lower().replace("_", "-"))
        if slug not in existing:
            errors.append(f"hub lists '{label.strip()}' (`{package}`) with no matching docs/packages/*-{slug}.md page")
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

    errors = (
        validate_python_examples()
        + validate_navigation()
        + validate_internal_links()
        + validate_prose_comma_spacing()
        + validate_package_hub_coverage()
    )
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
