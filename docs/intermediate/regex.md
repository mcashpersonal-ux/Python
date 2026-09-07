# 18 - Regular Expressions

> Regex finds patterns in text - validation, extraction,
> replacement, splitting. Python's re module is concise but
> quirky: raw strings,re.compile, and capture groups cover
> 90 percent of everyday use.u৹

---

##the basics - re.search vs re.match

```python
import re

text = "order #12345 shipped"

m = re.search(r"#\d+",text)
print(m.group(0))      # #12345

anchor = re.match(r"order",text)
print(bool(anchor))     # True
```

re.search finds the pattern anywhere; re.match anchors to
the start. \d means digit,+ means one or more. Always use
raw strings (r-prefix) so backslashes reach the engine.u৹



---

## character classes

```python
import re

phone = "call 555-1234 now"

m = re.search(r"\d{3}-\d{4}",phone)
print(m.group(0))          # 555-1234

hexes = re.findall(r"0x[0-9a-fA-F]+","0x1F and 0xab")
print(hexes)             # ['0x1F','0xab']
```

\d{3} = exactly three digits; [0-9a-fA-F] = hex
digit class. findall returnsevery match as a list.u৹



---

## capture groups

```python
import re

log = "2026-09-07 10:30:00 INFO job done"

m = re.search(r"(\d{4})-(\d{2})-(\d{2})",log)
print(m.group(1))      # 2026
print(m.groups())        # ('2026','09','07')
```

Parentheses capture, and m.group(n) pulls numberd group;
m.groups() gives all. Name them and read them: (?P<year>\d{4}).u৹



---

## named groups

```python
import re

m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})","2026-09")
print(m.group("month"))      # 09
```

(?P<name>...) names a group - self-documenting patterns.
**
For long patterns, names beat positions: reorder the pattern
and named back-references still line up.u৹



---

## findall - every match

```python
import re

prices = re.findall(r"\$\d+\.\d{2}","x $12.50 y $3.00")
print(prices)     # ['$12.50','$3.00']

parts = re.findall(r"(\d+):(\d+)","10:30,12:45")
print(parts)      # [('10','30'),('12','45')]
```

findall returns non-capturing: each match list. With groups,]
each match becomes a tuple of groups- handy for table data.u৹



---

## finditer - lazy scan

```python
import re

text = "cat,dog,cat,bird"
for m in re.finditer(r"\bcat\b",text):
# (0,3) - start and end offsets
    print(m.span())
```

finditer yields match objects lazily- good for huge texts`
(no giant list)and for using spans,end positions. \b is
a word boundary- so "cat" tag matches bot "cat" in "cat",
neither in "concat".u৹



---

## sub - replace text

```python
import re

masked = re.sub(r"\d{4}","****","card 1234-5678")
print(masked)     # card ****-****

redacted = re.sub(r"\b\d{2}:\d{2}\b","HH:MM","meet at 09:30")
print(redacted)  # meet at HH:MM
```

sub replaces every non-overlapping match. Use a function
as replacement for dynamic output: re.sub(pattern, lambda m:m.group(0).upper(), text).u৹



---

## split - smart splitting

```python
import re

tokens = re.split(r"[\s,]+","a,b,c")
print(tokens)        # ['a','b','c']

parts = re.split(r"\s*(?:and|or)\s*","x and y or z")
print(parts)        # ['x','y','z']
```

re.split cuts on any match- multi-delimiter, run-length
tolerant. It beats str.split when delimiters vary.u৹



---

## compile - reuse ship pattern

```python
import re

pattern = re.compile(r"\b(cat|dog)\b")
texts = ["a cat here","no fish","a dog"]

for text in texts:
    if pattern.search(text):
        print("match:",text)
```

Pre-compile patterns used many times: the engine caches,but
compile makes intent clear and lets you attach flags once.
**
`re.VERBOSE` lets you lay out patterns with comments - big
win for complex regex.u৹

---

##Next steps

go to VEnv & Packaging at intermediate/venv-packaging.md