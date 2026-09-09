# 101 — Machine vision with OpenCV

> `opencv-python` brings OpenCV's image-processing and computer-vision toolkit to Python. It is useful for inspection pipelines that capture a frame, isolate useful pixels, measure objects, and hand selected regions to an OCR engine.

## Install

```bash
python -m pip install opencv-python
```

For servers, containers, and other environments without a graphical display, use `opencv-python-headless` instead. Do not install both distributions in one environment because they provide the same `cv2` import. OCR is separate: the OCR example below also needs `pytesseract` and the Tesseract executable.

## Start offline: count marked parts

This first example creates its own image, so it needs no camera, sample file, or GUI display. It thresholds bright circular marks and counts their contours; it prints `marked parts: 3`.

```python
import cv2
import numpy as np

image = np.zeros((240, 320), dtype=np.uint8)
for center in ((70, 80), (160, 120), (250, 70)):
    cv2.circle(image, center, 24, 255, thickness=-1)

_, mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_contours = [contour for contour in contours if cv2.contourArea(contour) > 500]
print(f"marked parts: {len(large_contours)}")
```

In production, validate thresholds across lighting conditions. Filter by area, aspect ratio, circularity, or a known region of interest so dust and reflections do not become false parts.

## Inspect a local image without a window

Use `imread` and `imwrite` for a display-free inspection job. This example assumes `inspection.jpg` exists in the current directory and writes a binary mask without opening a window.

```python
from pathlib import Path

import cv2

source_path = Path("inspection.jpg")
image = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
if image is None:
    raise FileNotFoundError(f"Could not read {source_path.resolve()}")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

output_path = Path("inspection-mask.png")
if not cv2.imwrite(str(output_path), mask):
    raise OSError(f"Could not write {output_path.resolve()}")
print(f"wrote {output_path} with shape {mask.shape}")
```

OpenCV images use BGR channel order by default, not RGB. Convert explicitly before passing an image to a library that expects RGB. Also check every `imread` result because a missing path returns `None`.

## Count connected objects

For binary masks, connected-component analysis returns one label per connected region and measurements such as area and bounding box. The background is label `0`, so start at index `1`.

```python
import cv2
import numpy as np

mask = np.zeros((160, 240), dtype=np.uint8)
cv2.rectangle(mask, (20, 30), (70, 100), 255, thickness=-1)
cv2.rectangle(mask, (100, 45), (145, 115), 255, thickness=-1)
cv2.circle(mask, (195, 75), 25, 255, thickness=-1)

count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
minimum_area = 200
objects = []
for label in range(1, count):
    area = int(stats[label, cv2.CC_STAT_AREA])
    if area >= minimum_area:
        x = int(stats[label, cv2.CC_STAT_LEFT])
        y = int(stats[label, cv2.CC_STAT_TOP])
        width = int(stats[label, cv2.CC_STAT_WIDTH])
        height = int(stats[label, cv2.CC_STAT_HEIGHT])
        objects.append((x, y, width, height, area))

print(f"objects: {len(objects)}")
for object_box in objects:
    print("x, y, width, height, area =", object_box)
```

Use `connectivity=8` when diagonally touching pixels should belong to the same object. If parts touch, connected components cannot separate them by themselves; consider watershed segmentation or a trained detector.

## Read a label with OCR

OpenCV prepares a crop; an OCR engine interprets its characters. This snippet expects `label.png`, needs the Python wrapper plus a system Tesseract installation, and runs without a GUI.

```bash
python -m pip install pytesseract
```

```python
from pathlib import Path

import cv2
import pytesseract

label_path = Path("label.png")
label = cv2.imread(str(label_path), cv2.IMREAD_GRAYSCALE)
if label is None:
    raise FileNotFoundError(f"Could not read {label_path.resolve()}")

scaled = cv2.resize(label, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
_, prepared = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
text = pytesseract.image_to_string(prepared, config="--psm 7")
print("label:", " ".join(text.split()))
```

OCR quality depends on focus, contrast, character spacing, and page-segmentation mode. Crop tightly, enlarge small text, and validate the returned string against an expected format before using it in a control decision. `pytesseract` does not install Tesseract or its language data.

## Optional live camera capture

A USB camera is not required for the examples above. When one is available, `VideoCapture(0)` usually selects the first camera, but device numbering and backend support vary by operating system. This **live-device example** writes one frame to disk instead of calling `imshow`, so it does not require a GUI display.

```python
from pathlib import Path

import cv2

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    raise RuntimeError("Could not open camera 0")

output_path = Path("camera-frame.jpg")
try:
    ok, frame = capture.read()
    if not ok:
        raise RuntimeError("Camera opened, but no frame was received")
    if not cv2.imwrite(str(output_path), frame):
        raise OSError(f"Could not write {output_path.resolve()}")
    print(f"saved {output_path} with shape {frame.shape}")
finally:
    capture.release()
```

Camera access may require OS permissions and a compatible V4L2, DirectShow, or Media Foundation backend. In a desktop session, `cv2.imshow` requires GUI support and a regular `waitKey` call; use the headless package and file output in services or containers.

## Safety notes

Treat every image as untrusted input. Limit image dimensions and memory use for files from users or network shares, and reject unreadable or unexpectedly large inputs. Never let an OCR result, object count, or camera failure directly actuate machinery without bounds checking, a known-good fallback, and an independent interlock. Test inspection thresholds across lighting, focus, motion blur, lens contamination, and missing or duplicated parts. Camera frames can contain people or identifying labels, so restrict access, retention, and logging to what the inspection requires.

## Next door

Next door: use [pytesseract](https://pypi.org/project/pytesseract/) for the OCR bridge, or pair OpenCV with [NumPy](059-numpy.md) for array-level image measurements.

### References

[1]: https://pypi.org/project/opencv-python/ "opencv-python on PyPI"
[2]: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html "OpenCV-Python Tutorials"
[3]: https://pypi.org/project/pytesseract/ "pytesseract on PyPI"

OpenCV package availability and the GUI/headless distinction are documented by the [opencv-python project][1]. The image-processing APIs used here are covered by the [OpenCV-Python tutorials][2], and the OCR wrapper is documented on [pytesseract][3].
