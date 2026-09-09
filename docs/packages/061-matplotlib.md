# 59 — Static plots with Matplotlib

> `matplotlib` is the foundational plotting library — publication-quality
> static charts with full control over every element. Most other Python
> plotting libraries (pandas' `.plot()`, seaborn) build on top of it.

---

## install

```bash
pip install matplotlib
```

---

## a basic line chart

```python
import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4]
y = [18.2, 23.4, 31.1, 19.8, 25.0]

plt.plot(x, y, marker="o")
plt.xlabel("Hour")
plt.ylabel("Temperature (C)")
plt.title("Line 1 Temperature")
plt.savefig("temperature.png", dpi=150)
plt.close()
```

`plt.savefig()` writes to a file without needing a display — the right
call in scripts and servers. Use `plt.show()` only in interactive
sessions.

---

## multiple series and a legend

```python
plt.plot(x, y, label="Line 1")
plt.plot(x, [20, 21, 22, 23, 24], label="Line 2")
plt.legend()
plt.savefig("comparison.png")
plt.close()
```

---

## subplots

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(x, y)
axes[0].set_title("Temperature")
axes[1].bar(["a", "b", "c"], [3, 7, 2])
axes[1].set_title("Counts")
fig.savefig("dashboard.png")
```

The object-oriented `fig, ax` style (rather than bare `plt.` calls) scales
better once a chart has multiple panels.

---

## plotting directly from pandas

```python
import pandas as pd

df = pd.DataFrame({"hour": x, "value": y})
ax = df.plot(x="hour", y="value", kind="line", marker="o")
ax.figure.savefig("from_pandas.png")
```

---

## error handling basics

```python
import matplotlib.pyplot as plt

try:
    plt.savefig("/no/such/dir/plot.png")
except FileNotFoundError as e:
    print("output directory doesn't exist:", e)
```

Also remember to `plt.close()` figures in loops/long-running processes —
matplotlib keeps them in memory until closed, which leaks over many
iterations.

---

## snippets box

```python
# style presets
plt.style.use("seaborn-v0_8")
```

```python
# annotate a point
plt.annotate("peak", xy=(2, 31.1), xytext=(2.5, 33), arrowprops=dict(arrowstyle="->"))
```

---

## when to use what

| Need | Package |
|---|---|
| Static, publication-quality charts | `matplotlib` |
| Interactive, zoomable charts for the web | `plotly` |
| Quick full dashboards with widgets | `streamlit` / `dash` |

Next door: swap to `plotly` when the same chart needs to be interactive
in a browser.
