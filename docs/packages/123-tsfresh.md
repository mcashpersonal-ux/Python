# 105 — Time-series features with tsfresh

> `tsfresh` automatically calculates a broad set of statistical characteristics from time series, turning repeated sensor windows into a feature table for exploration, anomaly detection, or supervised modeling. It is useful when manually choosing every vibration, temperature, or current statistic would be slow and incomplete.

## Install

```bash
python -m pip install tsfresh
```

For input that does not fit comfortably in memory, the project also documents an optional Dask extra: `python -m pip install "tsfresh[dask]"` [1]. The examples below are local, deterministic demonstrations: they synthesize sensor readings in memory, print tabular results, and do not require a sensor, network, proprietary hardware, or GUI display. `tsfresh` depends on scientific Python packages such as pandas, NumPy, SciPy, and scikit-learn; wheel availability and supported Python versions can vary by platform, so pin and test the complete environment used for production.

## Start offline: extract features from sensor windows

The long-format input convention is one row per observation, with an identifier for the window or asset, a sort column, and one or more sensor columns. `extract_features` groups by `column_id`, orders values by `column_sort`, and returns one row per ID. Starting with `MinimalFCParameters` keeps a first experiment fast; the default comprehensive settings calculate many more feature/calculator combinations [1] [2].

```python
import numpy as np
import pandas as pd
from tsfresh import extract_features
from tsfresh.feature_extraction import MinimalFCParameters

rng = np.random.default_rng(21)
rows = []
for window_id in range(6):
    time = np.arange(80)
    vibration = 0.25 * np.sin(2.0 * np.pi * time / 16.0)
    vibration += 0.02 * rng.standard_normal(time.size)
    vibration += 0.03 * window_id * np.sin(2.0 * np.pi * time / 7.0)
    temperature = 60.0 + 0.04 * time + 0.15 * window_id
    temperature += 0.08 * rng.standard_normal(time.size)
    rows.extend(
        {
            "window_id": window_id,
            "sample": int(sample),
            "vibration": float(vibration[sample]),
            "temperature": float(temperature[sample]),
        }
        for sample in range(time.size)
    )

readings = pd.DataFrame(rows)
features = extract_features(
    readings,
    column_id="window_id",
    column_sort="sample",
    default_fc_parameters=MinimalFCParameters(),
    n_jobs=0,
)

print("input shape:", readings.shape)
print("feature shape:", features.shape)
print(features.filter(like="vibration__").head(2).to_string())
```

The resulting columns encode the sensor kind and calculator, for example `vibration__mean` or `temperature__standard_deviation`. Keep the feature table's index aligned with labels and metadata; it represents the `window_id` values rather than individual samples. A calculation can produce `NaN` when a statistic is undefined for a short or constant series. Inspect missingness and use the documented `impute` helper or an explicitly fitted preprocessing policy before passing features to a model [1].

## Prepare windows from a sensor log

For a real historian or CSV export, first define the observation unit. A row can represent a fixed-duration window, a machine run, a batch, or an asset-day. Every window should have a stable identifier, a monotonic sample/order field, and measurements with known units. Do not let rows from two assets share an ID, and do not sort only by a wall-clock timestamp if timestamps can collide; use an additional sequence number when needed.

```python
import pandas as pd

raw = pd.DataFrame(
    {
        "asset": ["pump-A"] * 6 + ["pump-B"] * 6,
        "window": [0] * 3 + [1] * 3 + [0] * 3 + [1] * 3,
        "sample": [2, 0, 1] * 4,
        "pressure_kpa": [101.4, 101.0, 101.2, 104.0, 104.3, 104.1, 99.8, 99.7, 99.9, 100.2, 100.3, 100.1],
    }
)

raw["series_id"] = raw["asset"] + "::" + raw["window"].astype(str)
prepared = raw.sort_values(["series_id", "sample"]).dropna(
    subset=["series_id", "sample", "pressure_kpa"]
)
prepared = prepared.rename(columns={"pressure_kpa": "pressure"})
print(prepared[["series_id", "sample", "pressure"]].to_string(index=False))
```

The code above only validates and orders a small in-memory log; it does not connect to a live device. In production, perform unit conversion, duplicate detection, gap checks, clipping checks, and missing-value handling before extraction. Preserve the raw timestamp, asset, operating mode, load, maintenance state, and preprocessing version next to each feature row so a statistically unusual result can be investigated in physical context.

## Choose a feature budget and sensor-specific settings

A comprehensive extraction can be computationally expensive because it evaluates many calculators and parameter combinations. Use `MinimalFCParameters` for a smoke test, `EfficientFCParameters` when runtime matters, and `ComprehensiveFCParameters` when you are deliberately exploring a large candidate set [2]. Once a baseline experiment identifies useful calculators, a custom dictionary can restrict the output and make the pipeline more predictable.

```python
import numpy as np
import pandas as pd
from tsfresh import extract_features

readings = pd.DataFrame(
    {
        "window_id": np.repeat([0, 1, 2], 5),
        "sample": np.tile(np.arange(5), 3),
        "temperature": [60.0, 60.2, 60.1, 60.3, 60.4, 61.0, 61.3, 61.1, 61.4, 61.5, 62.0, 62.1, 62.4, 62.3, 62.6],
        "pressure": [100.0, 100.3, 100.1, 100.2, 100.4, 101.0, 101.2, 101.1, 101.3, 101.4, 102.0, 102.1, 102.2, 102.4, 102.3],
    }
)

settings = {
    "mean": None,
    "standard_deviation": None,
    "maximum": None,
    "minimum": None,
}
features = extract_features(
    readings,
    column_id="window_id",
    column_sort="sample",
    default_fc_parameters=settings,
    n_jobs=0,
)
print(features.to_string())
```

