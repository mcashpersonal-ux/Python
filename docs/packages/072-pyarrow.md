# 70 — Columnar data with Apache Arrow (pyarrow)

> `pyarrow` implements Apache Arrow's columnar in-memory format and
> Parquet file I/O — fast, language-agnostic data exchange and efficient
> storage for large tabular datasets. Pandas, DuckDB, and Spark all
> speak Arrow.

---

## install

```bash
pip install pyarrow
```

---

## read and write Parquet files

```python
import pyarrow as pa
import pyarrow.parquet as pq

table = pa.table({"sensor": ["line1", "line2"], "value": [23.4, 25.1]})
pq.write_table(table, "readings.parquet")

loaded = pq.read_table("readings.parquet")
print(loaded)
```

Parquet is columnar and compressed by default — typically far smaller
and faster to read than the equivalent CSV, especially for wide tables
where you only need a few columns.

---

## interop with pandas

```python
import pandas as pd
import pyarrow as pa

df = pd.DataFrame({"sensor": ["line1", "line2"], "value": [23.4, 25.1]})
table = pa.Table.from_pandas(df)

back_to_pandas = table.to_pandas()
```

```python
# pandas can also read/write parquet directly using pyarrow under the hood
df.to_parquet("readings.parquet")
df2 = pd.read_parquet("readings.parquet")
```

---

## reading only the columns you need

```python
import pyarrow.parquet as pq

table = pq.read_table("readings.parquet", columns=["value"])
```

Column pruning at read time is one of Parquet's biggest advantages over
CSV — you pay I/O cost only for the columns you actually select.

---

## working with large datasets in chunks

```python
import pyarrow.dataset as ds

dataset = ds.dataset("readings_partitioned/", format="parquet")
for batch in dataset.to_batches(columns=["sensor", "value"]):
    process(batch.to_pandas())
```

`pyarrow.dataset` handles partitioned directories of Parquet files and
streams them in batches instead of loading everything into memory at
once.

---

## error handling basics

```python
import pyarrow.parquet as pq
import pyarrow as pa

try:
    table = pq.read_table("readings.parquet")
except pa.ArrowInvalid as e:
    print("corrupt or invalid parquet file:", e)
except FileNotFoundError:
    print("file not found")
```

---

## snippets box

```python
# compression options when writing
pq.write_table(table, "readings.parquet", compression="zstd")
```

```python
# convert between Arrow and numpy for a single column
import numpy as np
values = table.column("value").to_numpy()
```

---

## when to use what

| Need | Package |
|---|---|
| Efficient columnar storage/exchange, Parquet | `pyarrow` |
| In-memory manipulation, everyday analysis | `pandas` |
| Raw numeric arrays only | `numpy` |

Next door: partition large `pandas` exports by date/sensor into Parquet
files for efficient downstream reads.
