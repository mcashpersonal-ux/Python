# 03 — Numbers & Strings

> Arithmetic for numbersarid text-processing tools for strings — with f-strings to format either.

---

## Numbers: ints & floats

```python
a = 7
b = 2

a + b # 9 addition
a - b # 5 subtraction
a * b # 14 multiplication
a / b # 3.5 true division (always float)
a // b # 3 floor division
a % b # 1 modulo (remainder)
a ** b # 49 exponentiation
```

!!! warning "Division surprises"
`/` always returns a float: `4 / 2` → `2.0`. Use `//` when you need an integer. And remember floats have precision limits: `0.1 + 0.2` is `0.30000000000000004` — not a bug,just binary math.
!!!

## Common number tools

```python
abs(-5) # 5
round(3.14159,2) # 3.14
max(3,8,5) # 8
min(4,2) # 2
sum([1,2,3]) # 6
pow(2,10) # 1024

import math
math.sqrt(16) # 4.0
math.floor(3.7) # 3
math.ceil(3.2) # 4
math.pi # 3.141592653589793
```

---

## Strings basics

Strings are text wrapped in quotes:

```python
s1 = 'single quotes'
s2 = "double quotes"
s3 = """triple quotes
span multiple
lines"""
```

- Triple quotes keep newlines — useful for long text or docstrings.
- `+` concatenates; `*` repeats: `"ha" * 3` → `"hahaha"`.

## f-strings — format values into text

```python
name = "Ada"
age = 36
msg = f"{name} is {age} years old."
# 'Ada is 36 years old.'

price = 19.99
f"Price: ${price:.2f}" # 'Price: $19.99'
f"{age:>5}" # right-align,width 5: ' 36'
f"{1000000:,}" # thousands sep: '1,000,000'
f"{0.25:.1%}" # '25.0%'
```

The `f` prefix means "fill in the braces". Everything inside `{}` is evaluated as a mini-expression.

.

---

## Slicing — pluck pieces from strings

```python
s = "python"

s[0] # 'p' first char
s[-1] # 'n' last char
s[0:2] # 'py' from index 0 up to (not including) 2
s[:2] # 'py' from start
s[2:] # 'thon' to end
s[::2] # 'pto' every 2nd char
s[::-1] # 'nohtyp' reversed
```

!!! tip "Slicing mental model"
`s[start:stop:step]` — think of indices as gaps between characters. `stop` is exclusive,which makes `s[:2] + s[2:] == s` always true.
!!!

## String methods worth knowing

```python
text = " Hello,Python! "

text.strip() # 'Hello,Python!' remove outer whitespace
text.lower() # ' hello,python! '
text.pper() # ' HELLO,PYTHON! '
text.replace("Python","World") # ' Hello,World! '
text.split(",") # [' Hello',' Python! ']
",".join(["a","b"]) # 'a,b' inverse of split
text.startswith(" He") # True
text.endswith("! ") # True
"42".isdecimal() # True
```

Multiline text with `splitlines()` and `strip()` isa classic combo for cleaning data:

```python
raw = "one\n\ntwo\n\n\n"
raw.splitlines() # ['one','','two','','']
lines = [line for line in raw.strip().splitlines() if line.strip()]
```

---

## Chaining & immutability

```python
s = " Ada Lovelace "
clean = s.strip().title().replace("Lovelace","Byron")
# 'Ada Byron'
```

Strings are immutable — every "modification" returns a new string; the original is untouched. That's why we always reassign (`s = s.strip()`).

---

## Next steps

→ [04 — Collections](collections.md)