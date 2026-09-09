# 108 — Discrete-event simulation with SimPy

> `simpy` is a pure-Python, process-based discrete-event simulation framework. It lets you represent jobs, machines, buffers, and shared operators as generator-based processes and resources, then study queueing, cycle time, utilization, and throughput without connecting to a live production system.

## Install

```bash
python -m pip install simpy
```

SimPy is distributed as a platform-independent Python wheel, has no runtime dependencies, and supports Python 3.8+ on CPython and PyPy. The examples below are local, deterministic demonstrations: they print results, need no PLC, network connection, database, or GUI display, and run in simulated time rather than waiting for wall-clock time. Pin the SimPy version and random-number seed for a repeatable study.

## First example: an offline production line

A line can be modeled as processes that arrive, request a limited-capacity machine, receive service, and move to the next operation. `Resource` requests queue when all machine slots are busy; the `with` block releases a request even if the process exits unexpectedly. This example models a two-machine line with a finite buffer and reports completed units, average flow time, and machine utilization.

```python
import random
import simpy

RANDOM_SEED = 7
RUN_UNTIL = 480.0  # minutes in one simulated shift


def station(env, name, input_buffer, output_buffer, capacity, service_time, stats):
    machine = simpy.Resource(env, capacity=capacity)
    stats[name] = {"busy_minutes": 0.0, "completed": 0}

    while True:
        job = yield input_buffer.get()
        entered = env.now
        with machine.request() as request:
            yield request
            started = env.now
            yield env.timeout(service_time(job))
            stats[name]["busy_minutes"] += env.now - started
        stats[name]["completed"] += 1
        yield output_buffer.put((job, entered))


def arrivals(env, first_buffer, interarrival, total_jobs):
    for job_id in range(total_jobs):
        yield first_buffer.put(job_id)
        yield env.timeout(interarrival)


def line_sink(env, finished_buffer, flow_times):
    while True:
        job, entered_line = yield finished_buffer.get()
        flow_times.append((job, env.now - entered_line))


random.seed(RANDOM_SEED)
env = simpy.Environment()
raw_material = simpy.Store(env, capacity=6)
between_stations = simpy.Store(env, capacity=4)
finished = simpy.Store(env)
stats = {}
flow_times = []

# Fixed service times make the baseline easy to audit. Add distributions later.
env.process(arrivals(env, raw_material, interarrival=7.0, total_jobs=100))
env.process(station(env, "cut", raw_material, between_stations, 1, lambda _: 5.0, stats))
env.process(station(env, "assemble", between_stations, finished, 1, lambda _: 9.0, stats))
env.process(line_sink(env, finished, flow_times))
env.run(until=RUN_UNTIL)

print(f"completed: {len(flow_times)}")
print(f"throughput per hour: {len(flow_times) / (RUN_UNTIL / 60.0):.2f}")
if flow_times:
    mean_flow = sum(flow for _, flow in flow_times) / len(flow_times)
    print(f"mean flow time (minutes): {mean_flow:.2f}")
for name, values in stats.items():
    print(f"{name} utilization: {values['busy_minutes'] / RUN_UNTIL:.1%}")
```

`Environment` advances directly to the next scheduled event, so a 480-minute shift completes quickly. A `Store` models a finite buffer of job objects; a `Resource` models a machine's simultaneous capacity. The model's units are minutes because the inputs use minutes. A throughput result is meaningful only with a declared warm-up policy, run length, arrival process, service-time distributions, and definition of “completed.”

## Model arrivals, queues, and bottlenecks

Use a process to create jobs and `env.timeout()` to schedule the next arrival. For a production study, replace the constant inter-arrival and service times with reviewed distributions. `random.expovariate(rate)` is useful for a first Poisson-arrival sensitivity study, while empirical samples or a fitted distribution may be more appropriate for batch releases, changeovers, or correlated downtime.

A queue is not automatically a physical buffer. An unbounded `Store` can hide starvation or overflow; give buffers a capacity when blocking matters. If a machine can process two units in parallel, use `Resource(env, capacity=2)`. If urgent work should be served first, use `PriorityResource`; document the priority policy because it changes waiting-time fairness and may starve low-priority jobs.

```python
import random
import simpy


def job_generator(env, queue, number, mean_interarrival):
    for job_id in range(number):
        yield queue.put((job_id, env.now))
        yield env.timeout(random.expovariate(1.0 / mean_interarrival))


def processor(env, queue, service, results):
    machine = simpy.Resource(env, capacity=1)
    while True:
        job_id, queued_at = yield queue.get()
        with machine.request() as request:
            yield request
            wait = env.now - queued_at
            yield env.timeout(random.expovariate(1.0 / service))
            results.append((job_id, wait, env.now))


random.seed(11)
env = simpy.Environment()
queue = simpy.Store(env, capacity=20)
results = []
env.process(job_generator(env, queue, number=80, mean_interarrival=6.0))
env.process(processor(env, queue, service=8.0, results=results))
env.run(until=600.0)

print(f"finished: {len(results)}")
if results:
    waits = [wait for _, wait, _ in results]
    print(f"mean queue wait (minutes): {sum(waits) / len(waits):.2f}")
print(f"unfinished in buffer: {len(queue.items)}")
```

