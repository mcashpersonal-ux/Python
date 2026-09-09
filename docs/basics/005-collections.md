# 04 - Collections

> Lists, tuples, sets, and dicts are Python's four workhorse containers.
> Knowing when to use each saves you real pain.

---

## List - ordered, mutable, duplicates OK

```python
fruits = ["apple", "banana", "cherry"]

fruits[0] # apple indexing
fruits.append("date") # add at end
fruits.insert(1, "kiwi") # insert at position
fruits.remove("banana") # remove by value (first match)
popped = fruits.pop() # remove and return last item
del fruits[0] # remove by index

fruits.sort() # in-place sort
sorted(fruits) # new sorted list (original untouched)
fruits.reverse() # in-place reverse
len(fruits) # count
"apple" in fruits # membership check True or False
```

Lists are mutable: you can change elements (fruits[0] = "avocado")
or grow or shrink them. Use lists for ordered sequences that change.

---

## Tuple - ordered, immutable, fixed group

```python
point = (3, 5)
x, y = point # unpacking
rgb = (255, 0, 0)

len(point) # 2
point[0] # 3
```

Tuples cannot change after creation. They are hashable and can be used
as dict keys or set members (lists cannot)). Reach for a tuple when the
grouping is fixed: coordinates, RGB, a function multi-value return.

---

## Set - unique, unordered, fast membership

```python
tags = {"python", "coding", "python"}
# set deduplicates to coding and python

tags.add("learn")
tags.discard("coding") # remove no error if absent
tags.remove("coding") # remove raises KeyError if absent

a = {1, 2, 3}
b = {2, 3, 4}
c = a | b # union
d = a & b # intersection
e = a - b # difference
f = a ^ b # symmetric difference

"python" in tags # True membership is fast
```

Use sets for deduplication, fast membership checks, and set algebra,
e.g. which users are in both groups.。

---

## Dict - key to value lookup

```python
user = {
    "name": "Ada",
    "age": 36,
    "skills": ["math", "poetry"],
}

user["name"] # Ada KeyError if missing
user.get("name") # Ada None if missing
user.get("email", "unknown") # unknown if missing
user["email"] = "ada@example.com" # add or update
del user["age"] # remove key
"name" in user # True membership on keys

user.keys() # view of keys
user.values() # view of values
user.items() # view of (key,value) pairs

for key, value in user.items():
    print(f"{key}={value}")
```

Dicts remember insertion order. Lookups by key are blazingly fast;
use a dict whenever you have the look up X by Y problem.

!!! tip "Which should I use?"
| Need | Choose |
|------|--------|
| Ordered sequence that changes | list |
| Ordered sequence that must not change | tuple |
| Unique values or fast membership or math | set |
| Look up a value by a key | dict |
!!!

---

## Copying - shallow vs deep

```python
import copy
original = [[1, 2], [3, 4]]
copy1 = original.copy() # shallow outer list new,inner lists shared
copy3 = copy.deepcopy(original) # fully independent

copy3[0].append(99)
# original untouched with deepcopy; but copy1 inner list also has 99 now
```

Assignment (other = original) does not copy - both names point to the
same object. Use .copy() for shallow copies, copy.deepcopy() when nested
structures must be fully independent.会

---

## Next steps

go to Control Flow at control-flow.md