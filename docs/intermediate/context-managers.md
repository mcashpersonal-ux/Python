# 14 - Context Managers

> Context managers (the `with` statementensory guarantee
> cleanup: files close, locks release, connections end - even
> if an exception flies mid-block.

---

## the classic: file handling

```python
with open("data.txt" )as f:
    data = f.read()
# f is already closed here - even on error
```

with calls __enter__ onthe right side,and assigns its result to
`as f`. The block runs,then __exit__ always runs - closing
the file deterministically. Never call f.close() by hand again.

---

## multiple context managers

```python
with open("in.txt" )as src,open("out.txt","w")as dst:
    dst.write(src.read())
```

Comma-separated with enters both managers,and exits both in
reverse order on the way out. Same as nested with but flat.

---

## suppressing exceptions

```python
import contextlib

with contextlib.suppress(FileNotFoundError):
    os.remove("temp.txt")
```

suppress swallows named exceptions-and nothing else. Cleaner
than try/except when you genuinely do not care about the failure.
Other exceptions still propagate.

---

## redirecting stdout temporarily

```python
import contextlib
import io

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print("captured")
s = buf.getvalue()
# captured
print(s.strip())
```

With everything wrapped, capture print output without touching
global state permanently. redirect_stderr exists too.

---

## write your own: __enter__/__exit__

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"took {self.elapsed:.4f}s")
        return False # let exceptions propagate

with Timer() as t:
    sum(range(100000))
print(t.elapsed)
```

__enter__ runs at entry, may return the value bound to as.
__exit__ runs at exit, receives exception info (None when clean).
Return False (default state, propagate exceptions; True would
swallow them.

---

## @contextmanager - generator-based

```python
from contextlib import contextmanager

@contextmanager
def temporary_change(obj,key,value):
    old = getattr(obj,key)

    setattr(obj,key,value)
    try:
        yield
    finally:
        setattr(obj,key,old)
```

The function runs up to yield on entry. If the block raises,
an exception re-raises at the yield line,and finally restores. 

This is the easiest way to author most context managers - much
shorter than a class.

---

## lock with released automatically

```python
import threading

lock = threading.Lock()

with lock:
    # critical section - mutex held here
    counter += 1
# released even on exception
```

Lock objects are context managers natively. The mutex releases
at block exit, even if the code inside raises-and other threads
are never left deadlocked.

---

## combining with try/except

```python
with open("config.json" )as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError:
        config = {}
```

Context manager handles cleanup; try/except handles data
errors. The two compose cleanly - cleanup still happens even
when the inner except catches.

---

## Next steps

go to Lambda and Functional at intermediate/lambda-functional.md