Inspect both throughput and queue behavior. A line can produce the target rate while accumulating work-in-process and unacceptable lead time, especially near saturation. Record queue length over time or sample it at regular simulated intervals; do not infer it from the final queue contents alone.

## Compare capacity scenarios with replications

One random run is a scenario, not a confidence interval. Run multiple independent replications with different seeds, discard a documented warm-up period for a continuously operating line, and summarize the distribution of throughput or waiting time. The following example compares one versus two parallel machines using the same arrival and service assumptions. It uses a finite horizon and counts only completions after the warm-up cutoff.

```python
import random
import statistics
import simpy


def arrivals(env, queue, mean_interarrival, horizon):
    job_id = 0
    while env.now < horizon:
        yield queue.put((job_id, env.now))
        job_id += 1
        yield env.timeout(random.expovariate(1.0 / mean_interarrival))


def workers(env, queue, capacity, mean_service, completed, warmup):
    machine = simpy.Resource(env, capacity=capacity)
    while True:
        job_id, _ = yield queue.get()
        with machine.request() as request:
            yield request
            yield env.timeout(random.expovariate(1.0 / mean_service))
            if env.now >= warmup:
                completed.append(job_id)


def replicate(capacity, seed, horizon=2_000.0, warmup=500.0):
    random.seed(seed)
    env = simpy.Environment()
    queue = simpy.Store(env, capacity=200)
    completed = []
    env.process(arrivals(env, queue, mean_interarrival=9.0, horizon=horizon))
    env.process(workers(env, queue, capacity, mean_service=12.0, completed=completed, warmup=warmup))
    env.run(until=horizon)
    measured_hours = (horizon - warmup) / 60.0
    return len(completed) / measured_hours


for capacity in (1, 2):
    rates = [replicate(capacity, seed) for seed in range(10, 20)]
    print(
        f"capacity={capacity}: mean={statistics.mean(rates):.2f}/hour, "
        f"stdev={statistics.stdev(rates):.2f}"
    )
```

Use common random numbers when comparing scenarios if you want input variability to cancel more cleanly, but keep the analysis plan fixed before inspecting results. For a serious study, report replication count, warm-up, confidence intervals, rejected or blocked jobs, and the exact model version. If the line has setup families, failures, repairs, shifts, or finite raw material, represent those events explicitly rather than adding an unexplained correction factor.

## Add work-in-process and downstream material flow

`Container` is useful for homogeneous quantities such as kilograms of resin, liters of liquid, or a common pool of tokens. `Store` is better when each unit needs an ID, due date, product family, or quality status. A downstream process can `get()` finished units from a `Store`, while an upstream process blocks on `put()` when a finite buffer is full; that naturally models line blocking and backpressure.

For dashboards, collect timestamped observations in ordinary Python lists and export them after the run. SimPy itself does not provide a plotting backend, and no GUI is required. If you add Matplotlib, select a non-interactive backend such as `Agg` in headless CI and save files rather than calling `plt.show()`.

## Safety notes

- These examples are **offline simulations only**. They do not read a PLC, drive a robot, connect to a historian, or issue a production-control command.
- A simulation is a decision-support model, not proof that a line will meet a takt time, quality target, ergonomic limit, or safety requirement. Validate assumptions against measured production data and have process owners review the result.
- Define job arrival, service, setup, downtime, scrap, rework, buffer capacity, shift calendar, and completion rules before interpreting throughput. A wrong event definition can produce precise but misleading numbers.
- Do not use an unvalidated model to bypass guarding, change interlocks, extend maintenance intervals, approve staffing reductions, or authorize a live equipment change.
- Use finite buffers and explicit blocking when those constraints exist physically. Unbounded queues can hide WIP growth, memory use, and impossible material flow.
- Treat random seeds, warm-up periods, horizon length, replication count, and confidence intervals as part of the experiment record. Re-run sensitivity studies after changing SimPy, Python, or model dependencies.
- Keep acquisition, simulation, optimization, and control paths separate. If live data is imported, use a read-only snapshot or replay and validate timestamps, units, missing records, and asset identity before fitting or calibrating the model.
- SimPy is event-based rather than a fixed-step continuous simulator. It is a good fit for interacting jobs and shared resources; choose a domain-specific or continuous solver when physical dynamics between events are the primary question.

## Next door

Next door: read the [SimPy tutorial and shared-resources guide](https://simpy.readthedocs.io/en/latest/) and pair the model with [pandas](https://pandas.pydata.org/docs/) for validated production-data preparation and replication summaries.

## References

[1]: https://simpy.readthedocs.io/en/latest/ "SimPy documentation"
[2]: https://simpy.readthedocs.io/en/latest/topical_guides/resources.html "SimPy shared resources"
[3]: https://pypi.org/project/simpy/ "SimPy on PyPI"

<!-- Sources: [1] [2] [3] -->
