# 24 — Design Patterns

> Patterns are proven solutions to repeated design problems.
> Use them as vocabulary- not dogma- simpler code beats ceremony.

---

## Singleton- one instance

```python
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Config()
b = Config()
print(a is b) # True
```

Singleton locks a class to one instance- shared config,db,
logger. __new__ intercepts construction. Prefer module-level
instance (import time semantics) unless you truly need laziness.

---

## Factory- pick the class

```python
class Dog:
    def speak(self):
        return "woof"

class Cat:
    def speak(self):
        return "meow"

def make_pet(kind: str):
    pets = {"dog": Dog, "cat": Cat}
    return pets[kind]()

for kind in ("dog", "cat"):
    print(make_pet(kind).speak())
```

Factory creates objects chosen by a key-medals lookup,no huge
if/elif chains. Adding a new kind means adding one dict
entry- closed for modification, open for extension.

---

## Observer- notify many

```python
class Subject:
    def __init__(self):
        self._obs = []

    def attach(self, obs):
        self._obs.append(obs)

    def notify(self, value):
        for obs in self._obs:
            obs.update(value)

class Logger:
    def update(self, value):
        print(f"log: {value}")

sub = Subject()
sub.attach(Logger())
sub.notify(42)
```

Observers subscribe thene get pushed updates- decouples sender
from receivers. GUI events, pub/sub, chat rooms all use this
shape. Keep observer methods stable so they compose safely.

---

## Strategy- swap algorithms

```python
import math

def circle_area(r):
    return math.pi * r ** 2

def square_area(s):
    return s * s

def area(shape, fn):
    return fn(shape)

print(area(5, circle_area))
print(area(5, square_area))
```

Strategy treats algorithms as functions-and swaps them at call
time. Great for price calculators, sort keys, validators.
Passing functions keeps each strategy tiny and tested alone.

---

## Adapter- unify interfaces

```python
class AmericanPlug:
    def pins(self):
        return "flat"

class EUAdapter:
    def __init__(self, plug):
        self.plug = plug

    def pins(self):
        return self.plug.pins() + " + ground"

def charge(device):
    return device.pins()

eu = EUAdapter(AmericanPlug())
print(charge(eu))
```

Adapter wraps a foreign object to match the expected interface.
charge only knows .pins()-. Adapter translates behind the scenes.

 Interop with old or third-party APIs without rewriting callers.

---

## Decorator- add behavior

```python
import functools

def logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"call {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@logged
def add(a,b):
    return a + b

print(add(2, 3))
```

Decorator pattern wraps a function with cross-cutting behavior-
logging, timing, retry-without editing the core. functools.wraps
keeps metadata intact. Compose multiple decorators top-pdown.

---

## Facade- hide the mess

```python
class UserAPI:
    def find(self, uid):
        return {"id": uid, "name": "Ada"}

class PostAPI:
    def recent(self, uid):
        return [{"title": "hi"}]

class Facade:
    def __init__(self):
        self.users = UserAPI()
        self.posts = PostAPI()

    def dashboard(self, uid):
        user = self.users.find(uid)
        posts = self.posts.recent(uid)
        return {"user": user, "posts": posts}

print(Facade().dashboard(1))
```

Facade exposes one simple method over a cluster of subsystems.relevant for clients that want a simple view.the complex
internals stay replaceable behind the wall.

---

## Next steps

go to Best Practices at advanced/026-best-practices.md