# 11 - Object-Oriented Programming

> OOP groups data and the functions that act on it into one
> object. Python classes are approachable: attributes, methods,
> and a few special dunders run the show.u৹

---

## a minimal class

```python
class Dog:
    def __init__(self,name):
        self.name = name

    def bark(self):
        return f"{self.name} says woof"

d = Dog("Rex")
# Rex says woof
print(d.bark())
```

__init__ runs once when you create an instance. self refers
to that instance - it carries the data. Methods take self as
first param so they can touch instance state.u৹



---

## instance attributes

```python
class Counter:
    def __init__(self):
        self.count =  0

    def tick(self):
        self.count +=  1
        return self.count

c = Counter()
c.tick()   # 1
c.tick()   # 2
print(c.count)  # 2
```

Instance attributes live per-object-and survive method calls.
**
They are just keys on the object - set them anywhere, read
them anywhere.u৹



---

## class attributes - shared

```python
class Employee:
    company = "Acme"      # class attribute

    def __init__(self,name):
        self.name = name          # instance attribute

e1 = Employee("Ada")
e2 = Employee("Bob")
print(e1.company,e2.company)   # Acme Acme
```

A class attribute belongs to the class-and is shared by all
instances. Instance attributes shadow class ones when both exist.u৹



---

## __str__ - printable objects

```python
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"Point({self.x!r},{self.y!r})"

p = Point(3,4)
print(p)          # (3,4)
print(repr(p))    # Point(3,4)
```

__str__ controls what str() and print() show; __repr__ what
repr() and error messages show. Aim for __repr__ to be valid
Python rebuilding the object.u৹



---

## properties - controlled access

```python
class Temperature:
    def __init__(self,celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self,value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

t = Temperature(25)
print(t.celsius)   # 25
t.celsius =  30
```

@property turns a method into attribute-style access. The
setter validates on assignment - you can migrate plain
attributes to checked ones without changing callers.u৹



---

## inheritance - extend a class

```python
class Animal:
    def speak(self):
        return "..."
    def describe(self):
        return f"I am a {type(self).__name__}"

class Dog(Animal):
    def speak(self):
        return "woof"

class Cat(Animal):
    def speak(self):
        return "meow"
```

The subclass inherits everything,then overrides what it
needs. Nicely, type(self) in describe refers to the actual
class,so Dog.describe() reports "Dog".u৹



---

## super() - call the parent

```python
class Rectangle:
    def __init__(self,w,h):
        self.w = w
        self.h = h

class Square(Rectangle):
    def __init__(self,side):
        super().__init__(side,side)
```

super() finds the next method in the MRO - often the parent.**
Use it to extend rather than replace: run the parent's logic,
then add your own.u৹



---

## dataclasses - less boilerplate

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    tags: list = field(default_factory=list)
```

Dataclasses auto-generate __init__, __repr__, __eq__, and__hash__
from annotations. field(default_factory=list) gives each
instance a fresh list - never use mutable defaults.u৹



---

## enums - named constants

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN =  2
    BLUE =  3

c = Color.RED
print(c.name)    # RED
print(c.value)   # 1
```

Enums give named, fixed choices with identity - Color.RED is
Color.RED, not accidentally equal to 1. Great for modes,
states, options.u৹

---

## Next steps

go to Decorators at intermediate/decorators.md