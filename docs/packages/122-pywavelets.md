# 104 — Wavelet analysis with PyWavelets

> `PyWavelets` provides discrete, continuous, and wavelet-packet transforms for multiresolution analysis. It is useful for vibration and acoustic signals whose short-lived impacts, transients, and changing frequency content are difficult to summarize with one global Fourier spectrum.

## Install

```bash
python -m pip install PyWavelets
```

The import name is `pywt`, while the package name on PyPI is `PyWavelets`. The examples below are local, deterministic demonstrations: they generate signals in memory, print numerical results, and do not require a sensor, audio interface, proprietary hardware, network connection, or GUI display. PyWavelets depends on NumPy; binary-wheel availability can vary by Python version and operating system, so pin and test the complete environment used for production analysis.

## Start offline: detect a vibration impact with a discrete wavelet transform

A discrete wavelet transform (DWT) separates a finite signal into approximation and detail coefficients at several scales. The detail bands are useful for locating an impulsive bearing or gear event. This example creates a noisy sinusoid with one synthetic impact, reconstructs the finest detail band, and reports the largest detail peak.

```python
import numpy as np
import pywt

sample_rate = 2_000.0
sample_count = 4_000
time = np.arange(sample_count) / sample_rate
rng = np.random.default_rng(12)

signal = 0.25 * np.sin(2 * np.pi * 120.0 * time)
signal += 0.04 * rng.standard_normal(sample_count)
impact_index = 2_400
signal[impact_index : impact_index + 10] += np.hanning(10) * 2.5

wavelet = pywt.Wavelet("db4")
level = 4
coefficients = pywt.wavedec(signal, wavelet, level=level, mode="symmetric")
detail_only = [np.zeros_like(coefficients[0])] + [
    np.zeros_like(detail) if index != len(coefficients) - 1 else detail
    for index, detail in enumerate(coefficients[1:], start=1)
]
finest_detail = pywt.waverec(detail_only, wavelet, mode="symmetric")[:sample_count]
peak_index = int(np.argmax(np.abs(finest_detail)))

print(f"impact sample: {impact_index}")
print(f"largest finest-detail sample: {peak_index}")
print(f"peak time: {peak_index / sample_rate:.4f} s")
```

The coefficient order returned by `wavedec` is `[cA_n, cD_n, ..., cD_1]`, so `cD_1` is the finest detail band. Boundary extension and reconstruction can make the reconstructed array slightly longer than the input; trim it to the original sample count before comparing sample positions. For a real machine, choose the sampling rate, wavelet family, level, and event threshold using labeled baseline data rather than treating `db4` or a single peak as universal settings.

## Denoise an acoustic or vibration waveform

Wavelet thresholding can reduce broadband noise while retaining localized structure. `pywt.threshold` applies a coefficient-wise rule; the following display-free example estimates noise from the finest detail coefficients, applies a soft threshold to detail bands, and prints the improvement in signal-to-noise ratio against a known synthetic reference.

```python
import numpy as np
import pywt

sample_rate = 8_000.0
time = np.arange(int(sample_rate)) / sample_rate
rng = np.random.default_rng(4)
clean = 0.6 * np.sin(2 * np.pi * 440.0 * time)
clean += 0.25 * np.sin(2 * np.pi * 1_200.0 * time)
clean[3_000:3_030] += 1.2 * np.hanning(30)
noisy = clean + 0.18 * rng.standard_normal(clean.size)

wavelet = "sym5"
level = 5
coefficients = pywt.wavedec(noisy, wavelet, level=level, mode="symmetric")
finest_detail = coefficients[-1]
noise_sigma = np.median(np.abs(finest_detail)) / 0.6745
threshold = noise_sigma * np.sqrt(2.0 * np.log(noisy.size))
filtered = [coefficients[0]] + [
    pywt.threshold(detail, threshold, mode="soft")
    for detail in coefficients[1:]
]
denosed = pywt.waverec(filtered, wavelet, mode="symmetric")[: noisy.size]

snr_noisy = 10.0 * np.log10(np.mean(clean**2) / np.mean((noisy - clean) ** 2))
snr_denoised = 10.0 * np.log10(np.mean(clean**2) / np.mean((denoised - clean) ** 2))
print(f"threshold: {threshold:.4f}")
print(f"noisy SNR: {snr_noisy:.2f} dB")
print(f"denoised SNR: {snr_denoised:.2f} dB")
```

This universal-threshold recipe is a starting point, not a guarantee of better fault sensitivity. Validate it against waveforms containing the impulses, harmonics, and modulation patterns that matter to the application. Excessive thresholding can erase a weak defect signature, while insufficient thresholding can preserve false alarms.

## Track changing frequency content with a continuous wavelet transform

A continuous wavelet transform (CWT) evaluates a signal over a dense set of scales and is useful for acoustic chirps, run-ups, and other nonstationary events. `pywt.scale2frequency` converts scales to approximate pseudo-frequencies for a chosen wavelet. The example uses the complex Morlet wavelet and reports the strongest scale in each time window; it does not plot or open a display.

