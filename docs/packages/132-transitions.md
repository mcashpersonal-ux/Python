# 114 — Equipment state machines with transitions

> `transitions` is a lightweight Python library for modeling finite state machines. It turns named states, triggers, guards, and callbacks into explicit lifecycle logic, which is useful for sequencing equipment commands and making interlocks reviewable before connecting to a real controller.

## Install

```bash
python -m pip install transitions
```

The core package is pure Python and does not require a device, network connection, or GUI display. The project publishes wheels for current CPython releases, including Python 3.8 through 3.13; pin the version used in tests because callback behavior and extension APIs should be regression-tested with your application. Diagram support is optional: `transitions[diagrams]` may require Graphviz/pygraphviz or another backend, while the examples below use only the core package.

## First example: an offline equipment lifecycle

A state machine should describe **what may happen next**, not merely store a string such as `"running"`. The following demo models a pump with an explicit `off → ready → running` sequence, a guarded start, and a fault path. It is local and deterministic: it prints an event log and never opens a socket, controls hardware, or requires a display.

```python
from transitions import Machine


class Pump:
    def __init__(self) -> None:
        self.estop_clear = True
        self.suction_ok = False
        self.log = []
        self.machine = Machine(
            model=self,
            states=["off", "ready", "running", "fault"],
            initial="off",
            auto_transitions=False,
            after_state_change="record_state",
        )
        self.machine.add_transition(
            "enable", "off", "ready", conditions="guard_clear"
        )
        self.machine.add_transition(
            "start",
            "ready",
            "running",
            conditions=["guard_clear", "suction_present"],
            before="record_start_request",
        )
        self.machine.add_transition("stop", "running", "ready")
        self.machine.add_transition("trip", ["ready", "running"], "fault")
        self.machine.add_transition("reset", "fault", "off", conditions="guard_clear")

    def guard_clear(self) -> bool:
        return self.estop_clear

    def suction_present(self) -> bool:
        return self.suction_ok

    def record_start_request(self) -> None:
        self.log.append("start request accepted")

    def record_state(self) -> None:
        self.log.append(f"state={self.state}")


pump = Pump()
pump.enable()
pump.suction_ok = True
pump.start()
pump.stop()
pump.trip()
print(pump.state)
print(" | ".join(pump.log))
```

The `Machine` attaches trigger methods such as `enable()` and `start()` to the model. A trigger succeeds only when its source state and conditions match. With `auto_transitions=False`, the library does not silently add convenience methods for every state, so an unreviewed state jump is less likely to appear in application code. A failed condition leaves the state unchanged and raises a transition error; handle that error at the command boundary and report why the request was rejected.

## Design states around an equipment lifecycle

Choose states that have distinct operating rules, outputs, and permitted commands. A useful sequence commonly separates **disabled**, **initializing**, **ready**, **starting**, **running**, **stopping**, and **fault** rather than treating all non-running values as one state. State names are not proof of physical feedback: `running` should mean that the application has received the required run confirmation, not merely that it issued a start command.

| State | Typical entry evidence | Permitted next actions |
| --- | --- | --- |
| `off` | Output is commanded safe and the lifecycle is inactive | Enable, or remain off |
| `ready` | Initialization completed and permissives are true | Start, disable, or trip |
| `running` | Run command and independent run feedback agree | Stop, or trip |
| `stopping` | Stop command is in progress | Confirm stopped, or fault on timeout |
| `fault` | A trip, timeout, or invalid feedback was recorded | Reset only after the cause and permissives are cleared |

Keep physical I/O, timing, and communication adapters outside the state model. The adapter should translate a sensor snapshot into facts such as `suction_ok` and translate an accepted transition into a reviewed output command. This separation makes replay tests possible and prevents a state-machine callback from accidentally hiding a network write.

## Encode interlocks as guards, not comments

A guard is a boolean predicate evaluated before a transition. Use guards for conditions that must already be true, such as an emergency-stop circuit being healthy, a valve being open, a door being closed, a pressure switch being satisfied, or a maintenance lock being absent. Keep guards side-effect-free. They should read a validated snapshot and return a decision; they should not start a motor, sleep, retry a network call, or mutate state.

```python
from transitions import Machine


class Mixer:
    def __init__(self) -> None:
        self.lid_closed = False
        self.drain_closed = True
        self.maintenance_lock = False
        self.state_log = []
        self.machine = Machine(
            model=self,
            states=["idle", "armed", "mixing", "blocked"],
            initial="idle",
            auto_transitions=False,
            after_state_change="remember",
        )
        self.machine.add_transition("arm", "idle", "armed", conditions="safe_to_arm")
        self.machine.add_transition("mix", "armed", "mixing", conditions="safe_to_mix")
        self.machine.add_transition("stop", "mixing", "armed")
        self.machine.add_transition("block", ["armed", "mixing"], "blocked")
        self.machine.add_transition("clear", "blocked", "idle", conditions="safe_to_arm")

    def safe_to_arm(self) -> bool:
        return not self.maintenance_lock

    def safe_to_mix(self) -> bool:
        return self.lid_closed and self.drain_closed and not self.maintenance_lock

    def remember(self) -> None:
        self.state_log.append(self.state)


mixer = Mixer()
mixer.arm()
try:
    mixer.mix()
except Exception as exc:
    print(f"start rejected in {mixer.state}: {type(exc).__name__}")

mixer.lid_closed = True
mixer.mix()
print(mixer.state)
```

The example intentionally rejects `mix()` until the lid feedback is present. In a live integration, update `lid_closed` from a timestamped, quality-checked input rather than from the same command path that requests motion. If a permissive becomes false while running, trigger a fault or controlled stop according to the equipment risk assessment; do not assume a guard checked during `start()` remains true forever.

