# polars — fast, multi-threaded dataframes

> polars is a DataFrame library built in Rust with a Python API. It uses
> all your CPU cores and a lazy query engine by default, which makes it
> dramatically faster than pandas on medium-to-large data — with a
> similar, if stricter, API.

## Install and load data

```bash
python -m pip install polars
```

```python
import polars as pl

df = pl.read_csv("readings.csv")
print(df.head())
print(df.schema)
```

Column types are inferred and strict — polars will not silently mix
strings and numbers in one column the way a looser tool might.

## select, filter, and compute

```python
import polars as pl

df = pl.DataFrame({"sensor": ["a", "a", "b"], "value": [1.5, 2.0, 9.9]})

result = (
    df.filter(pl.col("value") > 1.0)
    .group_by("sensor")
    .agg(pl.col("value").mean().alias("avg_value"))
)
print(result)
```

Expressions (`pl.col(...)`) are the core idiom — they describe *what* to
compute, and polars decides how to execute it efficiently, including
across multiple columns in parallel.

## lazy evaluation for big files

```python
import polars as pl

lazy = (
    pl.scan_csv("big_file.csv")
    .filter(pl.col("status") == "ok")
    .select(["id", "value"])
)
result = lazy.collect()   # nothing runs until collect()
```

`scan_csv` builds a query plan without reading the whole file; polars can
then push the filter and column selection down into the read itself,
often touching far less data than pandas would for the same result.

## converting to/from pandas

```python
import polars as pl

df = pl.read_csv("readings.csv")
pandas_df = df.to_pandas()          # needs pandas + pyarrow installed
back = pl.from_pandas(pandas_df)
```

Useful when a downstream library (a plotting call, an existing pipeline)
only accepts a pandas DataFrame.

## when to use what

| Need | Package |
|---|---|
| Existing pandas-based codebase, smaller data | `pandas` |
| New project, large CSV/Parquet files, want speed | `polars` |
| Out-of-core / bigger-than-RAM columnar data | `pyarrow` (with polars or duckdb) |

Next door: [pandas](060-pandas.md) for the older, more widely-integrated
alternative, and [pyarrow](072-pyarrow.md) for the columnar format both
of them can read and write.
