# 16 - JSON and CSV

> Two workhorse data formats: JSON for nested, typed, structured
> data; CSV for tabular data that tools like Excel and pandas
> speak fluently. Python stdlibs make both trivial.

---

## parse JSON - from string

```python
import json

raw = '{"name": "ada","score": 36}'
data = json.loads(raw)
print(data["name"]) # ada
print(data["score"]) # 36
```

json.loads parses a string into plain Python objects: object
to dict, array to list, true to True. The reverse - dict to
string - is json.dumps.

---

## parse JSON - from a file

```python
import json

with open("config.json") as f:
    config = json.load(f)

print(config.get("theme", "dark"))
```

json.load(f) reads and parses the file in one step. Combine
with the with statement - and file handles never leak.

---

## write JSON - with formatting

```python
import json

data = {"name": "bob", "skills": ["py", "sql"], "age": 41}

with open("out.json", "w" )as f:
    json.dump(data, f, indent=2, sort_keys=True)
```

indent makes output human-readable; sort_keys stabilizes
key order for diffs. Compass file gives:
{
  "name": .
}

---

## handle missing keys safely

```python
import json

raw = '{"name": "ada"}'
data = json.loads(raw)

missing = data.get("age", 0)
nested = data["meta"].get("theme", "dark") if "meta" in data else "dark"

print(missing) # 0
print(nested) # dark
```

JSON from outside is untrusted shape: use .get() defaults,
check nesting before diving in, never assume keys exist.

---

## CSV - reading rows

```python
import csv

with open("data.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
```

csv.reader turns each line into a list of strings. Pass
newline="" to avoid blank-line glitches on some platforms.

``

---

## CSV - writing rows

```python
import csv

rows = [["name", "age"], ["ada", 36], ["bob", 41]]

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)
```

csv.writer handles quoting, escaping, i newlines for you-
never hand-build CSV strings. writerows takes a list of
rows in one call.

---

## CSV - dict reader/writer

```python
import csv

with open("data.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

DictReader uses the first row as headers, and gives dicts -
row["name"] instead of row[0]. Parallel writer: DictWriter
needs fieldnames passed in.

---

## reading JSON lines (NDJSON)

```python
import json

def load_ndjson(path):
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
```

NDJSON (newline-delimited JSON): one JSON object per line.

Perfect for logs and streaming exports - the data loads
incrementally, yielding one record at a time. json.loads per
line, or the faster json.JSONDecoder().raw_decode trick.

---

## flattening nested JSON into a flat dict

```python
def flatten(d, prefix="", sep="_"):
    out = {}
    for k, v in d.items():
        key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, key, sep))
        else:
            out[key] = v
    return out

data = {"user": {"name": "ada", "meta": {"tier": "pro"}}}
# {'user_name': 'ada','user_meta_tier': 'pro'}
print(flatten(data))
```

Recursive flattening turns nested dicts into flat key-value
pairs - handy before stuffing rows into a DataFrame or
CSV. Leaf values keep the dotted path in their keys.

---

## Next steps

go to Regular Expressions at intermediate/018-regex.md