```python
import numpy as np
import pywt

sample_rate = 4_000.0
time = np.arange(4_000) / sample_rate
frequency = 180.0 + 420.0 * time / time[-1]
signal = np.sin(2.0 * np.pi * (180.0 * time + 210.0 * time**2 / time[-1]))
signal += 0.15 * np.sin(2.0 * np.pi * 60.0 * time)

scales = np.arange(2, 128)
coefficients, frequencies = pywt.cwt(
    signal,
    scales,
    "cmor1.5-1.0",
    sampling_period=1.0 / sample_rate,
)
power = np.abs(coefficients) ** 2
window = slice(500, 3_500)
strongest_scale_index = np.argmax(power[:, window], axis=0)
representative_index = strongest_scale_index[len(strongest_scale_index) // 2]
print(f"representative dominant frequency: {frequencies[representative_index]:.1f} Hz")
print(f"frequency range covered: {frequencies.min():.1f}–{frequencies.max():.1f} Hz")
```

Scale-to-frequency mapping depends on the mother wavelet, sampling period, and boundary effects. The CWT produces a redundant representation, so it is usually more expensive than a DWT. Do not interpret high power at the first and last portions of a record without checking the cone-of-influence or equivalent edge reliability; pad or discard edge regions according to a documented rule.

## Build band-energy features for condition monitoring

For a compact monitoring feature, calculate energy in selected DWT detail bands and retain the acquisition context. `pywt.dwt_max_level` prevents requesting more levels than the signal length and filter support can support. The example creates a short vibration window and returns log-scaled detail energies.

```python
import numpy as np
import pywt

sample_rate = 2_048.0
rng = np.random.default_rng(9)
window = 0.3 * rng.standard_normal(1_024)
window += 1.5 * np.sin(2.0 * np.pi * 256.0 * np.arange(1_024) / sample_rate)

wavelet = pywt.Wavelet("coif3")
level = min(4, pywt.dwt_max_level(window.size, wavelet.dec_len))
coefficients = pywt.wavedec(window, wavelet, level=level, mode="periodization")
energies = {
    f"detail_{detail_level}": float(np.mean(detail**2))
    for detail_level, detail in zip(range(level, 0, -1), coefficients[1:])
}
log_energies = {name: round(10.0 * np.log10(value + 1e-12), 2) for name, value in energies.items()}
print("wavelet level:", level)
print("detail energies (dB):", log_energies)
```

A DWT band is only approximately associated with a frequency interval because the effective response depends on the wavelet filters, extension mode, sampling rate, and level. Keep the raw window, timestamp, sensor location, speed, load, and preprocessing parameters with each feature row. A feature shift can reflect a changed operating regime, sensor mounting, or acquisition chain rather than an equipment fault.

## Safety notes

- These examples are **offline demonstrations only**. They do not read live telemetry, actuate equipment, open a GUI, or issue an audio or control command.
- A wavelet coefficient, energy feature, or reconstructed waveform is an analysis result, not a diagnosis. Confirm suspected faults with time-domain review, operating context, other sensors, and an approved maintenance process.
- Do not use a PyWavelets threshold or alarm by itself to trip machinery, suppress a protective function, or declare an asset safe. Keep protection and shutdown logic independent from exploratory signal analysis.
- Verify sample rate, units, anti-alias filtering, sensor mounting, channel polarity, timestamps, missing samples, and clipping before comparing features. Resampling or a changed acquisition backend can move apparent bands and thresholds.
- Treat boundary coefficients and short records carefully. Document the wavelet family, level, extension mode, threshold rule, CWT scales, and edge-discard policy so results remain reproducible after upgrades.
- Limit input duration and array sizes when processing untrusted files, and reject NaN, infinite, clipped, or malformed data before transform calls. Preserve raw recordings under appropriate access and retention controls, especially for speech or other identifying acoustic content.
- Live acquisition is hardware- and platform-dependent. Test device drivers, permissions, clock synchronization, and buffer behavior separately from the PyWavelets analysis, and use a fail-safe, independently validated path for any physical response.

## Next door

Next door: pair PyWavelets with [SciPy's signal tools](https://docs.scipy.org/doc/scipy/reference/signal.html) for filtering and resampling, then validate wavelet-derived features on labeled, time-aware vibration data before deploying them in a monitoring pipeline.

## References

[1]: https://pywavelets.readthedocs.io/en/latest/ "PyWavelets documentation"
[2]: https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html "PyWavelets discrete wavelet transform reference"
[3]: https://pywavelets.readthedocs.io/en/latest/ref/cwt.html "PyWavelets continuous wavelet transform reference"
[4]: https://pywavelets.readthedocs.io/en/latest/ref/thresholding-functions.html "PyWavelets thresholding functions reference"
[5]: https://pypi.org/project/PyWavelets/ "PyWavelets on PyPI"

PyWavelets documents the DWT, CWT, thresholding, coefficient ordering, scale conversion, and installation details in its [reference documentation][1] [2] [3] [4] and [PyPI project page][5].

<!-- Sources: [1] [2] [3] [4] [5] -->
