# 103 — Barcode generation with python-barcode

> `python-barcode` creates standard one-dimensional barcodes such as Code 128 and EAN-13 from Python. It can write dependency-free SVG labels or raster images through Pillow, making it useful for printing traceability labels and serial identifiers without talking to a scanner or printer directly.

## Install

```bash
python -m pip install python-barcode
# Add Pillow only when raster output is required:
python -m pip install "python-barcode[images]"
```

SVG generation has no external runtime dependency. The `images` extra installs Pillow for PNG, JPEG, and other raster formats; the available formats and font behavior then depend on the installed Pillow version and platform.

## Start offline: create a serial-label SVG

This first example is **local and demo-safe**. It writes an SVG file in the current directory and does not require a printer, camera, network connection, GUI display, or proprietary hardware. Code 128 is a practical choice for alphanumeric serial identifiers, and the library calculates any format-specific checksum automatically.

```python
from pathlib import Path

from barcode import Code128
from barcode.writer import SVGWriter

serial = "LINE07-PART042-000123"
output_path = Path("traceability_label.svg")

barcode = Code128(serial, writer=SVGWriter())
barcode.write(
    output_path.open("wb"),
    options={
        "module_width": 0.25,
        "module_height": 18.0,
        "quiet_zone": 6.5,
        "font_size": 10,
    },
)
print(f"wrote {output_path.resolve()} for serial {serial}")
```

For production code, prefer a context manager so the output file is closed even if rendering fails:

```python
from pathlib import Path

from barcode import Code128
from barcode.writer import SVGWriter

serial = "LOT-2026-09-09-0001"
output_path = Path("lot_2026_09_09_0001.svg")

with output_path.open("wb") as label_file:
    Code128(serial, writer=SVGWriter()).write(label_file)

print(output_path)
```

SVG is vector output, so it scales cleanly for a label layout or a print pipeline. Keep the human-readable serial text under the bars unless the surrounding label already carries an independently verified identifier.

## Generate a batch of traceability labels

A batch job can derive deterministic filenames from a validated serial list. This example remains offline and writes one SVG per identifier.

```python
from pathlib import Path

from barcode import Code128
from barcode.writer import SVGWriter

serials = ["LINE07-PART042-000123", "LINE07-PART042-000124"]
output_dir = Path("labels")
output_dir.mkdir(exist_ok=True)

for serial in serials:
    safe_name = serial.replace("/", "_")
    output_path = output_dir / f"{safe_name}.svg"
    with output_path.open("wb") as label_file:
        Code128(serial, writer=SVGWriter()).write(label_file)
    print(f"created {output_path}")
```

Use an allow-listed filename or a generated database key rather than placing arbitrary upstream text directly in a path. A serial should be unique according to the system of record, not merely unique within one process invocation.

## Add a GS1-128-style application identifier

When downstream systems expect structured fields, keep the encoded payload explicit. `GS1_128` is available for GS1-128 data, while the exact application-identifier rules belong to the organization’s GS1 specification and label contract. Do not treat a visually plausible barcode as proof that a payload is standards-compliant.

```python
from barcode import Code128
from barcode.writer import SVGWriter

serial = "01" + "09506000134352" + "21" + "ABC123456"
barcode = Code128(serial, writer=SVGWriter())

with open("product_serial_gs1_payload.svg", "wb") as label_file:
    barcode.write(label_file)

print(f"encoded payload: {serial}")
```

For a real GS1 deployment, use the barcode class and data formatting required by the trading-partner specification, including fixed lengths, separators for variable-length fields, and any mandated human-readable text. Test the printed result with the same scanner family used at receiving or the production line.

## Export a PNG when the print pipeline needs raster input

Use `ImageWriter` only when the receiving application requires a raster image. This example is **display-free** and writes a PNG; it does not open a window or send anything to a printer.

```python
from pathlib import Path

from barcode import Code128
from barcode.writer import ImageWriter

serial = "ASSET-000042"
output_path = Path("asset_000042.png")

with output_path.open("wb") as image_file:
    Code128(serial, writer=ImageWriter()).write(
        image_file,
        options={"dpi": 300, "module_height": 18.0, "quiet_zone": 6.5},
    )

print(f"wrote {output_path.resolve()}")
```

Pillow controls the raster formats supported by `ImageWriter`; PNG is generally a safer interchange format than JPEG because lossy compression can damage narrow bars and quiet zones. DPI, module width, printer resolution, and the final physical size must be checked together.

## Save compressed SVG for a web or archive boundary

`SVGWriter` can emit SVGZ when a consumer explicitly supports compressed SVG. Keep ordinary `.svg` for the broadest compatibility.

```python
from barcode import Code128
from barcode.writer import SVGWriter

barcode = Code128("SERIAL-0007", writer=SVGWriter())
filename = barcode.save("serial_0007", options={"compress": True})
print(filename)
```

`save()` appends the writer’s extension, so this creates `serial_0007.svgz`. Do not rename a compressed file to `.svg`; consumers use the extension and content type to decide how to decode it.

## Validate before rendering

`python-barcode` validates the barcode format, but application-level validation is still your responsibility. Reject control characters, unexpected length, duplicate serials, and characters outside the label contract before rendering. For traceability, persist the exact encoded payload, format, rendered filename, creation time, and the revision of the label template.

```python
import re

serial = "LINE07-PART042-000123"
if re.fullmatch(r"[A-Z0-9-]{1,32}", serial) is None:
    raise ValueError("serial contains unsupported characters or length")

print(f"validated serial: {serial}")
```

## Safety notes

- The examples generate files only. A generated SVG or PNG is not a printer command and does not confirm that a label was printed, applied, or successfully scanned.
- Validate and allow-list serial contents before encoding. Treat source values as untrusted data; never encode secrets, credentials, or personal data merely because they fit a barcode format.
- Preserve the exact payload and format alongside the label artifact. Handle duplicate serials, missing records, and regeneration as explicit workflow states rather than silently overwriting an existing label.
- Protect the quiet zone, contrast, minimum bar width, physical dimensions, and human-readable text during layout. Do not crop, resize non-uniformly, or apply lossy compression after rendering without verifying scan performance.
- Printer, label-stock, font, DPI, and operating-system behavior can vary. `ImageWriter` requires Pillow and may expose different raster formats across Pillow builds; SVG consumers may differ in SVGZ support.
- A live print or production-line integration requires approved printer drivers, permissions, label calibration, scanner acceptance testing, and an independent verification step. Do not actuate equipment or release product based only on successful Python rendering.

## Next door

Next door: pair `python-barcode` with [pyzbar](120-pyzbar.md) to decode a test image and verify that printed traceability labels round-trip to the intended serial identifier.

## References

[1]: https://python-barcode.readthedocs.io/en/stable/getting-started.html "python-barcode getting started"
[2]: https://python-barcode.readthedocs.io/en/stable/writers.html "python-barcode writers"
[3]: https://pypi.org/project/python-barcode/ "python-barcode on PyPI"

The project documents installation, barcode classes, checksum behavior, file-like output, and writer options in its [getting-started guide][1] and [writer reference][2]. Check [PyPI][3] for current releases and dependency metadata.

Caveat: barcode readability depends on the complete physical path from rendered artifact to scanner, including stock, printer, optics, lighting, motion, and quiet zones. Calibrate acceptance criteria with the actual label process.
