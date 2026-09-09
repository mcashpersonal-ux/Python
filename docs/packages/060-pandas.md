# 58 — DataFrames with pandas

> `pandas` is the standard tool for labeled tabular data — load CSVs,
> clean messy columns, resample time series, group and aggregate. Built
> on NumPy, and the natural next step once raw arrays aren't enough.

---

## install

```bash
pip install pandas
```

---

## load and inspect data

```python
import pandas as pd

df = pd.read_csv("readings.csv")
print(df.head())
print(df.info())
print(df.describe())
```

---

## select, filter, and compute columns

```python
hot = df[df["value"] > 25]
df["value_f"] = df["value"] * 9 / 5 + 32 # new column from existing ones
subset = df[["sensor", "value"]]
```

---

## group and aggregate

```python
summary = df.groupby("sensor")["value"].agg(["mean", "max", "min"])
print(summary)
```

---

## time series: parse dates and resample

```python
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.set_index("timestamp")

hourly_avg = df["value"].resample("1h").mean()
print(hourly_avg)
```

Setting a `DatetimeIndex` unlocks `.resample()`, rolling windows, and
date-based slicing (`df["2026-01-01":"2026-01-02"]`).

---

## error handling basics

```python
import pandas as pd

try:
    df = pd.read_csv("readings.csv")
except FileNotFoundError:
    print("file not found")
except pd.errors.EmptyDataError:
    print("file is empty")
except pd.errors.ParserError as e:
    print("could not parse CSV:", e)
```

Also watch for silent `NaN` from bad rows — `df.isna().sum()` shows how
many missing values landed in each column after loading.

---

## snippets box

```python
# fill or drop missing values
df["value"] = df["value"].fillna(df["value"].mean())
df = df.dropna(subset=["sensor"])
```

```python
# merge two dataframes like a SQL join
merged = df.merge(metadata_df, on="sensor", how="left")
```

```python
# write back out
df.to_csv("cleaned.csv", index=False)
df.to_excel("cleaned.xlsx", index=False) # needs openpyxl installed
```

---

## when to use what

| Need | Package |
|---|---|
| Labeled tabular/time-series data | `pandas` |
| Raw numeric arrays only | `numpy` |
| Data too large for memory | consider `pyarrow` + chunked reads |

Next door: chart a resampled series with `matplotlib` or `plotly`.
