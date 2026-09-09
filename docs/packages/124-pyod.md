# 106 — Anomaly detection with PyOD

> `pyod` is a Python toolkit for detecting unusual observations with more than 40 outlier-detection algorithms. It is useful for condition monitoring when sensor features are converted into a table of operating observations, but an anomaly score is evidence for investigation rather than a diagnosis by itself.

## Install

```bash
python -m pip install pyod
```

The examples below are local, deterministic demonstrations. They generate measurements in memory, print results, and do not connect to a sensor, PLC, historian, network, or GUI display. PyOD depends on NumPy, SciPy, scikit-learn, and other scientific packages, so wheel availability can vary by Python version, operating system, and CPU. Pin a tested PyOD and dependency set for repeatable production scoring.

## First example: offline condition-monitoring data

A useful first model has one row per observation window and columns that describe the equipment state. The example below represents vibration RMS, winding temperature, and motor current. Most observations form a normal operating population; a few synthetic rows have a simultaneous temperature and vibration increase. `IForest` fits an isolation forest and labels observations with `1` for outlier and `0` for inlier.

```python
import numpy as np
from pyod.models.iforest import IForest

rng = np.random.default_rng(7)
normal = rng.normal(
    loc=[2.0, 65.0, 18.0],
    scale=[0.15, 2.0, 0.8],
    size=(120, 3),
)
known_events = np.array(
    [
        [3.2, 84.0, 22.5],
        [3.5, 88.0, 23.0],
        [3.0, 81.0, 21.8],
    ],
    dtype=float,
)
features = np.vstack([normal, known_events])

model = IForest(contamination=0.03, random_state=7)
model.fit(features)
predictions = model.predict(features)

print("detected outliers:", int((predictions == 1).sum()))
print("last three labels:", predictions[-3:].tolist())
print("last three scores:", np.round(model.decision_function(features[-3:]), 3).tolist())
```

PyOD exposes fitted labels through `labels_` and fitted decision scores through `decision_scores_`. For new rows, `predict` returns labels and `decision_function` returns scores. In PyOD's standard convention, larger decision-function values are more abnormal; inspect the fitted version's API when combining scores from different detector classes. The contamination setting is a modeling assumption about the expected outlier fraction, not a measured probability that a bearing or motor will fail.

## Choose features and operating context

Condition monitoring works better when features have a physical interpretation and are calculated over a consistent window. Candidate features include vibration RMS or crest factor, temperature rise above ambient, pressure, flow, current, speed, and rate-of-change. Preserve asset ID, timestamp, operating mode, load, and maintenance state alongside the numeric feature matrix even when those columns are not passed directly to the detector.

Operating regimes can make a healthy machine appear anomalous. A single global model may flag a legitimate startup or high-load condition. Segment the training data by a known regime, add operating variables, or use separate models when the process has materially different normal populations. Standardize features when an algorithm is scale-sensitive; tree-based isolation methods are less sensitive to scale, but comparable units still improve review and feature diagnostics.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

raw_features = np.array(
    [
        [1.8, 61.0, 15.0],
        [2.0, 64.0, 17.0],
        [2.2, 68.0, 19.0],
    ],
    dtype=float,
)
scaler = StandardScaler().fit(raw_features)
scaled_features = scaler.transform(raw_features)

print("scaled shape:", scaled_features.shape)
print("scaled means:", np.round(scaled_features.mean(axis=0), 6).tolist())
```

Fit preprocessing only on an approved baseline period. If the baseline already contains an undetected fault, the model can learn the fault as normal. For a fleet, decide whether one model is appropriate across assets; otherwise retain one scaler and detector per comparable asset class or operating regime.

## Score a held-out batch and review the highest risks

Do not evaluate a detector only on the same rows used for fitting. Keep a chronological or asset-aware holdout when possible, then rank the holdout observations for inspection. `predict_proba` is available for some PyOD detector workflows, but a normalized score should not be interpreted as a calibrated failure probability without a separate calibration study.

```python
import numpy as np
from pyod.models.ecod import ECOD

rng = np.random.default_rng(12)
training = rng.normal(loc=[0.0, 10.0], scale=[1.0, 1.5], size=(100, 2))
holdout = np.array(
    [[0.2, 9.8], [-0.4, 11.0], [4.8, 17.0], [-5.0, 3.0]],
    dtype=float,
)

model = ECOD(contamination=0.05)
model.fit(training)
scores = model.decision_function(holdout)
ranking = np.argsort(scores)[::-1]

for index in ranking:
    print(f"row={index}, score={scores[index]:.3f}, features={holdout[index].tolist()}")
