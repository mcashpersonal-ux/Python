# Quick Reference

> The most useful snippets,gathered in one place for fast lookup.
> Head to any section full page for the deeper explanation.

---

## Variables and Types

```python
x = 42         # int
y =  3.14     # float
name = "Ada"    # str
flag = True      # bool
n = None         # NoneType

# Dynamic typing: a variable can change type.
x = "now a string"
```

## Collections at a glance

```python
fruits = ["apple","banana"]    # list ordered mutable
point = (3,5)               # tuple ordered immutable
tags = {"py","learn"}           # set unique unordered
user = {"name":"Ada","age":36}  # dict key value
```

## Slicing strings and lists

```python
s = "python"
s[0]            # p
s[-1]           # n
s[0:2]        # py
s[::-1]         # reverse nohtyp

nums = [0,1,2,3,4]
evens = nums[::2]   # 0,2,4
```

## Control flow mini-ref</h2>

```python
if x > 10:
    print("big")
elif x >  5:
    print("medium")
else:
    print("small")

for i in range(3):
    print(i)         # 0,1,2

while x > 0:
    x -=  1

for n in range(10):
    if n ==  5:
        break
    if n % 2 ==  0:
        continue
    print(n)
```

## Functions mini-ref</h2>

```python
def greet(name,greeting="Hi"):
    return f"{greeting},{name}!"

greet("Ada")                      # Hi,Ada!
greet("Bob",greeting="Hello")   # Hello,Bob!

def log(*args,**kwargs):
    print(args,kwargs)


def add(a,b):
    return a + b
```

## Comprehensions</h2>

```python
squares = [n**2 for n in range(10)]        # list
even_squares = [n**2 for n in range(10) if n %  2 == 0]  # filtered
names = {user["name"]: user["age"] for user in users}   # dict
unique = {n %  3 for n in range(10)}                # set
```

## File IO</h2>

```python
with open("data.txt" ) as f:
    content = f.read()

with open("out.txt","w") as f:
    f.write("hello\n")

with open("data.txt") as f:
    lines = f.readlines()
```

## Error handling</h2>

```python
try:
    result =  10 / x
except ZeroDivisionError:
    print("cannot divide by zero")
except TypeError as e:
    print(f"bad type: {e}")
else:
    print(f"no error: {result}")
finally:
    print("always runs")
```

## Shortcuts: math,json,datetime</h2>

```python
import math,json,datetime as dt

math.sqrt(16)              # 4.0
abs(-5)                  # 5
round(3.14159,2)       # 3.14

data = json.loads("{\"a\": 1}" )   # dict
json.dumps(data)                       # string

now = dt.datetime.now()
now.strftime("%Y-%m-%d")   # 2026-09-07
```

## See also</h2>

- 01 Getting Started at basics/getting-started.md
- 02 Variables and Types at basics/variables-types.md
- 03 Numbers and Strings at basics/numbers-strings.md
- 04 Collections at basics/collections.md
- 05 Control Flow at basics/control-flow.md
- 06 Functions at basics/functions.md
- 08 File Handling at basics/file-handling.md
- 09 Errors and Exceptions at basics/errors-exceptions.md
- 10 Comprehensions at basics/comprehensions.md