# 109 — Power-system analysis with pandapower

> `pandapower` is a Python toolkit for building electrical networks as tabular models and running power-flow, short-circuit, optimal-power-flow, and related studies. It is useful for reproducible planning and engineering analysis, but its numerical results remain dependent on the network data, solver assumptions, and the study standard you specify.

## Install

```bash
python -m pip install pandapower
```

The examples on this page are **local and offline**. They build a small synthetic network in memory, require no energized equipment, network connection, or GUI display, and print result tables rather than opening plots. `pandapower` depends on compiled numerical/scientific packages, so wheel availability can vary with Python version, operating system, and CPU. Use a supported CPython environment and pin the tested version for a study; install plotting extras only when you need visualization.

## First example: a small load-flow study

A load flow, or power flow, solves the steady-state operating point of a network. The external grid fixes a reference voltage, the line models impedance, and the load consumes active and reactive power. This deterministic example is safe to run on a laptop or in CI.

```python
import pandapower as pp

net = pp.create_empty_network(sn_mva=100.0)
grid_bus = pp.create_bus(net, vn_kv=20.0, name="Grid bus")
load_bus = pp.create_bus(net, vn_kv=20.0, name="Load bus")

pp.create_ext_grid(net, grid_bus, vm_pu=1.02)
pp.create_line_from_parameters(
    net,
    from_bus=grid_bus,
    to_bus=load_bus,
    length_km=1.0,
    r_ohm_per_km=0.20,
    x_ohm_per_km=0.40,
    c_nf_per_km=10.0,
    max_i_ka=0.40,
)
pp.create_load(net, load_bus, p_mw=5.0, q_mvar=1.0)

pp.runpp(net)
print(net.res_bus[["vm_pu", "va_degree"]])
print(net.res_line[["loading_percent", "p_from_mw", "q_from_mvar"]])
```

`runpp` writes calculated values into result tables such as `res_bus`, `res_line`, and `res_ext_grid`. Voltage magnitude is reported in per-unit, voltage angle in degrees, and line loading as a percentage of the configured thermal limit. A converged result is not automatically a valid engineering model: check the input units, base values, line data, transformer taps, load model, and convergence status before interpreting it.

## Build networks from standard elements

For realistic studies, prefer standard elements such as `create_bus`, `create_line`, `create_transformer`, `create_load`, `create_sgen`, and `create_ext_grid` when your equipment data matches a library type. `create_line_from_parameters` is convenient for a small transparent example, but it places responsibility for resistance, reactance, capacitance, current limit, and units on the author.

The network is stored in pandas-like tables. This makes it practical to import a reviewed asset register, inspect element indices, apply scenario changes, and export result tables. Keep the original input dataset immutable and create a separate scenario network when comparing alternatives.

```python
import pandapower as pp

net = pp.create_empty_network(sn_mva=100.0)
bus_a = pp.create_bus(net, vn_kv=110.0, name="Transmission bus")
bus_b = pp.create_bus(net, vn_kv=110.0, name="Industrial bus")
pp.create_ext_grid(net, bus_a, vm_pu=1.0)
pp.create_line_from_parameters(
    net, bus_a, bus_b, length_km=10.0,
    r_ohm_per_km=0.08, x_ohm_per_km=0.35,
    c_nf_per_km=12.0, max_i_ka=0.6,
)
load_index = pp.create_load(net, bus_b, p_mw=20.0, q_mvar=6.0, name="Base demand")

pp.runpp(net, calculate_voltage_angles=True)
base_voltage = float(net.res_bus.at[bus_b, "vm_pu"])

net.load.at[load_index, "p_mw"] *= 1.10
pp.runpp(net, calculate_voltage_angles=True)
scenario_voltage = float(net.res_bus.at[bus_b, "vm_pu"])

print(f"Base voltage: {base_voltage:.4f} pu")
print(f"10% higher-demand voltage: {scenario_voltage:.4f} pu")
```

For time series, use a controlled sequence of operating points and record convergence, voltage limits, line loading, and the exact input snapshot for every time step. Do not treat a failed or non-converged step as a normal zero-valued result.

## Short-circuit studies with IEC 60909 assumptions

`pandapower.shortcircuit.calc_sc` calculates short-circuit quantities using the network data and the selected short-circuit case. The external-grid short-circuit power and R/X parameters are essential: without a defensible source impedance, a calculated fault current is not a meaningful protection value. The following example uses explicit synthetic source data and calculates the maximum three-phase initial symmetrical short-circuit current.

