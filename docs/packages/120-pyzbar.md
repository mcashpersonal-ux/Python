# 102 — Barcode and QR reading with pyzbar

> `pyzbar` is a Python wrapper around the ZBar barcode reader. It decodes one-dimensional barcodes and QR codes from images, returning the payload, symbology, bounding rectangle, polygon, orientation, and a relative quality value that can be recorded alongside a line scan.

## Install

```bash
python -m pip install pyzbar pillow
```

`pyzbar` is the Python wrapper; the decoder itself is the native ZBar library. Windows wheels include the required ZBar DLLs. On Linux, install the system library when it is not already present, for example `sudo apt-get install libzbar0`; on macOS, `brew install zbar` is the usual route. The exact package name and availability depend on the operating system and CPU architecture. `opencv-python` is optional when frames already arrive as NumPy arrays.

## Start offline: decode a traceable QR fixture

This first example is **local and demo-safe**. It creates an in-memory PNG from a bundled fixture, opens it with Pillow, and decodes it without a camera, network connection, GUI display, or proprietary hardware. The payload is deliberately structured like a line traceability record.

```python
import base64
from io import BytesIO

from PIL import Image
from pyzbar.pyzbar import decode

png_base64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAUoAAAFKAQAAAABTUiuoAAAB70lEQVR4nO2aTYrjMBBGX40MWco3sm/WZ5ob2EfpAwzYywabrxeSHCf0gDPgWDBVC0Eqb/FBUT8q2cRBG38dJcFRRx111FFHz0QtW7P5V4O5uPvTBTj6CtpJkiYwswbrkzdIkvSIniPA0VfQOaeQhvhlMN9SjPb5Vo1WR+82N2gArL9IgKN/tebpt3VTC7CamN8hwNF/iFYUMIPGNiyMfXbv786Xa3WU/RxBEN10P4q7k6Thcq2OpmjtbIgS2zi4/+NyrY7m+1Y/N+kAVtMQF/IfrPYGAY4es10l7LSkcRAI0kBIdzCvhLWgJVpxQZpCLoJDVGleWjxa1aB5Jux+32TEBYh/DOLaQPwyQfBdRjVonjIGIB9xIRXBgYcZxHPrenQfLWkh18S0NgxKPq+EVaH2MQUx2k2leeXNk+8Jq0J3uUVXpsNSGIN2qea5dT2aZ8Jt"
    "g5HHwcep3qNVCfq8y8jeLWTdhPetytD723GuiZ9mMDcwtm8R4Ogr6PZ2DATlGMWlHOcLcPQVtLwdW89qaTAczewn9BwBjh6w59dIwdqkSRDAfJdRM2rWBjG2q6Wj+9w+qqlO6/+Hlgn+YXlx32D4fatGdDQzsxasn2+yniCYc9+y/nwBjh6x1Lfun18IcstScXvfctRRRx11tBr0G81QcGnYjqNcAAAAAElFTkSuQmCC"
)

image = Image.open(BytesIO(base64.b64decode(png_base64)))
results = decode(image)
if len(results) != 1:
    raise RuntimeError(f"expected one code, found {len(results)}")

result = results[0]
print("payload:", result.data.decode("utf-8"))
print("type:", result.type)
print("rect:", result.rect)
print("quality:", result.quality)
```

The output payload is `line-07|part-042|rev-A`. `data` is bytes, so decode it with the expected character encoding before parsing fields. Keep the original bytes in an audit record when exact reproduction matters.

## Decode a local image and keep geometry

For a file-based inspection job, pass a Pillow image directly to `decode`. The returned `rect` is a convenient bounding box, while `polygon` preserves the detected corners. Geometry is useful for checking whether a label was inside the expected region of interest rather than merely present somewhere in the frame.

```python
from pathlib import Path

from PIL import Image
from pyzbar.pyzbar import decode

image_path = Path("line-scan.png")
if not image_path.is_file():
    raise FileNotFoundError(f"missing input image: {image_path.resolve()}")

with Image.open(image_path) as image:
    results = decode(image)

for result in results:
    payload = result.data.decode("utf-8", errors="replace")
    print(
        f"type={result.type} payload={payload!r} "
        f"left={result.rect.left} top={result.rect.top} "
        f"width={result.rect.width} height={result.rect.height} "
        f"quality={result.quality} orientation={result.orientation}"
    )
```

A missing result is not proof that a label is absent. Blur, glare, low contrast, a clipped quiet zone, skew, insufficient resolution, or an unsupported symbology can all cause a scan to fail. Save the source frame or a bounded evidence crop when a traceability decision must be investigated later.

## Restrict the symbology and validate the payload

By default, `decode` searches all symbol types supported by the installed ZBar backend. Restricting the search can reduce accidental matches when a station expects one known format. The parser below validates a simple traceability payload before it enters a production record.

```python
import re

from PIL import Image
from pyzbar.pyzbar import ZBarSymbol, decode

image = Image.open("label.png")
results = decode(image, symbols=[ZBarSymbol.QRCODE, ZBarSymbol.CODE128])
pattern = re.compile(r"^line-(?P<line>[0-9]{2})\|part-(?P<part>[A-Za-z0-9-]+)\|rev-(?P<revision>[A-Z0-9]+)$")

for result in results:
    text = result.data.decode("ascii", errors="strict")
    match = pattern.fullmatch(text)
    if match is None:
        print(f"rejected unexpected payload from {result.type}: {text!r}")
        continue
    record = {
        "symbology": result.type,
        "line": match.group("line"),
        "part": match.group("part"),
        "revision": match.group("revision"),
        "quality": result.quality,
        "rect": result.rect,
    }
    print(record)
```

