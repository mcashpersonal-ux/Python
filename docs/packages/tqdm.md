# tqdm — progress bars

> tqdm wraps iterables and reports progress with minimal code.

## Install and basic use

```bash
python -m pip install tqdm
```

```python
from time import sleep
from tqdm import tqdm

for item in tqdm(range(5), desc="Processing"):
    sleep(0.1)
```

## Manual updates

```python
from tqdm import tqdm

with tqdm(total=100, unit="item") as progress:
    for batch_size in (20, 30, 50):
        process_batch(batch_size)
        progress.update(batch_size)
```

The manual example assumes `process_batch` is your application function. Keep progress output separate from machine-readable stdout when the program is used in a pipeline; use logging or `tqdm.write()` for messages.

## Practical guidance

Progress bars add terminal output and a small measurement cost. Disable them in non-interactive jobs with a configuration flag, and do not expose sensitive item names in the description.

Next door: [Rich](rich.md) for richer terminal interfaces.
