# Qollab Python runner and UI bridge

The root `main.py` is the Python-mode entry point. Running it directly prints a
dependency-free environment report and exits without importing Qiskit or
running a circuit. The Task 8 release adds a separate Python smoke package that
imports the project, checks Qiskit, and runs a small synthetic QAOA circuit on
Qiskit's local `BasicSimulator`.

## Task 8 clean-session check

Build the two release archives from the project root:

```sh
python scripts/package_qollab_release.py
```

Upload `qollab-task8-python-smoke.zip` as a Python-mode project and run its
`main.py`. Copy the complete JSON output. This checks Qollab's Python package
environment and local Qiskit `BasicSimulator` execution. It does **not** call a
Qollab-provided free simulator/backend, submit an IonQ job, or test browser to
Python calls. The report lists names, types, and public method names for any
backend-like objects exposed in the entry-point namespace; it does not print
object values or credentials.

The clean-session run succeeded on Python 3.14.2 with Qiskit 2.5.2, NumPy
2.4.6, and SciPy 1.18.0. The synthetic p=1, four-qubit, K=2 trial used 512
shots, returned a feasible sample with zero objective gap, and completed one
`BasicSimulator` sampling job. The report exposed a global `backend` instance
whose exact type is Qiskit's `BasicSimulator`. A second run passed that injected
instance into QAOA and confirmed `available: true`, `used_for_qaoa: true`, one
sampling job, and no remote submission. This completes the clean Python and
host-exposed local simulator check; sampling counts vary between runs.

The user uploaded `qollab-task8-app.zip` in HTML/JS mode and confirmed that the
page loads, the replay labels and reload/reset behavior work, and no browser
errors were found. The bundled controls use clearly labeled replays because a
Qollab browser-to-Python adapter has not been verified. Live hosted QAOA result
rendering remains pending that bridge check.

## Dependencies and execution scope

The Qollab ZIP places the Python package at its root so the project loader can
resolve the explicit `repackq.*` imports without a runtime-added `src` search
path. The repository itself retains its normal `src/` layout.

The implementation uses Qiskit core (`QuantumCircuit`, `SparsePauliOp`,
`Statevector`, `transpile`, and `BasicSimulator`). It has its own p=1 QAOA
parameter optimizer and does not require the Qiskit Algorithms or Qiskit
Optimization add-on packages. It does not draw circuits, so Qiskit
Visualizations is also unnecessary. SciPy is optional: it enables COBYLA for
direct callers, while the packaged demo uses a deterministic grid optimizer.
No paid service or separate deployment is required.

The optimizer uses a deterministic grid/refinement method, so SciPy is not
required. `run_task5_toy_demo()` uses synthetic cells only and does not submit
a Qollab or IonQ backend job. The package-version diagnostic does not prove
that Qiskit imports or runs successfully; the separate `qollab_runtime_probe()`
can perform that smoke check if the host can invoke Python functions.

## Qollab runtime validation

The Task 5 record reports a Qollab Python-runner check on Qiskit 2.5.2. Its
p=1, four-qubit, K=2 run used 512 local `BasicSimulator` shots and one local
sampling call. Exhaustive QUBO mapping verification passed. The best measured
feasible sample matched the exact optimum (`TOY-0`, `TOY-1`) with zero
objective gap; feasible sampling mass was 0.6074 and exact-optimum sampling
mass was 0.2441. The report also identified an infeasible cardinality-1
sample, as expected from the raw counts.

The Task 5 and Task 8 runs validate the Qollab Python environment and its
host-exposed local `BasicSimulator` path. No remote Qollab or IonQ backend was
used. The browser bridge and IonQ remain unverified. The circuit uses synthetic
data and is not a battery-data result.

## Task 7 browser application

The project includes the RePack-Q workbench at `web/index.html`, host-callable
UI functions in root `main.py`, and a local HTTP server in
`run_repackq_web.py`. The complete Python API lives in `src/repackq/ui.py`; it
returns decision-time snapshots separately from held-out fixture observations.
The optimizer and QAOA wrapper never receive future truth. Future values are
returned only by the reveal API after the UI's explicit reveal action.

The local browser/Python contract is documented in
[`web/js/components/README.md`](../web/js/components/README.md). On loopback
hosts, the browser registers a same-origin HTTP adapter and QAOA stages stream
back to the UI as they occur. Other hosts require their own verified adapter.
Qollab's Python project mode runs `main.py` and displays text output. Its
HTML/JS mode requires root `index.html` and `main.js`, which now boot the
workbench; root `styles.css` supplies the preview stylesheet.

Build the app and Python smoke packages on Windows, macOS, or Linux:

```sh
python scripts/package_qollab_release.py
```

The command creates `qollab-task8-app.zip` and
`qollab-task8-python-smoke.zip`. The app ZIP contains both project modes:
Python API entrypoint `main.py` and standalone HTML/JS entrypoints `index.html`
and `main.js`. The packager embeds `styles.css`, compiles the browser modules,
and inlines preview assets. The HTML/JS page does not fetch nested modules,
stylesheets, or JSON assets. Its interactive inventory and held-out reveal are
synthetic, while the benchmark panel shows aggregate derived-real results.

The Python smoke ZIP is a separate Python-mode project. Its `main.py` prints a
safe runtime report, runs Qiskit's local `BasicSimulator` smoke test, and runs
the four-candidate synthetic p=1 QAOA demo with 512 shots. It never discovers
or submits a remote backend job. This is the package to upload to Qollab's
Python mode when checking the current Python/Qiskit environment. Copy the
complete JSON output for review.

The Qollab HTML/JS package has been checked for loading, replay labels, and
reload/reset behavior without browser errors. It has no verified
browser-to-Python adapter, so hosted solver controls use labeled synthetic
replays. A live hosted UI run and an IonQ simulator run remain unverified. Do
not present a replay as a live backend job.

On Windows, `Launch RePack-Q.bat` creates a project-local environment, installs
the pinned dependency on first use, and opens the live local workbench. On any
platform, `python run_repackq_web.py` serves the same-origin Python API at
`http://127.0.0.1:8000/`; this local app does not submit a Qollab or IonQ job.
