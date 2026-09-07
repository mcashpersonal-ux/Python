# 57 — N-dimensional arrays with NumPy

> `numpy` is the foundation of Python's scientific stack — fast
> n-dimensional arrays and vectorized math, in C under the hood. Pandas,
> scikit-learn, and most numeric libraries are built on it.

---

## install

```bash
pip install numpy
```

---

## create arrays and do vectorized math

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)        # [11 22 33 44] — element-wise, no loop needed
print(a * 2)         # [2 4 6 8]
print(a.mean())       # 2.5
```

Vectorized operations run in compiled C loops — far faster than a Python
`for` loop over the same data for large arrays.

---

## multi-dimensional arrays and indexing

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.shape)   # (2, 3)
print(matrix[0, :])   # first row: [1 2 3]
print(matrix[:, 1])   # second column: [2 5]
print(matrix.T)       # transpose
```

---

## boolean masking and filtering

```python
readings = np.array([18.2, 23.4, 31.1, 19.8, 40.0])
hot = readings[readings > 25]
print(hot)  # [31.1 40. ]

readings[readings > 35] = np.nan  # flag out-of-range as missing
```

---

## generate and reshape data

```python
zeros = np.zeros((3, 4))
ones = np.ones(5)
range_arr = np.arange(0, 10, 2)          # [0 2 4 6 8]
linspace = np.linspace(0, 1, 5)          # 5 evenly spaced points

reshaped = np.arange(12).reshape(3, 4)
```

---

## error handling basics

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([1, 2])
try:
    a + b
except ValueError as e:
    print("shape mismatch:", e)
```

Shape mismatches are the most common NumPy error — check `.shape` when
operations fail unexpectedly.

---

## snippets box

```python
# save and load arrays
np.save("readings.npy", readings)
loaded = np.load("readings.npy")
```

```python
# basic stats in one call
print(np.mean(readings), np.std(readings), np.percentile(readings, 95))
```

---

## when to use what

| Need | Package |
|---|---|
| Raw numeric arrays, linear algebra | `numpy` |
| Labeled tabular data, time series | `pandas` (built on numpy) |
| Symbolic math instead of numeric | `sympy` |

Next door: wrap arrays in `pandas` DataFrames once you need labels and
mixed types.
