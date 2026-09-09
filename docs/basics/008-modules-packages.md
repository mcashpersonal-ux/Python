# 07 - Modules, Packages, and stdlib

> A module isa .py file of reusable code. A package isa folder
> of modules. The standard library ships hundreds of them. This
> page shows the import patterns you will use every day.

---

## import a module

```python
import math

print(math.sqrt(16)) # 4.0
print(math.pi) # 3.14159...
```

import loads the whole module into the namespace math. Use
math.name to reach anything inside.

---

## from - selective import

```python
from math import sqrt,pi

print(sqrt(16)) # 4.0
print(pi)
```

from math import name brings specific names into your namespace,
so you can use them bare. Handy when you only need a few things,
or you want shorter names.

---

## aliasing - succinct names

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = np.array([1,2,3])
```

import module as alias gives the module a shorter handle.
*
The community standard aliases above are everywhere in tutorials
and Stack Overflow.

---

## write your own module

```python
# mymath.py
def double(x):
    return x * 2

TWO = 2
```

```python
# app.py - same folder
import mymath

print(mymath.double(21)) # 42
print(mymath.TWO)
```

Any .py file is importable by filename (minus .py).)
Keep module names lowercase with underscores, no hyphens.

---

## packages - folders of modules

```python
# mypkg/__init__.py # can be empty
# mypkg/mathlib.py # regular module

# app.py
from mypkg import mathlib
from mypkg.mathlib import double
```

A folder with an __init__.py becomes a package you can
import from. The __init__ runs when the package loads - usually
leave it empty or put package-level docs there.

---

## if __name__ == "__main__" - dual-purpose scripts

```python
# tool.py
def main():
    print("running as a script")

if __name__ == "__main__":
    main()
```

Run python tool.py and main() runs. Import tool from elsewhere
and it does nothing - useful guards keep your demo code from
firing on import.

---

## aspect of the stdlib everyone uses

```python
import os
import sys
import json
from datetime import datetime
import re
import pathlib
from collections import defaultdict
import csv
import sqlite3
import random
import statistics

# working directory
print(os.getcwd())
# interpreter version
print(sys.version)
# True/False
print(pathlib.Path("data.txt").exists())
print(random.choice(["a","b","c"]))
print(statistics.mean([1,2,3,4]))
```

You rarely need third-party libs for basics - the stdlib covers
files, paths, dates, json, csv, math, and much more. Know
what exists before reaching for pip.

---

## installing third-party packages

```bash
pip install requests
```

```python
import requests
resp = requests.get("https://api.github.com")
print(resp.status_code)
```

pip install brings packages from PyPI into your environment.
Virtual environments (see venv-packaging.md keep projects
from conflicting.

---

## Next steps

go to File Handling at file-handling.md