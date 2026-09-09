# 110 — Desktop HMI foundations with PySide6

> `PySide6` is the official Python binding for Qt 6. It gives operator-facing applications a mature widget toolkit, signals and slots, timers, model/view components, and platform-native desktop integration without tying the HMI to a particular PLC, protocol, or device.

## Install

Install the binding into the virtual environment used by the application:

```bash
python -m pip install PySide6
```

The wheel includes the Qt libraries needed by the binding, so a separate system Qt installation is normally not required. Pin and test a version for production deployments; wheel availability and native platform support vary by Python version and operating system. The Qt for Python documentation lists the currently supported platforms and installation procedure [1].

## Run an offline HMI smoke test

A useful first test should not open a window, connect to equipment, or write an output. This example builds a small status panel from deterministic local data and selects Qt's `offscreen` platform backend before importing Qt. It therefore works in a headless CI runner as well as on a desktop, provided the PySide6 wheel supports the host platform.

```python
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


def build_demo_panel() -> QWidget:
    panel = QWidget()
    panel.setWindowTitle("Demo HMI")
    layout = QVBoxLayout(panel)

    status = QLabel("Pump: stopped | pressure: 2.4 bar")
    acknowledge = QPushButton("Acknowledge demo alarm")
    acknowledge.clicked.connect(lambda: status.setText("Pump: stopped | alarm acknowledged"))

    layout.addWidget(status)
    layout.addWidget(acknowledge)
    return panel


app = QApplication(sys.argv)
panel = build_demo_panel()
panel.show()
QTimer.singleShot(50, app.quit)
exit_code = app.exec()
print(f"offline HMI smoke test completed with exit code {exit_code}")
raise SystemExit(exit_code)
```

`QApplication` owns the event loop, and `QTimer.singleShot` gives the loop one short turn before clean shutdown. Remove the `QT_QPA_PLATFORM` line and the timer for an interactive desktop test; that variant requires a working display server or windowing session.

## Build a clear operator status panel

An HMI should expose state rather than make an operator infer it from a raw value. Keep the display text, colour, and enabled actions derived from one state object. The following example is an interactive desktop example: it requires a display and demonstrates a local simulation only. It does not talk to a live controller.

```python
import sys
from dataclasses import dataclass

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget


@dataclass
class MachineState:
    running: bool = False
    temperature_c: float = 22.5
    alarm: str = ""


def render(state: MachineState, status: QLabel, action: QPushButton) -> None:
    state_text = "RUNNING" if state.running else "STOPPED"
    alarm_text = f" | alarm: {state.alarm}" if state.alarm else ""
    status.setText(f"Machine: {state_text} | temperature: {state.temperature_c:.1f} °C{alarm_text}")
    action.setText("Stop" if state.running else "Start")


app = QApplication(sys.argv)
state = MachineState()
window = QWidget()
window.setWindowTitle("Local machine simulator")
layout = QVBoxLayout(window)
status = QLabel()
action = QPushButton()
layout.addWidget(status)
layout.addWidget(action)


def toggle_machine() -> None:
    state.running = not state.running
    state.temperature_c = 34.0 if state.running else 22.5
    render(state, status, action)


action.clicked.connect(toggle_machine)
render(state, status, action)
window.resize(360, 100)
window.show()

# This local simulation changes the reading once, then leaves the panel interactive.
QTimer.singleShot(1000, toggle_machine)
raise SystemExit(app.exec())
```

For a real application, separate the device or protocol adapter from the widgets. The adapter should publish validated snapshots through signals, while the GUI thread only renders snapshots and sends explicitly confirmed commands. Avoid putting blocking serial, Modbus, HTTP, or database calls in a button callback or timer slot because they freeze repainting and make the interface appear unsafe or dead.

## Use signals, timers, and worker boundaries

