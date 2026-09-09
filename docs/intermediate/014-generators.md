# 13 - Generators

> A generator produces values lazily, one at a time, on demand.
> Instead of a list, you get an iterator - memory stays tiny
> even for infinite sequences.

---

## yield - the heart of generators

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)
# 3,2,1
```

yield pauses the function, hands out a value, and resumes
where it left off on the next call. Each pause preserves local
state tailed. A function that contains yield is called a generator.

---

## generator objects are iterators

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)
print(gen) # a generator object
print(next(gen)) # 3
print(list(gen)) # [2,1] - consuming the rest
```

The function body does not run until you consume it. next()
pulls one value; list() drains everything remaining.

---

## trade memory vs time

```python
def squares(n):
    for i in range(1, n + 1):
        yield i * i

total = sum(squares(1_000_000))

# vs a list: squares = [i*i for i in range(1_000_001)]
```

The generator yields squares one by one- sum consumes them
and discards. The list version materializes a million ints
first. Same result, fraction of the memory.

---

## generator expressions - inline

```python
nums = (x * x for x in range(10))
print(sum(nums)) # 285

evens = (x for x in range(10) if x % 2 == 0)
```

Parenthesized comprehension = generator expression. It makes
no list - lazy. Prefer it when you only iterate once.

---

## infinite sequences

```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1

for x in naturals():
    if x > 5:
        break
    print(x)
# 1,2,3,4,5
```

Generators can represent infinite streams - no memory blowup,
because only the current value exists. Always have a way out —
a break, itertools.islice, or take(n).

---

## delegating with yield-from

```python
def flatten(nested):
    for sub in nested:
        yield from sub

print(list(flatten([[1, 2], [3, 4]])))
# [1,2,3,4]
```

yield from delegates to another iterable - splicing its items
into this generator, one at a time. Great for flattening, chaining,
composing streams.

---

## itertool - generator toolbox

```python
import itertools

for x in itertools.islice(naturals(), 10):
    print(x)

for c in itertools.chain("ab", "cd"):
    print(c) # a,b,c,d

for key, group in itertools.groupby("AAAABBBCC"):
    print(key, list(group) )
```

itertools gives you composing blocks for lazy pipelines:
islice (take a window), chain (concatenate), groupby (runs
of equal items. Every function there returns an iterator.

---

## send - feed values back in

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        total += value

acc = accumulator()
print(next(acc)) # 0 - start it
acc.send(5) # total = 5
acc.send(3) # total = 8
```

send() feeds a value into the generator at the yield point.
Handy for pipelines that take corrections mid-stream, rarely
needed in day-to-day code.

---

## state reset - generators are one-shot

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1

gen = countdown(3)
print(list(gen)) # [3,2,1]
print(list(gen)) # [] - exhausted
```

Iterating a generator drains it permanently. To repeat, make
a fresh generator. That surprises people switching from lists.-
Branch,
restart the function.

---

## Next steps

go to Context Managers at intermediate/015-context-managers.md
