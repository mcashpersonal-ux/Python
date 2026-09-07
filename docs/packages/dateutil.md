# python-dateutil — practical date handling

> python-dateutil extends the standard library with flexible parsing, relative deltas, and timezone helpers.

## Install and parse

```bash
python -m pip install python-dateutil
```

```python
from dateutil import parser

when = parser.isoparse("2026-09-08T02:30:00+06:00")
print(when.isoformat())
```

Prefer `isoparse()` for ISO-8601 input. General `parse()` accepts more formats but can interpret ambiguous input differently than your application expects.

## Relative dates

```python
from datetime import date
from dateutil.relativedelta import relativedelta

next_month = date(2026, 1, 31) + relativedelta(months=1)
print(next_month)  # 2026-02-28
```

Store instants with an explicit timezone and distinguish calendar arithmetic from fixed-duration arithmetic.

Next door: [Pendulum](pendulum.md) for a higher-level timezone API.
