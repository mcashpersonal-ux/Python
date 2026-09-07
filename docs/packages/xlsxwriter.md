# 65 — High-performance Excel writing with XlsxWriter

> `XlsxWriter` writes `.xlsx` files only (no reading) but does it fast and
> with rich formatting — charts, conditional formatting, cell styles. The
> pick when you're generating reports rather than editing existing files.

---

## install

```bash
pip install xlsxwriter
```

---

## write a basic workbook

```python
import xlsxwriter

wb = xlsxwriter.Workbook("readings.xlsx")
ws = wb.add_worksheet("Readings")

ws.write_row(0, 0, ["Sensor", "Value"])
ws.write_row(1, 0, ["line1", 23.4])
ws.write_row(2, 0, ["line2", 25.1])

wb.close()
```

`wb.close()` is required — nothing is actually written to disk until
then, unlike `openpyxl`'s `save()` which can be called mid-session too.

---

## formatting cells

```python
wb = xlsxwriter.Workbook("formatted.xlsx")
ws = wb.add_worksheet()

bold = wb.add_format({"bold": True})
money = wb.add_format({"num_format": "$#,##0.00"})

ws.write(0, 0, "Sensor", bold)
ws.write(1, 1, 1234.5, money)

wb.close()
```

Formats are created once via `add_format()` and reused across cells —
more efficient than per-cell styling in large sheets.

---

## conditional formatting

```python
ws.write_column(0, 0, [18.2, 23.4, 31.1, 19.8, 40.0])
ws.conditional_format(0, 0, 4, 0, {
    "type": "cell", "criteria": ">", "value": 30,
    "format": wb.add_format({"bg_color": "#FFC7CE"}),
})
```

---

## charts

```python
chart = wb.add_chart({"type": "line"})
chart.add_series({"values": "=Readings!$B$2:$B$3"})
ws.insert_chart("D2", chart)
```

---

## error handling basics

```python
import xlsxwriter

try:
    wb = xlsxwriter.Workbook("/no/such/dir/report.xlsx")
    ws = wb.add_worksheet()
    ws.write(0, 0, "test")
    wb.close()
except Exception as e:
    print("could not write workbook:", e)
```

`XlsxWriter` mostly surfaces filesystem errors at `close()` time since
writing is buffered until then — wrap the whole block, not just
`Workbook(..)`.

---

## snippets box

```python
# writing directly from pandas via this engine for speed
import pandas as pd
with pd.ExcelWriter("readings.xlsx", engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Readings", index=False)
```

---

## when to use what

| Need | Package |
|---|---|
| Fast report generation, charts, formatting | `xlsxwriter` |
| Need to also read/edit existing .xlsx files | `openpyxl` |

Next door: generate the report as the final step of a `pandas`
cleaning/aggregation pipeline.
