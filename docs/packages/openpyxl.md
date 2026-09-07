# 64 — Read/write Excel with openpyxl

> `openpyxl` reads and writes `.xlsx` files without needing Excel
> installed — cell values, formulas, formatting, charts. The engine
> `pandas` uses under the hood for `.to_excel()`/`.read_excel()`.

---

## install

```bash
pip install openpyxl
```

---

## write a workbook

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Readings"

ws.append(["Sensor", "Value"])
ws.append(["line1", 23.4])
ws.append(["line2", 25.1])

wb.save("readings.xlsx")
```

---

## read a workbook

```python
from openpyxl import load_workbook

wb = load_workbook("readings.xlsx")
ws = wb.active

for row in ws.iter_rows(min_row=2, values_only=True):  # skip header
    print(row)
```

`values_only=True` returns plain tuples instead of `Cell` objects — use
`values_only=False` (default) when you need formatting/formulas too.

---

## multiple sheets

```python
wb = Workbook()
ws1 = wb.active
ws1.title = "Line1"
ws2 = wb.create_sheet("Line2")

ws1.append(["hour", "value"])
ws2.append(["hour", "value"])

wb.save("multi.xlsx")

wb2 = load_workbook("multi.xlsx")
print(wb2.sheetnames)
print(wb2["Line2"]["A1"].value)
```

---

## formatting cells

```python
from openpyxl.styles import Font, PatternFill

cell = ws["A1"]
cell.font = Font(bold=True, size=12)
cell.fill = PatternFill(start_color="FFFF00", fill_type="solid")

ws.column_dimensions["B"].width = 15
```

---

## error handling basics

```python
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

try:
    wb = load_workbook("readings.xlsx")
except FileNotFoundError:
    print("file not found")
except InvalidFileException:
    print("not a valid xlsx file")
```

---

## snippets box

```python
# formulas — written as strings, Excel computes them on open
ws["C2"] = "=B2*1.8+32"
```

```python
# via pandas instead, when you already have a DataFrame
import pandas as pd
df.to_excel("readings.xlsx", index=False, sheet_name="Readings")
```

---

## when to use what

| Need | Package |
|---|---|
| Read/write with formatting, formulas, multiple sheets | `openpyxl` |
| Fastest possible writes, no reading | `xlsxwriter` |
| Already have a DataFrame, don't need cell-level control | `pandas.to_excel` |

Next door: use `pandas.read_excel(engine="openpyxl")` once cell-level
control isn't needed.
