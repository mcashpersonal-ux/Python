# 63 — Interactive notebooks with JupyterLab

> `jupyterlab` provides the notebook interface for exploratory work —
> run code cell-by-cell, inline plots, mix code with narrative markdown.
> The standard environment for data exploration and teaching, not for
> production services.

---

## install

```bash
pip install jupyterlab
```

---

## start the server

```bash
jupyter lab
```

This opens a browser tab at `http://localhost:8888/lab` with a file
browser, notebook editor, and terminal.

---

## a basic notebook cell

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("readings.csv")
df.plot(x="hour", y="value")
plt.show() # renders inline in the notebook, unlike in a plain script
```

`plt.show()` (or just leaving the figure as the last expression) renders
directly under the cell — no `savefig` needed for exploration.

---

## magic commands

```ipython
%matplotlib inline # ensure plots render inline (usually automatic now)
%timeit df["value"].sum() # benchmark a single line
%%time
# benchmark an entire cell
result = df.groupby("sensor").mean()
```

Lines starting with `%` (or `%%` for whole-cell) are Jupyter "magics" —
not valid outside a notebook/IPython session.

---

## displaying rich output

```python
from IPython.display import display, Markdown

display(Markdown("## Summary"))
display(df.describe()) # renders as a formatted table, not repr() text
```

---

## error handling basics

Exceptions in a cell print a traceback inline and stop that cell — earlier
cells' variables stay in memory, so you can fix and re-run just the
failing cell without restarting:

```python
try:
    risky_operation()
except Exception as e:
    print("caught:", e)
```

Watch for **stale state**: re-running cells out of order can leave
variables from a deleted/changed cell still in memory. Use "Restart
Kernel and Run All" before trusting a notebook's final output.

---

## snippets box

```python
# convert a notebook to a script for productionizing
```

```bash
jupyter nbconvert --to script analysis.ipynb
```

```python
# widgets for lightweight interactivity (needs ipywidgets)
from ipywidgets import interact

@interact(threshold=(0, 50))
def show(threshold=25):
    print(df[df["value"] > threshold])
```

---

## when to use what

| Need | Package |
|---|---|
| Exploration, teaching, one-off analysis | `jupyterlab` |
| Shareable app for non-technical users | `streamlit` |
| Reproducible production pipeline | plain `.py` scripts, not notebooks |

Next door: once analysis stabilizes, extract it into a `.py` module and
drop the notebook-only magics.
