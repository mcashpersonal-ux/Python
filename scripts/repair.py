#!/usr/bin/env python3
"""Repair layer: undo channel corruption introduced into markdown files.

Handles ghost variation-selector bytes, doubled commas, dropped spaces in
'for X in' patterns, and missing spaces after commas.

The comma-spacing fix is fence- and token-aware:
- Inside python-tagged fences, it uses `tokenize` so only genuine comma
  *operators* get a trailing space - commas embedded in string literals
  (e.g. "cat,dog,cat,bird" used as example CSV data) are left untouched,
  since tokenize treats string contents as a single STRING token.
- Inside other fences (bash, text, plain output) and in prose, a plain
  regex is used, since those blocks are illustrative text rather than
  code whose literal values matter.

Safe to re-run at any time; it is a no-op on already-clean files.
"""
import io
import pathlib
import re
import tokenize

GHOSTS = ("\uf8cf", "\ufe0f")
FENCE_RE = re.compile(r"^```([\w+-]*)\s*$")


def strip_ghosts(t):
    for g in GHOSTS:
        t = t.replace(g, "")
    return t


def fix_for_in(line):
    return re.sub(r"\bfor\s+(\w+)in\b", r"for \1 in", line)


def fix_plain_text(text: str) -> str:
    text = re.sub(r",(?=[A-Za-z])", ", ", text)
    return fix_for_in(text)


def fix_python_code(code: str) -> str:
    """Insert a space after comma OP tokens when missing, without ever
    touching characters inside string/comment tokens."""
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
    except Exception:
        return fix_for_in(code)

    lines = code.splitlines(keepends=True)
    inserts = []
    for tok in tokens:
        if tok.type == tokenize.OP and tok.string == ",":
            row, col = tok.end
            line = lines[row - 1] if row - 1 < len(lines) else ""
            nextchar = line[col:col + 1]
            if nextchar and nextchar not in (" ", "\t", "\n", ")", "]", "}", ","):
                inserts.append((row, col))
    for row, col in sorted(inserts, key=lambda x: (x[0], x[1]), reverse=True):
        line = lines[row - 1]
        lines[row - 1] = line[:col] + " " + line[col:]
    return fix_for_in("".join(lines))


def fix_file(p: pathlib.Path) -> bool:
    orig = p.read_text(encoding="utf-8")
    text = strip_ghosts(orig)
    lines = text.split("\n")

    out = []
    prose_buf = []
    i = 0

    def flush_prose():
        out.extend(fix_plain_text("\n".join(prose_buf)).split("\n"))
        prose_buf.clear()

    while i < len(lines):
        line = lines[i]
        m = FENCE_RE.match(line.strip()) if line.strip().startswith("```") else None
        if m is not None:
            flush_prose()
            lang = m.group(1).lower()
            out.append(line)
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            code_text = "\n".join(code_lines)
            new_code = fix_python_code(code_text) if lang in ("python", "py", "python3") else fix_plain_text(code_text)
            out.extend(new_code.split("\n"))
            if i < len(lines):
                out.append(lines[i])
                i += 1
            continue
        prose_buf.append(line)
        i += 1
    flush_prose()

    new_text = "\n".join(out)
    if new_text != orig:
        p.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    fs = sorted(pathlib.Path("docs").rglob("*.md"))
    changed = [f for f in fs if fix_file(f)]
    print("repaired:", len(changed))
    for f in changed:
        print(" -", f)


if __name__ == "__main__":
    main()