```

A ranked list is often more actionable than an arbitrary alarm count. Review the raw waveform or process context for the highest-ranked windows, check whether the event coincides with a mode change or missing-data interval, and record the review outcome. If labels become available after inspection or maintenance, preserve them for a later, time-aware validation set.

## Batch and rolling workflows

PyOD models generally fit on a batch and then score new observations. For a rolling workflow, append only validated observations to a controlled reference window and refit at an explicit cadence; do not silently retrain on every alarm. A retrained model can absorb a slowly developing fault or a sensor-bias shift, which makes historical scores incomparable.

```python
import numpy as np
from pyod.models.iforest import IForest

baseline = np.array(
    [[1.9, 64.0], [2.1, 65.0], [2.0, 66.0], [1.8, 63.5], [2.2, 65.5]],
    dtype=float,
)
new_batch = np.array(
    [[2.0, 64.5], [2.3, 67.0], [3.8, 82.0]],
    dtype=float,
)

model = IForest(contamination=0.20, random_state=3)
model.fit(baseline)
labels = model.predict(new_batch)
scores = model.decision_function(new_batch)

print("labels:", labels.tolist())
print("scores:", np.round(scores, 3).tolist())
```

For time series, remember that a row-wise detector does not understand temporal order, persistence, or causality. Add windowed and lagged features, use a sequential or change-point method when the question is about a sustained shift, and aggregate repeated points into an event with a documented debounce rule. Missing values must be handled before fitting; do not replace a failed sensor with a plausible constant without marking the imputation.

## Validate alarms with operational labels

If reviewed events are available, report a confusion matrix, precision, recall, and the alert rate at the chosen threshold. These metrics depend on the decision threshold and on how positives were defined. A rare-failure dataset can produce a high precision or recall estimate with wide uncertainty, so evaluate across time periods and assets rather than relying on one random split.

```python
import numpy as np
from sklearn.metrics import classification_report
from pyod.models.iforest import IForest

training = np.array([[0.0], [0.1], [-0.2], [0.3], [-0.1], [0.2]], dtype=float)
review_features = np.array([[-0.1], [0.2], [3.5], [4.0]], dtype=float)
review_labels = np.array([0, 0, 1, 1], dtype=int)

model = IForest(contamination=0.25, random_state=4)
model.fit(training)
predicted = model.predict(review_features)
print(classification_report(review_labels, predicted, zero_division=0))
```

Labels should represent a stable operational definition, such as “confirmed bearing defect within the next inspection interval,” rather than an unreviewed alarm. When the business cost of missed failures differs from the cost of inspections, choose thresholds using that cost and the available maintenance capacity, not only the detector's default contamination.

## Safety notes

- These examples are **offline demonstrations only**. They do not read live telemetry, actuate equipment, open a GUI, or issue a control command.
- An outlier is not automatically a fault. It can indicate a real defect, a legitimate operating regime, a sensor problem, a timestamp error, a maintenance activity, or a data-pipeline failure.
- Do not use a PyOD alarm by itself to trip equipment, suppress a protective function, extend an inspection interval, or declare an asset safe. Route alarms through qualified review and the site's approved protection and maintenance process.
- Define the observation window, asset population, operating regimes, missing-data policy, and positive event label before fitting. Keep raw measurements and feature-generation code so every score can be reproduced.
- Fit preprocessing and detectors on a clean, representative baseline. Guard against leakage from future measurements, post-failure data, duplicated windows, and maintenance records that would not be available at prediction time.
- Track model version, PyOD and dependency versions, training period, contamination, feature units, threshold policy, and retraining events. Revalidate after sensor replacement, firmware changes, process changes, or dependency upgrades.
- Keep acquisition, scoring, alerting, and control paths separate. Use read-only or replay data first, enforce access controls, and require a human or independently verified safety system for any physical intervention.

## Next door

Next door: read the [PyOD documentation](https://pyod.readthedocs.io/) and compare detectors on a time-aware, labeled holdout; use [scikit-learn's evaluation tools](https://scikit-learn.org/stable/modules/model_evaluation.html) when you need explicit threshold and metric analysis.

## References

[1]: https://pyod.readthedocs.io/ "PyOD documentation"
[2]: https://pyod.readthedocs.io/en/latest/ "PyOD API and model guide"
[3]: https://pyod.readthedocs.io/en/latest/pyod.models.html "PyOD model implementations"
[4]: https://scikit-learn.org/stable/modules/model_evaluation.html "scikit-learn model evaluation"
[5]: https://pypi.org/project/pyod/ "PyOD on PyPI"

<!-- Sources: [1] [2] [3] [4] [5] -->