## Sequence commands with callbacks and timeouts

Callbacks are useful for bookkeeping, audit records, and emitting an already-reviewed command to an adapter. `before` callbacks run before the state change, while `after` callbacks run after it. Keep them short and deterministic. For a real start sequence, represent waiting explicitly: enter `starting`, issue the command once, then let a supervisor trigger `confirm_running` when feedback arrives or `start_timeout` when a deadline expires.

```python
from transitions import Machine


class Fan:
    def __init__(self) -> None:
        self.feedback_running = False
        self.outputs = []
        self.machine = Machine(
            model=self,
            states=["stopped", "starting", "running", "fault"],
            initial="stopped",
            auto_transitions=False,
        )
        self.machine.add_transition(
            "request_start", "stopped", "starting", before="issue_start"
        )
        self.machine.add_transition(
            "confirm_running", "starting", "running", conditions="has_feedback"
        )
        self.machine.add_transition("start_timeout", "starting", "fault")
        self.machine.add_transition("stop", ["starting", "running"], "stopped")

    def issue_start(self) -> None:
        self.outputs.append("start command")

    def has_feedback(self) -> bool:
        return self.feedback_running


fan = Fan()
fan.request_start()
print(fan.state, fan.outputs)
fan.feedback_running = True
fan.confirm_running()
print(fan.state)
```

The state machine does not provide a clock or a safety-rated timeout by itself. A scheduler, PLC scan, or supervisory task must call the timeout trigger at a defined deadline and must make duplicate commands idempotent. For asynchronous applications, inspect the installed release's `transitions.extensions.asyncio.AsyncMachine`; do not mix synchronous callbacks and event-loop tasks without a clear ownership and cancellation policy.

## Test every legal and illegal path

Treat the transition table as a compact specification. Test the initial state, every legal trigger, every rejected trigger, guard changes, duplicate events, fault recovery, stale feedback, and restart behavior. A small table-driven test can assert that a rejected start does not alter state:

```python
from transitions import MachineError

from transitions import Machine


class Valve:
    def __init__(self) -> None:
        self.open_feedback = False
        self.machine = Machine(
            model=self,
            states=["closed", "opening", "open", "fault"],
            initial="closed",
            auto_transitions=False,
        )
        self.machine.add_transition("open_request", "closed", "opening")
        self.machine.add_transition(
            "confirm_open", "opening", "open", conditions="is_open"
        )
        self.machine.add_transition("timeout", "opening", "fault")

    def is_open(self) -> bool:
        return self.open_feedback


valve = Valve()
valve.open_request()
try:
    valve.confirm_open()
except MachineError:
    print("feedback guard rejected the transition")
assert valve.state == "opening"
valve.open_feedback = True
valve.confirm_open()
assert valve.state == "open"
print("lifecycle assertions passed")
```

For larger systems, keep the transition table in code review and use property-based or model-based tests to generate event sequences. Log the trigger, source state, destination state, guard result, input snapshot timestamp, and correlation ID. This makes a rejected command diagnosable without treating a log message as evidence that the physical operation completed.

## Optional hierarchy and diagrams

`HierarchicalMachine` in `transitions.extensions` can represent nested modes such as `automatic`, `manual`, and `maintenance`, each with substates. Use hierarchy only when the parent state has meaningful shared entry/exit behavior; otherwise a flat machine is easier to audit. Diagram extensions are optional and may require `transitions[diagrams]` plus system Graphviz libraries. A generated diagram is a review aid, not an executable safety analysis, and backend availability varies by operating system.

For package availability, the core `transitions` project is on PyPI and the source repository documents extension modules separately. Pin the package and optional backend versions in a lock file, especially when diagrams or asyncio extensions are part of a deployed toolchain.

## Safety notes

- These examples are **offline simulations only**. They do not connect to a PLC, robot, pump, valve, motor starter, network, or proprietary controller, and they do not require a GUI display.
- `transitions` is an application-level modeling library, not a safety-rated controller, emergency-stop circuit, motion controller, or proof of compliance with a machinery or process-safety standard.
- Do not aim a callback at a live output until the complete command path has been reviewed. Use a simulator or replay first, then an isolated lab controller with explicit dry-run and read-only modes.
- Keep guards pure and fail closed when required feedback is missing, stale, contradictory, or of unknown quality. Never treat a missing sensor value as permission to start.
- Separate command acknowledgement from physical completion. Require independent feedback for running, stopped, valve position, pressure, temperature, door position, and other equipment-specific facts.
- Implement watchdogs, bounded retries, communication-loss behavior, duplicate-event handling, and restart recovery outside the state machine or in a clearly tested supervisory layer.
- Make fault recovery deliberate. A `reset` trigger must not clear an alarm or re-energize equipment until the initiating cause, personnel clearance, and all permissives have been verified.
- Record state changes and rejected triggers with timestamps, asset identity, software version, and input quality. Protect audit logs from silent truncation and preserve enough history to investigate an unexpected transition.
- Review transitions for race conditions when multiple threads, callbacks, or asyncio tasks can trigger the same model. Serialize events per asset and define cancellation semantics before deployment.

## Next door

Next door: read the [`transitions` state-machine documentation](https://github.com/pytransitions/transitions) and pair the model with a simulator or PLC test harness before designing a live control integration.

## References

[1]: https://github.com/pytransitions/transitions "transitions source repository and documentation"
[2]: https://pypi.org/project/transitions/ "transitions on PyPI"
[3]: https://github.com/pytransitions/transitions#some-key-concepts "transitions core concepts"

<!-- Sources: [1] [2] [3] -->
