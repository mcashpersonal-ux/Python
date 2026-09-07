# 62 — Quick data apps with Streamlit

> `streamlit` turns a plain Python script into a web app — no HTML/CSS/JS,
> no callback wiring. Fastest path from "I have a script" to "I have a
> shareable tool" for internal data apps.

---

## install

```bash
pip install streamlit
```

---

## a minimal app

```python
# app.py
import streamlit as st
import pandas as pd

st.title("Plant Dashboard")

df = pd.read_csv("readings.csv")
st.line_chart(df, x="hour", y="value")
st.dataframe(df)
```

Run it with:

```bash
streamlit run app.py
```

Streamlit re-runs the entire script top-to-bottom on every interaction —
this is the core mental model, unlike Dash's targeted callbacks.

---

## widgets drive re-runs

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("readings.csv")

sensor = st.selectbox("Sensor", df["sensor"].unique())
threshold = st.slider("Alert threshold", 0.0, 50.0, 25.0)

filtered = df[df["sensor"] == sensor]
st.line_chart(filtered, x="hour", y="value")

hot = filtered[filtered["value"] > threshold]
if not hot.empty:
    st.warning(f"{len(hot)} readings above threshold")
```

Every widget's current value is just its return value — read it like a
normal variable, no separate state callback needed for simple cases.

---

## caching expensive operations

```python
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv("large_file.csv")

df = load_data()  # only re-runs the function when inputs change
```

Without caching, a slow load would re-run on every widget interaction —
`@st.cache_data` is essential for anything beyond toy data.

---

## error handling basics

```python
import streamlit as st

try:
    df = pd.read_csv("readings.csv")
except FileNotFoundError:
    st.error("readings.csv not found — check the file path")
    st.stop()
```

`st.stop()` halts the script cleanly instead of letting a later line
throw an unrelated exception on missing data.

---

## snippets box

```python
# session state for values that must persist across re-runs
if "counter" not in st.session_state:
    st.session_state.counter = 0
if st.button("Increment"):
    st.session_state.counter += 1
st.write(st.session_state.counter)
```

```python
# layout with columns
col1, col2 = st.columns(2)
col1.metric("Current", "23.4 C")
col2.metric("Max today", "31.1 C")
```

---

## when to use what

| Need | Package |
|---|---|
| Fastest internal tool from a script | `streamlit` |
| Fine-grained custom callbacks/layout | `dash` |
| Exploration in a notebook, not an app | `jupyterlab` |

Next door: cache a `pymodbus`/`influxdb-client` fetch with
`@st.cache_data` for a live polling dashboard.
