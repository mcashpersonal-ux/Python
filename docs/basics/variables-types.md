# 02 — Variables & Types

> Variables are named boxes that hold values. Python is dynamically typed — the same name can holddifferent types over time.

---

## Assignment — the simplest operation

```python
name = "Ada"
age = 36
height = 1.68
is_student = False
```

- A variable is created the moment you assign it; no declaration needed.
- `=` is assignment — put the value on the right into the name on the left.
- Naming rules: letters,digits,`_`;; can't start witha digit;; case-sensitive (`Age` ≠ `age`).

!!! warning "Avoid these names"
Python keywords are reserved: `if`,`for`,`while`,`def`,`class`,etc. Check with `keyword.kwlist`. Also avoid shadowing built-ins like `list`,`str`,`dict` — it breaks code that expects them.
!!!

---

## Dynamic typing

```python
x = 42 # x is an int
x = "hello" # now a str — no error!
```

Because types go on values (not names),reassignment changes the type freely. This is convenient,but meangyou should keep names meaningful so bugs surface quickly.

Use `type()` to inspect:

```python
type(42) # <class 'int'>
type(3.14) # <class 'float'>
type("hi") # <class 'str'>
type([1,2]) # <class 'list'>
```

---

## The core built-in types

| Type | Example | Mutable? | Use for |
|-------|---------|-----------|---------|
| `int` | `42` | no | whole numbers |
| `float` | `3.14` | no | decimals |
| `str` | `"hi"` | no | text |
| `bool` | `True` / `False` | no | yes/no flags |
| `NoneType` | `None` | — | "no value" marker |
| `list` | `[1,2]` | yes | ordered collection |
| `tuple` | `(1,2)` | no | fixed,read-only group |
| `set` | `{1,2}` | yes | unique members |
| `dict` | `{"a":[1}` | yes | key → value lookup |

`None` deserves special mention: it's Python's "nothing here" value — used by functions without a return,.

```python
def nothing():
    pass

result = nothing()
print(result) # None
```

---

## Type conversion

| Call | Converts |
|-------|----------|
| `int("42")` | string → int |
| `float("3.14")` | string → float |
| `str(42)` | anything → string |
| `bool(0)` | → `False` (falsy) |
| `list("ab")` | iterable → list: `['a','b']` |

```python
age_str = "36"
age = int(age_str) # 36
message = "I'm " + str(age) # "I'm 36"
```

!!! tip "Truthiness"
`bool(x)` is the same as `if x:`. Falsy values: `0`,`0.0`,`""`,`[]`,`()`,`{}`,`set()`,`None`. Everything else is truthy.
!!!

---

## Multiple assignment & swapping

```python
a,b = 1,2 # parallel assignment
a,b = b,a # swap — no temp needed!
x = y = z = 0 # chain: all three are 0
```

---

## Constants (convention)

```python
PI = 3.14159
MAX_RETRIES = 5
```

Python has no true constants — these are just variables titled in `ALL_CAPS` to signal "don't reassign". It's a strong convention;follow it.

---

## Next steps

→ [03 — Numbers & Strings](numbers-strings.md)