A `QTimer` is suitable for lightweight periodic work such as refreshing a clock or requesting a new snapshot from a non-blocking adapter. It is not a substitute for a worker thread when an operation can block. A worker can emit a result signal back to the GUI thread; the GUI then updates widgets in that slot. Qt's timer documentation describes the timeout signal and event-loop requirements [2].

```python
import sys
from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class DemoSource(QObject):
    reading_ready = Signal(float)

    def __init__(self) -> None:
        super().__init__()
        self._value = 20.0

    def poll_local_value(self) -> None:
        self._value += 0.5
        self.reading_ready.emit(self._value)


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Timed local reading")
layout = QVBoxLayout(window)
label = QLabel("waiting for a reading")
layout.addWidget(label)
source = DemoSource()
timer = QTimer()


def show_reading(value: float) -> None:
    label.setText(f"temperature: {value:.1f} °C")


source.reading_ready.connect(show_reading)
timer.timeout.connect(source.poll_local_value)
timer.start(250)
source.poll_local_value()
window.show()
raise SystemExit(app.exec())
```

Keep references to timers, workers, and adapters for as long as they are needed. Qt objects have ownership and thread-affinity rules; create and use widgets on the GUI thread, and communicate across worker boundaries with signals rather than directly mutating widgets.

## Structure a production desktop HMI

A practical application commonly has four layers: a device adapter, a validated state model, a presentation layer, and an audit or logging path. The adapter translates protocol-specific values into typed domain values. The model records freshness, quality, limits, and alarm state. The widgets render that model. The command path validates intent, requests confirmation where appropriate, and records the result.

| Layer | Responsibility | Example boundary |
|---|---|---|
| Adapter | Read and write a device or service | `read_snapshot()` and `set_mode()` |
| State model | Validate values and track freshness | `temperature_c`, quality, timestamp |
| Qt presentation | Render state and collect intent | labels, tables, buttons, trends |
| Audit path | Record operator actions and outcomes | structured log or local database |

Use `QMainWindow` for a multi-panel operator application, `QFormLayout` for labelled values, and Qt's model/view classes for larger tables. Keep units in labels, show the age of the last successful reading, and distinguish **unknown**, **stale**, and **zero**. A disconnected sensor should never silently appear as a healthy zero.

## Package and platform caveats

PySide6 is distributed on PyPI as the Qt for Python binding [3]. Its wheels are platform-specific and can be large because they carry Qt libraries. Verify the Python version, architecture, and target operating system in the deployment environment. On Linux, a normal interactive run needs a compatible Qt platform plugin and display session such as X11 or Wayland; in CI or a service, use the offscreen backend only for tests that do not require visual verification. Native packaging also needs attention to Qt plugins, permissions, and desktop launch configuration.

## Safety notes

Treat the HMI as an observation and command surface, not as the safety function. A button, colour, or displayed value is not an independent protective interlock. Enforce limits, permissives, watchdogs, emergency-stop behavior, and fail-safe output states in the controller or dedicated safety system.

Never allow stale, malformed, or unvalidated data to drive a command. Show communication age and quality, disable or gate commands when the device state is unknown, and require explicit confirmation for consequential actions. Make command handling idempotent where possible, log the requested and acknowledged result, and test behavior during disconnects, restarts, clock changes, and partial updates.

Do not perform blocking I/O on the GUI thread. A frozen window can hide an alarm and encourage unsafe retries. Test the deployed Qt backend and screen scaling on the actual operator workstation, and provide a documented recovery path if the application or display process exits.

## Next door

Next door: pair PySide6 with `pyserial` for a serial adapter, `pymodbus` for Modbus devices, or `pandas` for an offline trend and alarm-history view.

## References

[1]: https://doc.qt.io/qtforpython-6/ "Qt for Python documentation"
[2]: https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html "PySide6 QTimer documentation"
[3]: https://pypi.org/project/PySide6/ "PySide6 on PyPI"

The installation guidance and platform model follow the Qt for Python documentation [1], the timer discussion follows the `QTimer` API reference [2], and package availability follows the PyPI project record [3].