For different sensor kinds, `kind_to_fc_parameters` can give temperature, pressure, vibration, or current separate settings. Feature names and calculator availability are version-dependent, so record the tsfresh version, settings object or dictionary, input schema, and dependency lockfile with every model artifact. If a feature is expensive or unstable on short windows, remove it rather than silently accepting long runtimes or undefined values.

## Select features without leaking future information

Feature extraction creates candidates; it does not establish that a feature predicts a failure. With reviewed labels, split data chronologically or by asset before feature selection. Fit imputation, selection, scaling, and the final model on the training portion only. The following small, offline example uses `extract_relevant_features` with one binary label per sensor window, then prints the selected matrix shape [1].

```python
import numpy as np
import pandas as pd
from tsfresh import extract_relevant_features
from tsfresh.feature_extraction import MinimalFCParameters

rng = np.random.default_rng(4)
window_ids = np.arange(12)
readings = pd.DataFrame(
    {
        "window_id": np.repeat(window_ids, 24),
        "sample": np.tile(np.arange(24), window_ids.size),
    }
)
readings["vibration"] = np.sin(2.0 * np.pi * readings["sample"] / 8.0)
readings["vibration"] += 0.05 * rng.standard_normal(len(readings))
readings.loc[readings["window_id"] >= 9, "vibration"] += 0.8
labels = pd.Series((window_ids >= 9).astype(int), index=window_ids, name="failure")

selected = extract_relevant_features(
    readings,
    y=labels,
    column_id="window_id",
    column_sort="sample",
    default_fc_parameters=MinimalFCParameters(),
    n_jobs=0,
)
print("selected shape:", selected.shape)
print("selected columns:", selected.columns.tolist())
```

This demonstrates API usage, not a validated failure predictor. In a real study, label the event definition and prediction horizon before extraction, preserve a time-aware holdout, and check class balance and repeated-window leakage. A feature selected on all historical data can encode future operating conditions and produce an overly optimistic evaluation.

## Operational considerations

| Concern | Practical decision |
|---|---|
| Window definition | Use a fixed, documented duration or event boundary and retain overlap, sampling rate, and alignment metadata. |
| Missing samples | Detect gaps before extraction; distinguish an absent measurement from a real zero and record any imputation. |
| Runtime | Start with minimal or efficient settings, benchmark on representative windows, and consider the documented Dask extra for large inputs. |
| Feature stability | Compare distributions across assets, operating regimes, firmware changes, and sensor replacements before setting thresholds. |
| Reproducibility | Persist raw-data identifiers, tsfresh version, settings, preprocessing, labels, and feature-column order. |

## Safety notes

- These examples are **offline demonstrations only**. They do not read live telemetry, actuate equipment, open a GUI, or issue a control command.
- An extracted feature or statistically relevant feature is not a diagnosis. It can reflect a genuine fault, a changed load, a sensor mounting problem, a clock error, a data gap, or a maintenance activity.
- Do not use a tsfresh feature threshold by itself to trip machinery, suppress a protective function, extend an inspection interval, or declare an asset safe. Keep protection and shutdown logic independent from exploratory analytics.
- Validate sampling rate, units, anti-alias filtering, timestamps, asset identity, operating regime, clipping, and missingness before comparing features. A changed acquisition backend can shift feature distributions without a physical change.
- Guard against leakage from future rows, overlapping windows, post-failure measurements, duplicated records, and labels that would not be known at prediction time. Use chronological or asset-aware validation where appropriate.
- Feature extraction can consume substantial CPU, memory, and time. Bound input duration and row counts for untrusted files, prefer an explicit feature budget, and monitor worker/resource settings before processing large logs.
- Live acquisition is hardware-, driver-, permission-, and platform-dependent. Test acquisition and buffering separately from tsfresh, use replay data first, and require qualified review or an independently validated safety system for any physical response.

## Next door

Next door: combine [tsfresh's extraction and selection workflow](https://tsfresh.readthedocs.io/en/latest/text/quick_start.html) with [scikit-learn's time-aware model evaluation](https://scikit-learn.org/stable/modules/cross_validation.html) before deploying features into a condition-monitoring pipeline.

## References

[1]: https://tsfresh.readthedocs.io/en/latest/text/quick_start.html "tsfresh Quick Start"
[2]: https://tsfresh.readthedocs.io/en/latest/text/feature_extraction_settings.html "tsfresh Feature Extraction Settings"
[3]: https://pypi.org/project/tsfresh/ "tsfresh on PyPI"
[4]: https://scikit-learn.org/stable/modules/cross_validation.html "scikit-learn Cross-Validation"

The API behavior, feature-setting choices, installation options, and workflow caveats above are based on the [tsfresh Quick Start][1], [feature-setting reference][2], [PyPI project page][3], and [scikit-learn cross-validation documentation][4].

<!-- Sources: [1] [2] [3] [4] -->
