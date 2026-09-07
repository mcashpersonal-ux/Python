# 61 — Web dashboards with Dash

> `dash` builds full interactive dashboards purely in Python — Plotly
> charts plus dropdowns, sliders, and callbacks, with no separate
> JavaScript frontend to write.

---

## install

```bash
pip install dash
```

---

## a minimal app

```python
from dash import Dash, dcc, html
import plotly.express as px

app = Dash(__name__)

fig = px.line(x=[0, 1, 2, 3], y=[18.2, 23.4, 31.1, 19.8], title="Temperature")

app.layout = html.Div([
    html.H1("Plant Dashboard"),
    dcc.Graph(figure=fig),
])

if __name__ == "__main__":
    app.run(debug=True)
```

---

## add interactivity with a callback

```python
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.DataFrame({"hour": [0, 1, 2, 3], "value": [18.2, 23.4, 31.1, 19.8], "sensor": ["a", "a", "b", "b"]})

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(options=df["sensor"].unique(), value="a", id="sensor-picker"),
    dcc.Graph(id="chart"),
])

@app.callback(Output("chart", "figure"), Input("sensor-picker", "value"))
def update_chart(sensor):
    filtered = df[df["sensor"] == sensor]
    return px.line(filtered, x="hour", y="value")

if __name__ == "__main__":
    app.run(debug=True)
```

Callbacks re-run automatically whenever an `Input` component's property
changes — no manual event wiring needed.

---

## live-updating with an interval

```python
from dash import dcc, Output, Input

app.layout.children.append(dcc.Interval(id="tick", interval=5000))  # ms

@app.callback(Output("chart", "figure"), Input("tick", "n_intervals"))
def refresh(n):
    return px.line(fetch_latest_data())
```

---

## error handling basics

```python
@app.callback(Output("chart", "figure"), Input("sensor-picker", "value"))
def update_chart(sensor):
    filtered = df[df["sensor"] == sensor]
    if filtered.empty:
        return px.line(title="No data for this sensor")
    return px.line(filtered, x="hour", y="value")
```

Callbacks that raise exceptions show a red error overlay in the browser
in debug mode — guard against empty/missing data explicitly rather than
letting the callback crash.

---

## snippets box

```python
# multiple outputs from one callback
@app.callback(
    Output("chart", "figure"),
    Output("status", "children"),
    Input("sensor-picker", "value"),
)
def update(sensor):
    return px.line(df[df.sensor == sensor]), f"Showing {sensor}"
```

---

## when to use what

| Need | Package |
|---|---|
| Full dashboard app with controls | `dash` |
| Fastest possible simple data app | `streamlit` |
| Just the chart, embedded elsewhere | `plotly` alone |

Next door: back the dropdown's data source with `influxdb-client` for
live telemetry.
