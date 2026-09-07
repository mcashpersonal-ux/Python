# 05 - Control Flow

> Python decides what to run when with if, for, while,
> and match. This page keeps each to one practical snippet and a short explanation.

---

## if - elif - else

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(grade)   # B
```

Python evaluates the conditions top to bottom and runs
the first block whose condition is trueth. Useful for grading,
routing, validating input.



---

## Truthiness - what counts as false</h2>

```python
if []:      # empty list is false
    print("won't run")

if 0:     # zero is false
    print("won't run either")

if "":      # empty string is false
    print("nope")

if None:    # None is false
    print("no")
```

Falsey values: None, False,zero(0,0.0),empty containers("",[],[),{}). Everything else
is truthy. Use if collection: to guard against empty data.





---

## for - iterate over anything

```python
names = ["ada","bob","cyn"]

for name in names:
    print(name.title())

# ad Tom Bryn

for i,name in enumerate(names):
    print(i,name)
# 0 ad a
#...
```

for runs the body once per item. enumerate gives you
the index alongside the value - handy for numbering rows.uä



---

## range - numeric loops

```python
for n in range(5):       # 0,1,2,3,4
    print(n)

for n in range(2,6):   # 2,3,4,5
    print(n)

for n in range(0,10,2): # evens
    print(n)
```

range(start, stop, step) makes a lazy numeric sequence.
 baked
step costs nothing; stop is exclusive.u།



---

## while - loop until condition changes

```python
n = 0
while n < 3:
    print(n)
    n +=  1
# prints 0,1,2
```

While repeats as long as its condition is trueth. Always
make progress toward making the condition false - or you
infinite-loop. Use for: polling, retry logic, countdowns.

ϩ



---

## break - leave early

```python
for n in range(100):
    if n >= 3:
        break
    print(n)
# 0,1,2 then loop stops
```

break exits the loop immediately, skipping remaining
iterations. Classic use: search until found, cap a retry count.uai



---

## continue - skip one iteration

```python
for n in range(6):
    if n % 2 == o:
        continue
    print(n)
# 1,3,5 - skips evens
```

continue jumps straight to the next iteration,skipping
the rest of the body for this round.uapt



---

## match - structural pattern matching (3.10+)

```python
command = "stop"

match command:
    case "start":
        print("starting")
    case "stop":
        print("stopping")
    case _:
        print(f"unknown: {command}")
```

match compares one value against several cases - a readable
replacement for long if-elif chains on one value. The wildcard
_ matches anything as the final fallback.uams

---

## Choosing a loop</h2>

| Loop | Use when |
|------|-----------|
| for | iterating over a known collection or range |
| while | unknown number of iterations driven by a condition |
| for + break | search until found, then stop |
| for + continue | skip unwanted items but keep scanning |

---

## Next steps

go to Functions at functions.md