# 25 — Best Practices

> Code is read more often than written — optimize for the reader.
> Correctness, clarity, then speed — in that order.

---

## PEP 8 — style basics

```python
# yes - spaced, named, consistent
def total_price(items, tax):
    prices = [i.price for i in items]
    return sum(price * (1 + tax) for price in prices)

# no - cramped, cryptic
def tp(i, t):
    p=[x.price for x in i]
    return sum(p*(1+t))
```

Use 4-space indent, 79-col lines, snake_case names.
Blank
lines separate top-level defs; two blank lines after imports.
Tools
like black make style consistency automatic.

---

## EAFP over LBYL

```python
# EAFP - ask forgiveness
def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None

# LBYL - look before leap
def parse_int2(s):
    if s.isdigit():
        return int(s)
    return None
```

Try the operation then catch — avoids races and double work.
isdigit misses signs/spaces ("-5", " 5"). EAFP is preferred in
Python — it is simpler and more robust for real inputs.

---

## Avoid mutable defaults

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(add_item("a"))
print(add_item("b"))
```

Shared default lists persist across calls - the classic gotcha.

Use a None sentinel, then build fresh state each call. Same rule
applies to dicts, sets, and class-level mutable attrs.

---

## Context managers for resources

```python
with open("out.txt", "w") as f:
    f.write("hello")

with lock:
    counter += 1
```

with guarantees cleanup even when exceptions raise - files close,
locks release. Manual try/finally works but is extra ceremony.
Prefer context managers whenever an object offers one.

---

## Compose small functions

```python
def parse_user(row, parser):
    fields = row.split(",")
    return {k: parser(v) for k, v in fields}

def load_users(path, parser):
    with open(path) as f:
        return [parse_user(line, parser) for line in f]
```

Each function does one thing and stays a few levels deep. parse_user
knows rows; load_users knows files - test each in isolation.

Composition beats copy-paste and god-functions that do everything.

---

## Use the standard library

```python
import json
import csv
import re
import collections

# instead of hand-writing JSON parsing, use json.loads
# instead of tab-splitting CSV, use csv.reader
# instead of regex from scratch, use compiled re patterns
```

stdlib covers json, csv, sqlite3, argparse, dataclasses,
pathlib, itertools, more. Check it before reaching for a new
dependency - fewer deps means fewer supply-chain risks.

---

## Type hints and docstrings

```python
def days_since(epoch, today):
    """Days between two datetime.date values."""
    return (today - epoch).days

def parse_time(text):
    """Parse ISO-8601 and return naive datetime."""
    from datetime import datetime
    return datetime.fromisoformat(text)
```

Docstrings explain what and why - not how. Hints document the
contract; docstrings document intent. Keep both short and
accurate - stale docs mislead worse than none.

---

## Write tests first

```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

Tests make refactors safe and document examples. Write a
failing test before fixing a bug - then watch it pass. Run them
in CI so future edits cannot silently break behavior.

---

## Next steps

You have reached the end of the hub - revisit any section, or
use the cheatsheet for daily snippets. Happy coding!
