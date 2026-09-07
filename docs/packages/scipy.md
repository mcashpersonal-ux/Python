# 66 — Scientific computing with SciPy

> `scipy` extends NumPy with optimization, statistics, signal processing,
> interpolation, and linear algebra routines — the toolkit for anything
> beyond basic array math.

---

## install

```bash
pip install scipy
```

---

## statistics

```python
from scipy import stats
import numpy as np

data = np.array([18.2, 23.4, 31.1, 19.8, 25.0])
print(stats.describe(data))

t_stat, p_value = stats.ttest_1samp(data, popmean=20)
print(t_stat, p_value)
```

---

## optimization (curve fitting)

```python
from scipy.optimize import curve_fit
import numpy as np

def model(x, a, b):
    return a * np.exp(b * x)

x = np.array([0, 1, 2, 3, 4])
y = np.array([1.0, 2.7, 7.4, 20.1, 54.6])

params, covariance = curve_fit(model, x, y)
a, b = params
print(f"a={a:.2f}, b={b:.2f}")
```

---

## signal processing

```python
from scipy import signal
import numpy as np

t = np.linspace(0, 1, 500)
noisy = np.sin(2 * np.pi * 5 * t) + 0.5 * np.random.randn(500)

b, a = signal.butter(4, 0.1, btype="low")
filtered = signal.filtfilt(b, a, noisy)
```

Common in telemetry pipelines — smoothing noisy sensor data before
analysis or alerting.

---

## interpolation

```python
from scipy.interpolate import interp1d
import numpy as np

x = np.array([0, 1, 2, 3])
y = np.array([10, 20, 15, 25])

f = interp1d(x, y, kind="linear")
print(f(1.5))  # interpolated value between known points
```

---

## error handling basics

```python
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
import warnings

try:
    with warnings.catch_warnings():
        warnings.simplefilter("error", OptimizeWarning)
        params, _ = curve_fit(model, x, y)
except RuntimeError as e:
    print("fit did not converge:", e)
```

`curve_fit` raising `RuntimeError` usually means bad initial guesses —
pass `p0=[...]` with reasonable starting values for the parameters.

---

## snippets box

```python
# linear algebra beyond numpy basics
from scipy import linalg

A = np.array([[3, 1], [1, 2]])
b = np.array([9, 8])
x = linalg.solve(A, b)
```

---

## when to use what

| Need | Package |
|---|---|
| Optimization, stats, signal processing | `scipy` |
| Basic array math only | `numpy` |
| Symbolic (exact) math | `sympy` |

Next door: feed a fitted model's predictions back into `pandas` for
comparison against actuals.
