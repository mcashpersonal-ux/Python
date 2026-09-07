# 23 — Type Hints

> Type hints document intent and let tools catch bugs before runtime.
> They are optional- python stays dynamic- but enables mypy/IDE checks.

---

##basic annotations

```python
def greet(name: str, count: int) -> str:
    return f"Hello {name}" * count

total: int = 0
names: list[str] = ["a", "b"]
```

Annotate each arg and return type after colons. Builtins
are subscriptable since 3.9: list[str], dict[str, int]. Hints don't
enforce at runtime- tools do.u

---

##typing module

```python
from typing import Optional, Union, List, Dict

def find(xs: List[int], key: int) -> Optional[int]:
    for v in xs:
        if v == key:
            return v
    return None

def load(path: str) -> Union[str, bytes]:
    with open(path, "rb") as f:
        return f.read()
```

Optional[int] means int or None- shorthand for Union[int, None].
Union lists alternatives; modern code can write int | None instead.

Use Optional for maybe-values, Union for multi-types.u

---

##TypeVar- generic functions

```python
from typing import TypeVar, Sequence

T = TypeVar("T")

def first(xs: Sequence[T]) -> T:
    return xs[0]

nums: list[int] = [1, 2]
s: list[str] = ["a", "b"]
print(first(nums))
print(first(s))
```

TypeVar links input and output types- first takes list[int]
and returns int, list[str] returns str. Callers keep type
safety across containers without repetition.u

---

##Protocol- structural typing

```python
from typing import Protocol

class Sized(Protocol):
    def __len__(self) -> int: ...

def show_size(obj: Sized) -> None:
    print(len(obj))

show_size([1, 2])
show_size("hello")
```

Protocol matches any type with the required members- no need
to inherit. show_size accepts list and str because both define
__len__. Structural typing keeps functions open to new types.u

---

##dataclass hints

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
```

Fields are annotations without defaults; dataclass generates
__init__, repr, eq. Mypy can catch wrong-typed args at
analysis time. Dataclasses pair naturally with hints- no manual
init boilerplate.u

---

##Literal- exact values

```python
from typing import Literal

def set_mode(mode: Literal["fast", "safe"]) -> None:
    print(mode)

set_mode("fast")
set_mode("safe")
# set_mode("slow")  # type checker error
```

Literal pins args to a fixed set- catches typos likem "sloe"
before runtime. Great for modes, directions, and option
strings. Combine with Final for constants.u

---

##mypy- run the checker

```bash
pip install mypy
mypy my_program.py
```

mypy reads hints and reports mismatches without running
code. Start lenient (--ignore-missing-imports) thene tighten.
CI can run mypy so regressions surface at merge time, not
runtime.u

---

##Next steps

go to Design Patterns at advanced/design-patterns.md