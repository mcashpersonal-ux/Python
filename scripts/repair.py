#!/usr/bin/env python3
"""Repair layer: undo channel corruption introduced into markdown files.
Handles ghost variation-selector bytes, doubled commas, dropped spaces in
'for X in' patterns, and unclosed parens at line ends inside code blocks.
"""
import pathlib
import re

GHOSTS = ("\uf8cf", "\ufe0f")

def strip_ghosts(t):
    for g in GHOSTS:
        t = t.replace(g, "")
    return t

def fix_code_line(line):
    line = line.replace(",,",",")
    line = line.replace(" ,",",")
    line = line.replace(", ",",")
    line = re.sub(r"\bfor\s+(\w+)in\b", r"for \1 in",line)
    if ("(" in line and line.count("(") > line.count(")")) and not line.lstrip().startswith("#"):
        line = line + ")"
    return line

def fix_file(p):
    orig = p.read_text(encoding="utf-8")
    t = strip_ghosts(orig)
    lines = t.splitlines()
    out = []
    in_code = False
    for raw in lines:
        s = raw.strip()
        if s.startswith("```"):
            in_code = not in_code
            out.append(raw)
            continue
        if in_code:
            raw = fix_code_line(raw)
        out.append(raw)
    t = "\n".join(out)
    if t != orig:
        p.write_text(t, encoding="utf-8")
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