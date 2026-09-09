# 111 — Touchscreen HMIs with Kivy

> `kivy` is a cross-platform Python framework for touch-aware user interfaces. It is a practical fit for operator panels that need large controls, portable deployment, and a clear separation between a visual screen and the commands or status model behind it.

## Install

```bash
python -m pip install kivy
```

Kivy 2.3.1 documents support for Python 3.8–3.13 and provides platform-specific wheels for common desktop systems.[1] Installation can still depend on the operating system, Python architecture, and available graphics backend. A Kivy application normally needs a window provider such as SDL2 and an OpenGL-capable display; a remote shell, minimal container, or display-less service is not a substitute for a target-panel test.

## Start offline: model touch actions before drawing a screen

A touch panel should not put device I/O directly in a button callback. Start with a small, display-free command model that can be tested on a laptop or in continuous integration. This example accepts only bounded operator intents and records them; it uses no hardware and opens no GUI window.

```python
from dataclasses import dataclass, field


@dataclass
class OperatorPanel:
    enabled: bool = False
    events: list[str] = field(default_factory=list)

    def press_enable(self) -> str:
        self.enabled = True
        self.events.append("enable_requested")
        return "enabled"

    def press_stop(self) -> str:
        self.enabled = False
        self.events.append("stop_requested")
        return "stopped"

    def press_start(self, permissive: bool) -> str:
        if not self.enabled:
            self.events.append("start_rejected:panel_disabled")
            return "rejected: panel disabled"
        if not permissive:
            self.events.append("start_rejected:not_permissive")
            return "rejected: not permissive"
        self.events.append("start_requested")
        return "start requested"


panel = OperatorPanel()
print(panel.press_start(permissive=True))
print(panel.press_enable())
print(panel.press_start(permissive=True))
print(panel.press_stop())
print("audit:", panel.events)
```

Keep this model independent of Kivy. A later widget callback can call `press_start()` and render the returned state, while a separate, reviewed adapter translates `start_requested` into a protocol or PLC command. That separation makes touch behavior testable without pretending that a simulated click proves a real machine is safe.

## Build a large touch-first panel

`App.build()` returns the root widget tree. Use generous button sizes, short labels, high contrast, and a persistent status area rather than relying on hover states or tiny desktop controls. The following is a **display-required demo**: run it on a workstation or target panel with a working Kivy window backend.

```python
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class TouchPanel(App):
    def build(self):
        self.status = Label(text="READY", font_size=dp(28), size_hint_y=None, height=dp(72))
        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(18))
        root.add_widget(self.status)

        controls = BoxLayout(spacing=dp(18))
        start = Button(text="START", font_size=dp(30))
        stop = Button(text="STOP", font_size=dp(30))
        start.bind(on_release=self.request_start)
        stop.bind(on_release=self.request_stop)
        controls.add_widget(start)
        controls.add_widget(stop)
        root.add_widget(controls)
        return root

    def request_start(self, _button):
        self.status.text = "START REQUESTED"

    def request_stop(self, _button):
        self.status.text = "STOP REQUESTED"


if __name__ == "__main__":
    TouchPanel().run()
```

The callback above changes only the display. In a live HMI, replace the status-only body with a call to the command model and an adapter that has explicit timeouts, acknowledgements, and fault handling. Do not infer that a command succeeded merely because a button was released.

## Update status without blocking the UI

Kivy's `Clock` schedules callbacks on the event loop.[2] Use it for lightweight polling of a cached, thread-safe status snapshot or for a heartbeat indicator. Do not perform slow serial, network, filesystem, or database operations inside a widget callback; they can make the screen stop responding to touches.

```python
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label


class StatusDemo(App):
    def build(self):
        self.ticks = 0
        self.label = Label(text="status: starting", font_size=dp(28))
        Clock.schedule_interval(self.refresh_status, 1.0)
        return self.label

    def refresh_status(self, _elapsed):
        self.ticks += 1
        self.label.text = f"status heartbeat: {self.ticks}"


if __name__ == "__main__":
    StatusDemo().run()
```

For real I/O, let a worker or asynchronous service own the blocking operation and pass immutable results back to the UI thread. Stop scheduled events and worker tasks during application shutdown so a late result cannot update a destroyed widget.

## Make touch feedback and navigation explicit

Touch users need immediate visual feedback. Disable or restyle a control while a command is pending, show the last update time, and provide a clear fault screen that does not disappear when another status message arrives. For multiple screens, use a `ScreenManager` with named screens rather than building ad hoc widget replacement logic. Keep navigation separate from process commands so a screen change cannot accidentally start or stop equipment.

A portable HMI also needs a deployment decision. Desktop Kivy builds use the host's window and graphics stack; Android, iOS, and other targets require their respective packaging workflows and platform permissions. Test the exact display resolution, touch calibration, orientation, font rendering, and sleep/lock behavior on the intended device. Kivy's core UI is portable, but the packaging and backend details are not identical across platforms.

## Safety notes

Kivy is a user-interface toolkit, not a safety-rated control system. Treat every touch as an untrusted request and require the command layer to validate mode, permissions, permissives, freshness of feedback, and safe bounds before any actuator write. Provide a physically independent emergency stop and other required protective functions; never implement them only as an on-screen button. Make STOP behavior fail-safe and available from every operating screen, and define what happens when the display, application, network, or power fails. Record command requests and device acknowledgements with timestamps, but do not log secrets or unnecessary personal data. Test accidental touches, glove use, wet screens, stale status, reconnects, duplicate taps, and loss of focus on the actual panel.

## Next door

Next door: pair Kivy with a small, independently tested command/state layer, then connect that layer to the appropriate protocol guide such as [pymodbus](028-modbus-pymodbus.md) rather than letting widget callbacks write registers directly.

### References

[1]: https://kivy.org/doc/stable/gettingstarted/installation.html "Kivy installation documentation"
[2]: https://kivy.org/doc/stable/api-kivy.clock.html "Kivy Clock API"
[3]: https://kivy.org/doc/stable/api-kivy.app.html "Kivy Application API"

Kivy's supported Python versions and installation paths are described in its [installation documentation][1]. The scheduling and application lifecycle APIs used above are documented in the [Clock API][2] and [Application API][3].
