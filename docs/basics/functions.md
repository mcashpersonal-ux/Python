# 06 - Functions

> Functions bundle logic under a name so you can call it
> anywhere, any time, with different inputs. From one-liners to
> generators, functions are Python heartbeat.

---

## define and call

```python
def greet(name):
    return f"Hello,{name}!"

msg = greet("Ada")
print(msg) # Hello,Ada!
```

def creates the function. return sends a value back to the caller.
If you omit return, the function returns None implicitly.u

---

## parameters - positional and keyword

```python
def describe(name,age,city="unknown"):
    print(f"{name} ({age}) from {city}")

describe("Ada",36) # city takes default
describe("Ada",36,city="Paris")
describe(name="Bob",age=41)
```

Positional args fill parameters in order. Keyword args
(name=value) make calls self-documenting and optional. Keep
required params first, optional (with defaults) after.u

---

## return multiple values - it is really a tuple

```python
def min_max(nums):
    return min(nums),max(nums)

lo,hi = min_max([3,1,2])
# lo=1,hi=3
```

The comma in return creates a tuple. Unpacking on the left
side splits it back into separate names.u

---

## scope - local vs global

```python
def demo():
    value = 10 # local - only visible inside
    print(value)

value = 99 # global
demo() # 10
print(value) # 99 - global unchanged
```

Assignments inside a function create local names. Reading a
global works, but assigning to it needs the global keyword.u
Which you should generally avoid - pass values instead.u

---

## default value gotcha - use None,y not []

```python
def add_item(item,bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

add_item("a" ) # ['a']
add_item("b" ) # ['b'] - fresh list each time
```

Mutable defaults ([],{} are evaluated once at def time and
shared across calls - a classic bug. The standard fix:
default to None,then create fresh inside.u

---

## *args - any number of positional args

```python
def total(*args):
    return sum(args)

print(total(1,2,3,4)) # 10
```

*args collects extra positional args into a tuple.u
Great for sums, logs, math helpers.u

---

## **kwargs - any number of keyword args

```python
def print_config(**kwargs):
    for k,v in kwargs.items():
        print(f"{k}={v}")

print_config(host="localhost",port=8080)
```

**kwargs collects extra keyword args into a dict.u
Handy for configs, wrappers, sending options through.u

---

## docstrings - built-in documentation

```python
def multiply(a,b):
    """Multiply two numbers and return the product.

"""
    return a * b

print(multiply.__doc__) # the docstring
help(multiply)
```

The first statement in a function can be a string - python stores
it as __doc__ and help() displays it.u Write these for anything
you will reuse.u

---

## lambda - inline anonymous function

```python
square = lambda x: x ** 2
print(square(5)) # 25
```

lambda is a one-expression function with no name. Prefer
def for anything more than a one-liner.u

---

## functions are first-class

```python
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def apply(func,text):
    return func(text)

print(apply(shout,"hi")) # HI
print(apply(whisper,"HI")) # hi
```

Functions can be passed around like any value - store them in
lists, dicts, pass to other functions. That backs callbacks,
decorators, and higher-order-functionstyle.u

---

## Next steps

go to Modules and Packages at modules-packages.md