Do not use `quality` as a universal pass/fail threshold. ZBar documents it as an unscaled relative quantity whose exact definition is application-dependent. Establish thresholds with representative labels, lighting, focus, speed, and the particular backend used at the station.

## Scan a grayscale line buffer

A camera or vision system may provide an 8-bit grayscale buffer rather than a Pillow image. `pyzbar` accepts a tuple of `(pixels, width, height)` for an 8-bits-per-pixel image. This is useful at a line-scanning boundary because the image dimensions and the exact byte buffer can be logged with the decoded result.

```python
from pyzbar.pyzbar import decode

width, height = 640, 480
pixels = bytes(width * height)  # Demo buffer only; a live scanner supplies real grayscale bytes.
results = decode((pixels, width, height))

if not results:
    print("no barcode found in this demo buffer")
else:
    for result in results:
        print(result.type, result.data, result.rect)
```

The all-zero buffer intentionally produces no detection and requires no display. A real acquisition adapter must guarantee that `len(pixels) == width * height`, that each sample is one byte, and that the row order and dimensions match what the decoder receives. Passing a 24-bit RGB byte buffer as though it were 8-bit grayscale raises an unsupported-bits-per-pixel error or produces invalid interpretation.

## Use an OpenCV frame without a GUI

When an upstream vision pipeline already has an OpenCV frame, pass its NumPy array to `decode`. This **display-free example** assumes `camera-frame.png` exists and does not call `imshow`; it therefore works in a service or container once the image and native ZBar library are available.

```python
from pathlib import Path

import cv2
from pyzbar.pyzbar import decode

image_path = Path("camera-frame.png")
frame = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
if frame is None:
    raise FileNotFoundError(f"could not read {image_path.resolve()}")

for result in decode(frame):
    print(result.type, result.data.decode("utf-8", errors="replace"), result.rect)
```

If the whole frame is expensive or contains unrelated labels, crop a bounded region of interest before decoding and translate the returned coordinates back to full-frame coordinates by adding the crop origin. Keep the crop dimensions limited when images can come from untrusted uploads.

## Live camera integration boundary

A USB camera is optional. If one is available, capture frames with the camera library selected for the deployment, call `decode` on each accepted frame, and release the device on shutdown. The following is a **live-device example**: it requires camera permissions and a working OpenCV backend, but still avoids a GUI display.

```python
import cv2
from pyzbar.pyzbar import decode

capture = cv2.VideoCapture(0)
if not capture.isOpened():
    raise RuntimeError("could not open camera 0")

try:
    ok, frame = capture.read()
    if not ok:
        raise RuntimeError("camera opened, but no frame was received")
    for result in decode(frame):
        print(result.type, result.data.decode("utf-8", errors="replace"), result.rect)
finally:
    capture.release()
```

Camera numbering and backend support vary across Linux, Windows, and macOS. Do not assume that camera index `0`, exposure, focus, resolution, or frame timing is stable. For a conveyor or line scanner, timestamp the source frame, station identity, trigger or encoder position, and decoder result together so a later record can be traced to the physical scan.

## Safety notes

- **The first example is offline only.** Do not connect a copied camera example to a production line until device permissions, acquisition settings, retention, and failure behavior have been reviewed.
- Treat decoded bytes, symbology, coordinates, orientation, and quality as untrusted input. Validate encoding, length, syntax, station identity, and an allow-listed part or revision before creating a traceability record.
- A failed decode, a duplicate decode, or multiple competing codes must be an explicit station state. Never convert “no result” into an assumed part identity, and never actuate machinery from a barcode result without independent interlocks and operator-approved fallback behavior.
- Check the complete image path, including quiet zone, focus, motion blur, glare, label contrast, skew, field of view, trigger timing, and line speed. Test both readable and deliberately damaged labels.
- `pyzbar` depends on the native ZBar shared library. Pin and test the Python package, ZBar backend, operating system, and architecture together; platform packages may differ in symbology and orientation support. On Windows, a missing Visual C++ runtime can also prevent import.
- Images and payloads may contain personal, product, or supply-chain information. Restrict access, logging, and retention to the traceability requirement.

## Next door

Next door: pair `pyzbar` with [OpenCV](119-opencv-python.md) for camera and region-of-interest preparation, then store decoded payloads with a timestamped historian record.

## References

[1]: https://pypi.org/project/pyzbar/ "pyzbar on PyPI"
[2]: https://github.com/NaturalHistoryMuseum/pyzbar "pyzbar source repository and README"
[3]: https://zbar.sourceforge.net/ "ZBar barcode reader"

The wrapper API, accepted image forms, native-library installation notes, and backend differences are documented by the [pyzbar project][1] and its [source repository][2]. Supported symbologies and the native reader's role are described by [ZBar][3].

Caveat: the embedded fixture is only a documentation test image. Production acceptance criteria must be calibrated against the actual camera, optics, labels, motion, and installed ZBar backend.
