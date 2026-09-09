# 08 - File Handling

> Reading and writing files is an everyday task: configs,
> logs, data exports. pathlib and open() cover most needs.

---

## reading a whole file

```python
from pathlib import Path

text = Path("data.txt" ).read_text()
print(text)
```

Path.read_text() opens, reads, and closes the file for you.
One line, no with needed. Pass encoding="utf-8" explicitly for reproducible behavior across platforms.

---

## writing a whole file

```python
from pathlib import Path

Path("out.txt").write_text("hello world\n", encoding="utf-8")
```

write_text() overwrites existing content. To append, use Path.open("a", encoding="utf-8") or open() with mode="a".
Folders must exist first - write_text does not create parents.

---

## append to a file

```python
with open("log.txt", "a") as f:
    f.write("new line\n")
```

mode "a" appends to the end. with closes the file automatically
even on errors - never forget closing, or data can vanish.

---

## reading line by line

```python
with open("data.txt")as f:
    for line in f:
        # no trailing newline
        print(line.strip())
```

Iterating over a file object yields lines lazily - great for
huge files. .strip() removes the trailing newline. Use
rstrip("\n") if you want to keep leading space.

---

## reading all lines into a list

```python
with open("data.txt")as f:
    lines = f.readlines()

# how many lines
print(len(lines))
```

readlines() consumes the whole file at once - fine for small
files, wasteful for gigabytes. Prefer iterating for big data.

---

## writing with a list of lines

```python
lines = ["a\n", "b\n", "c\n"]

with open("out.txt", "w")as f:
    f.writelines(lines)
```

writelines() takes an iterable of strings and writes each
with no separator added - you supply newlines yourself.

---

## JSON - save and load structured data

```python
import json

data = {"name": "Ada", "skills": ["python", "ml"]}

with open("data.json", "w")as f:
    json.dump(data, f)

with open("data.json" )as f:
    loaded = json.load(f)

print(loaded["skills"][0]) # python
```

json.dump serializes a python object into the file; json.load
reads it back. Round-trip safe for dicts, lists, strings,
numbers, booleans, and None.

---

## csv - tabular data

```python
import csv

rows = [["name", "age"], ["Ada", 36], ["Bob", 41]]

with open("people.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

with open("people.csv", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)
```

newline="" prevents blank lines on Windows. reader yields
lists of strings per row; writerows writes them all.

---

## binary files

```python
data = b"\\x00\\x01\\x02"

with open("blob.bin", "wb")as f:
    f.write(data)

with open("blob.bin", "rb")as f:
    raw = f.read()
print(raw)
```

Open in "rb"/"wb" for binary content - images, audio,
pickles. Bytes are just integers 0-255; text mode would
mangle them.

---

## error handling - missing file

```python
from pathlib import Path

p = Path("nope.txt")

if p.exists():
    print(p.read_text())
else:
    print("file not found")
```

Check exists() before reading to dodge a FileNotFoundError.
For racy situations (file deleted between check and open), use try/except:
see errors-exceptions.md).

---

## Next steps

go to Errors and Exceptions at errors-exceptions.md