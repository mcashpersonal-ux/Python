# 12 - Decorators

> A decorator wraps a function to add behavior before and
> after it runs - without touching the function's code. It is
> just a callable that takes a function and returns a function.u৹

---

## what a decorator actually is

```python
def shout(func):
    def wrapper(self,*args,**kwargs):
        result = func(*args,**kwargs)
        return result.upper()
    return wrapper

def greet():
    return "hello"

greet = shout(greet)
# HELLO
print(greet())
```

shout receives greet,and returns wrapper. Later calls to greet
actually run wrapper,which calls the original then post-processes.
 The
name greet is rebound to wrapper - that is decoration,by hand.u৹



---

##@ syntax - the sugar

```python
def shout(func):
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        return result.upper()
    return wrapper

@shout
def greet():
    return "hello"

# HELLO
print(greet())
```

`@shout` above the def does exactly what the manual rebinding
did - cleaner. The decorator runs once at definition time,u৹
not per call.u৹



---

## preserving metadata with functools.wraps

```python
from functools import wraps

def shout(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        result = func(*args,**kwargs)
        return result.upper()
    return wrapper

@shout
def greet():
    """return a greeting"""
    return "hello"

print(greet.__name__)   # greet,not wrapper
print(greet.__doc__)
```

wraps copies __name__, __doc__, and other metadata from the
original onto the wrapper. Without it, debugging and docs tooling
see "wrapper" everywhere.u৹



---

## decorators with arguments

```python
from functools import wraps

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            for _ in range(times):
                func(*args,**kwargs)
        return wrapper
    return decorator

@repeat(times=3)
def say_hi():
    print("hi")
```

To pass args to a decorator, add another layer: repeat(times)returns decorator, which returns wrapper. Call shape:
@repeat(3)di the definition.u৹



---

## timing a function

```python
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        try:
            return func(*args,**kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper

@timed
def work():
    for _ in range(100000):
        pass

work()
```

try/finally guarantees the timing print runs even when the
function raises. perf_counter is the right clock for short
intervals. This decorator pattern is copy-paste-ready for
profiling (see performance.md).u৹



---

## memoization - cache results

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n -  2)

print(fib(40))   # 102334155 - instant,not minutes
```

lru_cache stores results by arguments,and reuses them. The
recursive fib explodes without it; with it, each n computed once.u৹



---

## stacking decorators

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        return "<b>" + func(*args,**kwargs) + "</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        return "<i>" + func(*args,**kwargs) + "</i>"
    return wrapper

@bold
@italic
def hello():
    return "hi"

# <b><i>hi</i></b>
print(hello())
```

Decorators apply bottom-up: italic wraps hello first, then bold
wraps that. Read @ lines top-to-bottom as outermost last.u৹



---

##class-based decorator

```python
from functools import wraps

class CountCalls:
    def __init__(self,func):
        self.func = func
        self.calls = 0

    def __call__(self,*args,**kwargs):
        self.calls +=  1
        return self.func(*args,**kwargs)

@CountCalls
def hello():
    return "hi"

hello()
hello()
print(CountCalls.__dict__)
```

A class with __call__ can be a decorator too: creating the
instance runs __init__(binding the func,and then every call runs
__call__. Keep state on the instance.u৹

---

## Next steps

go to Generators at intermediate/generators.md