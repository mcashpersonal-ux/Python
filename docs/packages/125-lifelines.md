# 107 — Survival analysis with lifelines

> `lifelines` is a pure-Python survival-analysis library for estimating time-to-event distributions, handling right-censored observations, comparing groups, and fitting regression models. For equipment reliability, it turns incomplete failure histories into survival probabilities, hazard estimates, and defensible MTBF or warranty-life forecasts.

## Install

```bash
python -m pip install lifelines
```

The current PyPI release is distributed as a platform-independent wheel and requires Python 3.11 or newer. The core examples below are local and do not need a device, network connection, database, or GUI display. Install `matplotlib` separately only when you want to render plots; the numerical fitters work without a display backend.

## First example: offline equipment failure history

A survival record has a **duration** and an event indicator. Here, `1` means the unit failed during observation and `0` means it was still operating when observation stopped, so its exact failure time is **right-censored**. This small example is deterministic and safe to run on a laptop or in CI.

```python
from lifelines import KaplanMeierFitter, WeibullFitter

# Operating hours for eight identical test units.
durations = [120, 180, 210, 260, 310, 360, 420, 500]
failed = [1, 1, 0, 1, 1, 0, 1, 0]

km = KaplanMeierFitter().fit(durations, event_observed=failed, label="field units")
weibull = WeibullFitter().fit(durations, event_observed=failed, label="Weibull")

print(f"KM median survival: {km.median_survival_time_:.1f} hours")
print(f"Weibull scale (63.2% failed): {weibull.lambda_:.1f} hours")
print(f"Weibull shape: {weibull.rho_:.2f}")
print(f"Survival at 300 h: {float(km.predict(300)):.3f}")
```

`KaplanMeierFitter` is non-parametric: it estimates the survival step function without choosing a distribution. `WeibullFitter` imposes a Weibull shape, which is useful for a compact reliability model. In a Weibull fit, `lambda_` is the time at which the model estimates 63.2% of units have failed, while `rho_` describes the hazard trend: values above one indicate increasing failure risk, and values below one indicate decreasing risk.

## Model MTBF and reliability targets

For a complete, uncensored sample, the arithmetic average of failure hours is a simple estimate of mean time between failures (MTBF). With censored field observations, an ordinary average is biased downward because it discards the information that surviving units lasted at least as long as their observed duration. Fit a survival model instead, then report the assumptions and uncertainty with the estimate.

A two-parameter Weibull model has a finite mean when its fitted parameters are positive. The following snippet derives the model mean from `lambda_` and `rho_`, and also reports a percentile useful for warranty planning. It is self-contained and does not create a plot.

```python
import math
from lifelines import WeibullFitter

hours = [120, 180, 210, 260, 310, 360, 420, 500]
failed = [1, 1, 0, 1, 1, 0, 1, 0]

model = WeibullFitter().fit(hours, event_observed=failed)
model_mean = model.lambda_ * math.gamma(1.0 + 1.0 / model.rho_)
reliability_90_hours = model.percentile(0.90)

print(f"Model-based mean lifetime: {model_mean:.1f} hours")
print(f"Time with 90% survival: {reliability_90_hours:.1f} hours")
print(model.summary[["coef", "se(coef)"]])
```

The model-based mean is a **mean lifetime under the fitted Weibull distribution**, not a guarantee that a repairable fleet will run that many hours between service calls. For repairable assets, define the observation unit carefully: use time between completed repairs for MTBF, and do not mix planned preventive-maintenance removals with random failures unless the analysis explicitly models them.

## Compare equipment populations

Use separate Kaplan–Meier curves when comparing, for example, two bearing suppliers or two firmware versions. The example below performs a log-rank test and prints the estimated survival at 300 hours. It remains offline and uses only in-memory observations.

```python
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

vendor_a_hours = [120, 180, 210, 260, 310, 360]
vendor_a_failed = [1, 1, 0, 1, 1, 0]
vendor_b_hours = [160, 240, 330, 390, 450, 520]
vendor_b_failed = [1, 0, 1, 0, 1, 0]

km_a = KaplanMeierFitter().fit(vendor_a_hours, vendor_a_failed, label="vendor A")
km_b = KaplanMeierFitter().fit(vendor_b_hours, vendor_b_failed, label="vendor B")
test = logrank_test(
    vendor_a_hours,
    vendor_b_hours,
    event_observed_A=vendor_a_failed,
    event_observed_B=vendor_b_failed,
)

print(f"Vendor A survival at 300 h: {float(km_a.predict(300)):.3f}")
print(f"Vendor B survival at 300 h: {float(km_b.predict(300)):.3f}")
print(f"Log-rank p-value: {test.p_value:.4f}")
```

A small p-value is evidence that the observed survival curves differ under the test assumptions; it is not proof that one component caused the difference. Check exposure, censoring rules, operating conditions, and sample size before changing a bill of materials.

## Add operating conditions with Cox regression