```python
import pandapower as pp
from pandapower.shortcircuit import calc_sc

net = pp.create_empty_network(sn_mva=100.0)
grid_bus = pp.create_bus(net, vn_kv=20.0, name="Grid bus")
load_bus = pp.create_bus(net, vn_kv=20.0, name="Faulted bus")
pp.create_ext_grid(
    net,
    grid_bus,
    vm_pu=1.02,
    s_sc_max_mva=500.0,
    s_sc_min_mva=300.0,
    rx_max=0.10,
    rx_min=0.10,
)
pp.create_line_from_parameters(
    net, grid_bus, load_bus, length_km=1.0,
    r_ohm_per_km=0.20, x_ohm_per_km=0.40,
    c_nf_per_km=10.0, max_i_ka=0.40,
)

calc_sc(net, case="max")
print(net.res_bus_sc[["ikss_ka"]])
```

The result table contains `ikss_ka`, the initial symmetrical short-circuit current in kA. Depending on the requested calculation, additional columns can include peak and thermal-equivalent currents. For minimum-fault checks, use `case="min"` and provide minimum source parameters. Confirm the installed pandapower version's short-circuit documentation before relying on optional switches such as fault type, branch results, or kappa calculation; supported combinations and required input columns are version-sensitive.

## Inspect, validate, and export results

A study should report more than one attractive number. Check `net.converged` after a power flow, inspect voltage and loading limits, and preserve the input and software versions alongside exported results. For short-circuit work, verify that the fault type, source strengths, transformer impedances, motor contributions, and maximum/minimum case match the protection question.

```python
import pandapower as pp

net = pp.create_simple_four_bus_system() if hasattr(pp, "create_simple_four_bus_system") else pp.networks.simple_four_bus_system()
pp.runpp(net)
if not net.converged:
    raise RuntimeError("Power flow did not converge")

low_voltage = net.res_bus[net.res_bus.vm_pu < 0.95]
overloaded = net.res_line[net.res_line.loading_percent > 100.0]
print(f"Buses below 0.95 pu: {len(low_voltage)}")
print(f"Overloaded lines: {len(overloaded)}")
```

The fallback in this snippet accommodates versions that expose the standard test network through different namespaces. For a production study, prefer an explicitly version-pinned network-construction script over a convenience test case, and avoid silently accepting an empty or incomplete model.

## Safety notes

- These examples are **offline simulations only**. They do not connect to a substation, relay, inverter, PLC, or other live device, and they do not issue switching or control commands.
- A converged load flow or short-circuit calculation is not a protection-setting approval, equipment rating, arc-flash label, or proof of safe operation. Have a qualified power-system engineer review assumptions, standards, and results.
- Validate units and bases carefully. Mixing kV, V, MW, kW, MVA, ohms, per-unit values, phase quantities, or line-to-line and line-to-neutral conventions can produce plausible but dangerous results.
- Do not use synthetic or incomplete source impedance, transformer, grounding, motor, or converter data to make energization, interrupting, touch-voltage, or protection decisions. Document the data source and uncertainty for every critical parameter.
- Treat maximum and minimum fault cases as separate engineering questions. Confirm the fault type, location, source configuration, grounding method, and IEC 60909 assumptions against the applicable utility and protection requirements.
- Pin the pandapower and dependency versions, preserve the input network, record convergence and warnings, and regression-test results after upgrades. Native numerical dependencies may have platform-specific wheel availability.
- If importing measurements or topology from a live system, keep acquisition separate from any control path, validate freshness and quality, and use an approved read-only or simulator environment first. A pandapower result must never directly authorize a field operation.

## Next door

Next door: read the [pandapower documentation](https://pandapower.readthedocs.io/) for element tables, solver options, and the IEC 60909 short-circuit API, then compare study outputs with the applicable utility, protection, and equipment standards.

## References

[1]: https://pandapower.readthedocs.io/ "pandapower documentation"
[2]: https://pandapower.readthedocs.io/en/latest/powerflow/ac.html "pandapower AC power flow"
[3]: https://pandapower.readthedocs.io/en/latest/shortcircuit.html "pandapower short-circuit calculations"
[4]: https://pandapower.readthedocs.io/en/latest/elements/ext_grid.html "pandapower external-grid element"
[5]: https://pypi.org/project/pandapower/ "pandapower on PyPI"

<!-- Sources: [1] [2] [3] [4] [5] -->
