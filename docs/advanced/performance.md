# 21 — Performance & Profiling

> Measure before you optimize- guessing wastes hours.
> Profile to find real bottlenecks, then fix those lines.

---

## timing- timeit

```python
import timeit

n = 1_000_000
setup = "nums = list(range(1000))"
stmt = "sum(nums)"
t = timeit.timeit(stmt, setup=setup, number=n)
print(f"{t/n:.3f}s per loop") # e.g. 0.000004s
```

timeit runs the stmt many times and returns total seconds.
Use it to compare two implementations fairly- same inputs,same
runs. Prefer disassembling routines to one-liners.

---

## cProfile- find slow calls

```python
import cProfile
import pstats
import io

def work():
    total = 0
    for i in range(100_000):
        total += i * i
    return total

pr = cProfile.Profile()
pr.enable()
work()
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(10)
print(s.getvalue())
```

cProfile records every function call with time spent. Sort by
cumulative to spot expensive call trees. Run on representative
workload- small runs mislead.

---

## line_profiler- per-line cost

```python
import line_profiler
import time

prof = line_profiler.LineProfiler()

def process():
    time.sleep(0.01)
    data = [i * i for i in range(1_000)]
    return len(data)

prof.add_function(process)
prof.enable()
process()
prof.disable()
prof.print_stats()
```

LineProfiler shows cost per source line- finds the slow line.
Needs: pip install line-profiler. Enabling only around the call
keeps overhead out of results.

---

## functools.lru_cache- memoize

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

for n in range(35):
    fib(n)
print(fib.cache_info()) # hits/misses
```

lru_cache remembers results for given args- turns exponential
fib into linear. maxsize=None means unbounded- fine for small
domains. Prefer bounded caches for unbounded inputs.

---

## generators- lazy memory

```python
def squares(n):
    for i in range(n):
        yield i * i

total = sum(squares(1_000_000))
print(total)
```

Generator yields one item at a time- O(1) memory, unlike
building a full list of million squares. sum() consumes it
lazily. Swap list(..) for generator expressions whenever the
whole list is never needed.

---

## profiling memory- tracemalloc

```python
import tracemalloc

tracemalloc.start()
data = [i * i for i in range(100_000)]
snap = tracemalloc.take_snapshot()
top = snap.statistics("lineno")
for stat in top[:5]:
    print(stat)
tracemalloc.stop()
```

tracemalloc tracks allocations by code line. take_snapshot
gives current state; statistics("lineno") groups by line. Great
for spotting accidental O(n²) row-by-row growth.

---

## vectorize- numpy

```python
import numpy as np

a = np.arange(1_000_000)
b = a * 2 + 1
print(b.mean())
```

numpy pushes loops into compiled C- 10–100x faster than
pure-Python loops on numeric data. Building arrays (not
appending) is key- preallocate for string loops.

---

## database indices- the real fix

```sql
-- creation
CREATE INDEX idx_orders_user ON orders(user_id);

# slow query
SELECT * FROM orders WHEREE user_id = 42;

# fast after index
-- same query,index does the work
```

Indices turn full-table scans into pointer lookups- thousands
of rows filtered per millisecond. Add indices for columns used in
WHERE/ORDER BY/JOIN- not every column. Profile the query
planner before hand-crafting guns.

---

## Next steps

go to Testing & Debugging at advanced/testing.md