When each unit has covariates such as average temperature, load class, or supplier, use `CoxPHFitter`. The duration and event columns must be in the same pandas `DataFrame` as the predictors. Coefficients are log hazard ratios: a positive coefficient means higher instantaneous failure hazard, conditional on surviving to that time.

```python
import pandas as pd
from lifelines import CoxPHFitter

records = pd.DataFrame(
    {
        "hours": [120, 180, 210, 260, 310, 360, 420, 500],
        "failed": [1, 1, 0, 1, 1, 0, 1, 0],
        "temperature_c": [70, 75, 80, 82, 85, 88, 90, 92],
        "high_load": [0, 0, 0, 1, 1, 1, 1, 1],
    }
)

cox = CoxPHFitter().fit(records, duration_col="hours", event_col="failed")
print(cox.summary[["coef", "exp(coef)", "p"]])
print(cox.predict_survival_function(records.iloc[[0]], times=[300]))
```

Check proportional-hazards assumptions with `cox.check_assumptions(records, p_value_threshold=0.05)` on a suitably sized dataset. If temperature changes over time, a single row per unit may be inadequate; use lifelines' time-varying Cox format and document the measurement interval.

## Prepare field data and censoring correctly

Keep the event definition stable. A unit removed for preventive maintenance, a unit still operating at the end of the study, and a unit lost because its sensor stopped reporting are not automatically equivalent. Store the reason for every removal, then map only defensible right-censored cases to `event_observed=0`.

For timestamp-based records, convert start and end times to durations with the library utility. Missing end times represent censoring in this example; `freq="h"` makes the duration unit hours.

```python
from lifelines.utils import datetimes_to_durations

start_times = ["2025-01-01 08:00", "2025-01-03 08:00", "2025-01-05 08:00"]
end_times = ["2025-01-02 08:00", None, "2025-01-08 20:00"]

durations, observed = datetimes_to_durations(
    start_times,
    end_times,
    freq="h",
    dayfirst=False,
)
print("hours:", durations)
print("failure observed:", observed)
```

Use consistent timezone handling before conversion. Do not silently treat a missing telemetry interval as proof that a component survived; distinguish an operational censoring event from missing data and investigate the data-collection process.

## Optional plots without assuming a GUI

The fitter methods expose tables such as `survival_function_`, `confidence_interval_`, `hazard_`, and `cumulative_hazard_`. If you need a file rather than an interactive window, use a non-interactive Matplotlib backend before importing `pyplot`.

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

hours = [120, 180, 210, 260, 310, 360, 420, 500]
failed = [1, 1, 0, 1, 1, 0, 1, 0]

km = KaplanMeierFitter().fit(hours, failed, label="test fleet")
axis = km.plot_survival_function()
axis.set(xlabel="Operating hours", ylabel="Probability of surviving")
axis.figure.savefig("survival_curve.png", dpi=150, bbox_inches="tight")
plt.close(axis.figure)
print("wrote survival_curve.png")
```

## Safety notes

- Treat survival and MTBF outputs as statistical estimates, not safety claims or guaranteed service intervals. Validate the model against the applicable reliability, functional-safety, and maintenance requirements.
- Do not use a fitted curve to extend inspection intervals, disable protections, or defer a required replacement without engineering review and a documented change process.
- Define failure, censoring, exposure, and repair events before collecting data. Mixing planned removals, unplanned failures, and missing telemetry can produce a precise-looking but misleading result.
- Preserve raw timestamps, device identity, operating conditions, and censoring reasons. Protect the data from silent unit changes, clock errors, duplicate events, and survivorship bias.
- Compare confidence intervals and practical effect sizes, not only p-values. A non-significant result does not demonstrate equal reliability, especially for small samples or heavily censored fleets.
- Test proportional-hazards and distributional assumptions. Use a non-parametric Kaplan–Meier estimate as a diagnostic baseline before relying on a Weibull or Cox extrapolation beyond observed follow-up.
- For live-device ingestion, keep acquisition and control paths separate. This page's examples read only local, static data; they do not connect to a PLC, sensor, historian, or maintenance system.

## Next door

For a broader reliability workflow, pair [lifelines' survival-regression guide](https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html) with a controlled pandas data-preparation step; use [scipy](https://docs.scipy.org/doc/scipy/) when you need lower-level probability distributions or hypothesis tests.

## References

[1]: https://lifelines.readthedocs.io/en/latest/ "lifelines documentation"
[2]: https://lifelines.readthedocs.io/en/latest/Quickstart.html "lifelines Quickstart"
[3]: https://lifelines.readthedocs.io/en/latest/fitters/univariate/WeibullFitter.html "lifelines WeibullFitter API"
[4]: https://pypi.org/project/lifelines/ "lifelines on PyPI"
[5]: https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html "lifelines survival regression"

<!-- Sources: [1] [2] [3] [4] [5] -->

[6]: https://docs.scipy.org/doc/scipy/ "SciPy documentation"

<!-- Source links: [6] -->
