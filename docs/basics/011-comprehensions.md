# 10 - Comprehensions

> Comprehensions build new collections from existing ones in
> one expressive line: list, dict, set, and generator versions.
> Read them left-to-right: output expression, then for, then
> optional if filters.

---

## list comprehension - basics

```python
nums = [1, 2, 3, 4, 5]

squares = [n * n for n in nums]
print(squares)
# [1,4,9,16,25]
```

[n * n for n in nums] reads "square, for each n from nums".
It is equivalent to a for loop building a list, but tighter
and usually faster.

---

## with filter

```python
nums = [1, 2, 3, 4, 5, 6]

evens = [n for n in nums if n % 2 == 0]
print(evens)
# [2,4,6]
```

The optional if at the end keeps only items that pass. Filtering
in the comprehension avoids a separate loop plus append.

---

## transform plus filter

```python
words = ["ada", "bob", "cynthia", "dave"]

loud = [w.upper() for w in words if len(w) > 3]
print(loud)
# ['CYNTHIA', 'DAVE']
```

Expression (upper(, loop (for w, and filter (if len).
Build exactly the output you want in one pass.

---

## dict comprehension

```python
names = ["ada", "bob"]

lookup = {name: len(name) for name in names}
print(lookup)
# {'ada': 3,'bob': 3}
```

{key: value for ..} builds a dict. Classic uses: index
items by id, invert a mapping, build lookup tables.

---

## set comprehension

```python
nums = [1, 1, 2, 2, 3, 3]

unique = {n for n in nums}
print(unique)
# {1,2,3}
```

Sets keep unique items only- the comprehension dedupes
automatically. Ordering is not guaranteed though.

---

## nested comprehension - flatten

```python
matrix = [[1, 2], [3, 4]]

flat = [n for row in matrix for n in row]
print(flat)
# [1,2,3,4]
```

The for clauses read left to right: outer first, inner second.
 That
mirrors the nested-loop version:

```python
flat = []
for row in matrix:
    for n in row:
        flat.append(n)
```

---

## conditional expression in the output slot

```python
nums = [1, 2, 3, 4, 5]

labels = ["even" if n % 2 == 0 else "odd" for n in nums]
print(labels)
# ['odd','even','odd','even','odd']
```

The if here is the ternary expression - it runs for every item.

Compare with the filter if at the end, and: filter drops items,
ternary keeps all but changes values.

---

## generator expression - lazy

```python
nums = range(1, 000, 000)

total = sum(n * n for n in nums)
```

Generators produce values lazily-on demand-and do not build the
whole list in memory. sum((n*n for n in nums)) and sum(n*n
for n in nums) do the same-and the parens can be omitted when the
generator is the only argument. Use generator expressions for huge
or infinite sources.

---

## when not to use a comprehension

```python
# readable loop - keep it
result = []
for x in data:
    if x.is_valid():
        result.append(x.process())

# nested too deep - split it
# one comprehension per step,or anamed function
```

Comprehensions shine when simple. If you need else-branches,
breaks, or multiple statements, a plain for loop wins on
readability. Er, as Aidan says: clarity > cleverness.

---

## Next steps

Basics complete. go to Intermediate: OOP at
intermediate/012-oop.md