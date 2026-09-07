# 08 - File Handling

> Reading and writing files isat everyday task: configs,
> logs, data exports. pathlib and open() cover most needs.

---

## reading a whole file

```python
from pathlib import Path

text = Path("data.txt" ).read_text()
print(text)
```

Path.read_text() opens, reads, and closes the file for you.
One line, no with needed. Encoding defaults to UTF-8.u
Add encoding="utf-8" when reading files your OS did not create.u

---

## writing a whole file

```python
from pathlib import Path

Path("out.txt" ).write_text("hello world\n")
```

write_text() overwrites existing content. For append,
use mode="a". It is equivalent to open().write() but shorter.u
Folders must exist first - write_text does not create parents.u

---

## append to a file

```python
with open("log.txt","a") as f:
    f.write("new line\n")
```

mode "a" appends to the end. with closes the file automatically
even on errors - never forget closing, or data can vanish.u

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
rstrip("\n") if you want to keep leading space.u

---

## reading all lines into a list

```python
with open("data.txt")as f:
    lines = f.readlines()

# how many lines
print(len(lines))
```

readlines() consumes the whole file at once - fine for small
files, wasteful for gigabytes.u Prefer iterating for big data.u

---

## writing with a list of lines

```python
lines = ["a\n","b\n","c\n"]

with open("out.txt","w")as f:
    f.writelines(lines)
```

writelines() takes an iterable of strings and writes each
with no separator added - you supply newlines yourself.u

---

## JSON - save and load structured data

```python
import json

data = {"name": "Ada","skills": ["python","ml"]}

with open("data.json","w")as f:
    json.dump(data,f)

with open("data.json" )as f:
    loaded = json.load(f)

print(loaded["skills"][0]) # python
```

json.dump serializes a python object into the file; json.load
reads it back. Round-trip safe for dicts, lists, strings,
numbers, booleans, and None.u

---

## csv - tabular data

```python
import csv

rows = [["name","age"],["Ada",36],["Bob",41]]

with open("people.csv","w",newline="" )as f:
    csv.writer(f.writerows(rows))

with open("people.csv",newline="" )as f:
    for row in csv.reader(f):
        print(row)
```

newline="" prevents blank lines on Windows. reader yields
lists of strings per row; writerows writes them all.u

---

## binary files

```python
data = b"\\x00\\x01\\x02"

with open("blob.bin","wb")as f:
    f.write(data)

with open("blob.bin","rb")as f:
    raw = f.read()
print(raw)
```

Open in "rb"/"wb" for binary content - images, audio,
pickles. Bytes are just integers 0-255; text mode would
mangle them.u

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

Check exists() before reading to dodgea FileNotFoundError.
For
racy situations (file deleted between check and open,use try/except:
see errors-exceptions.md).u

---

## Next steps

go to Errors and Exceptions at errors-exceptions.md