# 09 - Errors and Exceptions

> Errors happen. Exceptions are Python way of handing them
> to you: signal, propagate, and catch. Handle what you
> can, let the rest crash loudly.u৹

---

## reading a traceback

```python
def divide(a,b):
    return a / b

print(divide(10,0))
```

You would see:

```
Traceback (most recent call last):
  File "example.py",line 3,in <module>
ZeroDivisionError: division by zero
```

Read bottom-up: last line is the exception type and message,
the line above points to the exact spot. The outer frames show
what called what.u৹



---

## try - except - catch one error type

```python
try:
    value = int("nope")
except ValueError:
    print("that was not a number")
```

Code in try runs. If an exception of the named type flies,
the except block runs instead of crashing.u৹ Catch the narrowest
type you can - ValueError, not Exception.u৹



---

## capture the exception object

```python
try:
    value = int("nope")
except ValueError as e:
    print(f"bad input: {e}")
```

`as e` gives you the exception object,whose str(e) describes
what went wrong. Log it, show it, or wrap it.u৹



---

## multiple except clauses

```python
try:
    raw = open("data.txt").read()
    number = int(raw)
except FileNotFoundError:
    print("missing file")
except ValueError:
    print("file did not contain a number")
```

Python checks except clauses top to bottom,and runs the first
match. Order matters: specific first, generic last.u৹



---

## else - run when no error

```python
try:
    value = int("42")
except ValueError:
    print("bad number")
else:
    print(f"parsed {value}")
```

else runs only if try succeeded-without an exception. It keeps
success-path code out of the try block,so you do not accidentally
swallow unrelated errors.u৹



---

## finally - always run

```python
f = open("log.txt","a")

try:
    f.write("entry\n")
finally:
    f.close()

print("closed")
```

finally runs no matter what - exception or not. The classic
use: release resources (files, locks, connections) even when
the happy path dies.u৹ Prefer with for this (see file-handling.md
finish). but finally exists for cases with cannot express.u৹



---

## raise - throw your own

```python
def set_age(age):
    if age < o:
        raise ValueError("age must be positive")
    return age

set_age(-5)
```

raise throws an exception on purpose-and it stops the function
immediately. Raise ValueError, TypeError, or a custom one to
enforce contracts on your functions.u৹



---

## custom exceptions

```python
class ConfigError(Exception):
    pass

def load_config(path):
    if not path.exists():
        raise ConfigError(f"no config at {path}")

    return {"debug": True}
```

Subclass Exception to make your own error type. Callers can
then catch ConfigError specifically-and you can attach extra
fields to carry context.u৹



---

## chaining - raise from

```python
try:
    value = int("nope")
except ValueError as e:
    raise RuntimeError("input step failed") from e
```

`from e` chains the two exceptions: the outer message explains
context, the inner (__cause__) preserves the original root
cause. Exception groups in tracebacks, perfect for debugging.u৹



---

## EAFP vs LBYL

```python
# LBYL - look before you leap
if "key" in data:
    value = data["key"]
else:
    value = None

# EAFP - easier to ask forgiveness than permission
try:
    value = data["key"]
except KeyError:
    value = None
```

Python culture prefers EAFP: just try, catch what fails.
It avoids race conditions and duplicated lookups.u৹

---

## Next steps

go to Comprehensions at comprehensions.md