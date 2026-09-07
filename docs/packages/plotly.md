# 60 — Interactive charts with Plotly

> `plotly` builds interactive, browser-based charts — zoom, hover
> tooltips, export — from a Python API. Renders standalone HTML or embeds
> in Jupyter/Dash apps.

---

## install

```bash
pip install plotly
```

---

## a basic interactive line chart

```python
import plotly.express as px

fig = px.line(x=[0, 1, 2, 3, 4], y=[18.2, 23.4, 31.1, 19.8, 25.0],
               labels={"x": "Hour", "y": "Temperature (C)"}, title="Line 1 Temperature")
fig.write_html("temperature.html")
```

`plotly.express` (`px`) is the high-level, one-call-per-chart-type API —
use it first before dropping to `plotly.graph_objects` for custom
layouts.

---

## plot directly from a pandas DataFrame

```python
import pandas as pd
import plotly.express as px

df = pd.DataFrame({"hour": [0, 1, 2, 3], "value": [18.2, 23.4, 31.1, 19.8], "sensor": ["a", "a", "b", "b"]})
fig = px.line(df, x="hour", y="value", color="sensor")
fig.show()  # opens in browser/Jupyter
```

---

## multiple chart types

```python
import plotly.express as px

fig = px.bar(df, x="sensor", y="value")
fig2 = px.scatter(df, x="hour", y="value", size="value", color="sensor")
fig3 = px.histogram(df, x="value")
```

---

## fine-grained control with graph_objects

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 1, 2], y=[1, 3, 2], mode="lines+markers", name="line1"))
fig.update_layout(title="Custom Chart", xaxis_title="Hour", yaxis_title="Value")
fig.write_html("custom.html")
```

---

## error handling basics

```python
import pandas as pd
import plotly.express as px

df = pd.DataFrame({"hour": [], "value": []})
fig = px.line(df, x="hour", y="value")
if not fig.data or len(fig.data[0].x) == 0:
    print("no data to plot — check upstream query/filter")
```

Plotly rarely raises on empty data — it silently renders a blank chart,
so validate your DataFrame has rows before charting.

---

## snippets box

```python
# export as a static image (needs kaleido: pip install kaleido)
fig.write_image("chart.png")
```

```python
# embed inside a Dash app instead of a standalone file
import dash
from dash import dcc

app = dash.Dash(__name__)
app.layout = dcc.Graph(figure=fig)
```

---

## when to use what

| Need | Package |
|---|---|
| Interactive charts for the web/Jupyter | `plotly` |
| Static images, print/publication | `matplotlib` |
| Full multi-chart dashboard app | `dash` (built on Plotly) |

Next door: drop the figure straight into a `dash` layout for a
click-through dashboard.
