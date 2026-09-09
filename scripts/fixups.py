#!/usr/bin/env python3
"""Apply one-off, targeted literal find/replace fixes.

Use this for corruption or typos that are specific to one exact string
in one file, where a general-purpose repair rule (see repair.py,
normalize.py) would be overkill or too risky to apply everywhere.

Historically this file only *declared* `pairs` without ever applying
them - `python scripts/fixups.py` did nothing. It now actually performs
the replacements and reports what changed. Entries whose "before" string
is no longer present (e.g. already fixed by an earlier repair pass) are
reported as already clean, not silently skipped.
"""
import pathlib

pairs = {
    "docs/basics/005-collections.md": [
        ("b = {2,  \uf8cf3,  \uf8cf4}", "b = {2, 3, 4}"),
        ("original = [[1,  2], [3,   \uf8cf4]]", "original = [[1, 2], [3, 4]]"),
    ],
}


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    applied = 0
    already_clean = 0
    missing_files = 0
    for rel_path, replacements in pairs.items():
        path = root / rel_path
        if not path.exists():
            print(f"MISSING FILE: {rel_path}")
            missing_files += 1
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for before, after in replacements:
            if before in text:
                text = text.replace(before, after)
                applied += 1
                print(f"fixed in {rel_path}: {before!r} -> {after!r}")
            else:
                already_clean += 1
        if text != original:
            path.write_text(text, encoding="utf-8")
    print(f"applied={applied} already_clean={already_clean} missing_files={missing_files}")


if __name__ == "__main__":
    main()
