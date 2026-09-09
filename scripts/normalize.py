#!/usr/bin/env python3
"""Normalize whitespace/punctuation artifacts in the docs.

This used to contain a couple of bugs that made it actively harmful:
- `t.replace(", ", " ,")` moved commas *before* the preceding space
  instead of collapsing " ," into ",", i.e. it did the opposite of
  what its neighbouring line intended.
- `t.replace(".", ".")` was a no-op (replacing "." with itself).

Both are fixed below. This script only touches whitespace/formatting;
it never rewrites words, so it's safe to run at any time.
"""
import pathlib
import re

GHOSTS = ("\uf8cf", "\ufe0f")


def norm(t: str) -> str:
    for g in GHOSTS:
        t = t.replace(g, "")
    t = t.replace(",,", ",")       # collapse doubled commas
    t = t.replace(" ,", ",")       # no space before a comma
    # NOTE: deliberately no "add space after comma" rule here - this
    # function is not fence-aware, and blindly adding spaces after every
    # comma would corrupt comma-separated string literals used as example
    # data (e.g. "cat,dog,cat,bird"). That fix lives in repair.py instead,
    # which is fence- and token-aware.
    t = re.sub(r"[ \t]+\n", "\n", t)       # trim trailing whitespace per line
    t = re.sub(r"\(\s*\)", "()", t)        # tidy stray whitespace in empty parens
    return t


def main():
    fs = sorted(pathlib.Path("docs").rglob("*.md"))
    total = 0
    for f in fs:
        t = f.read_text(encoding="utf-8")
        c = norm(t)
        if c != t:
            f.write_text(c, encoding="utf-8")
            total += 1
            print("fixed", f)
    print("files fixed:", total)


if __name__ == "__main__":
    main()
