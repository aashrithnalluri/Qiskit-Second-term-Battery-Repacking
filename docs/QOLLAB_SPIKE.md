# Qollab Python runner

Qollab runs Python projects from a root-level `main.py`. This project uses that
entry point to run the Task 5 implementation directly; it does not depend on a
browser-to-Python bridge or an interactive console.

## Run the Task 5 check

Upload a Python package ZIP with these root entries:

- `main.py`
- `requirements.txt`
- `repackq/` (at the ZIP root, not under `src/`)
- `scripts/__init__.py`
- `scripts/qollab_runtime_probe.py`

From PowerShell in the project folder, create or refresh that package with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package_qollab_task5.ps1
```

The script writes `qollab-task5-python.zip` beside the project files.

Run `main.py` using Qollab's Python runner. It prints one JSON report with the
Qiskit runtime capabilities and the results of a four-cell, K=2 synthetic
QAOA run on Qiskit's local `BasicSimulator`. Share the complete JSON output.

## Dependencies and execution scope

The Qollab ZIP places the Python package at its root so the project loader can
resolve the explicit `repackq.*` imports without a runtime-added `src` search
path. The repository itself retains its normal `src/` layout.

The implementation uses Qiskit core (`QuantumCircuit`, `SparsePauliOp`,
`Statevector`, `transpile`, and `BasicSimulator`). It has its own p=1 QAOA
parameter optimizer and does not require the Qiskit Algorithms or Qiskit
Optimization add-on packages. It does not draw circuits, so Qiskit
Visualizations is also unnecessary. The other optional libraries in Qollab's
list are unrelated to this check.

The optimizer uses a deterministic grid/refinement method, so SciPy is not
required. The run uses synthetic cells only and does not submit a Qollab or
IonQ backend job. If Qiskit core is unavailable in the runner, the JSON report
will say which import failed; install the platform's Qiskit 2.x core runtime
before retrying.

## Qollab runtime validation

Validated with Qollab's Python runner on Qiskit 2.5.2. The p=1, four-qubit,
K=2 run used 512 `BasicSimulator` shots and one local sampling call. Exhaustive
QUBO mapping verification passed. The best measured feasible sample matched
the exact optimum (`TOY-0`, `TOY-1`) with zero objective gap; feasible sampling
mass was 0.6074 and exact-optimum sampling mass was 0.2441. The report also
identified an infeasible cardinality-1 sample, as expected from the raw counts.

This validates the Qollab Python runtime integration and Task 5 execution
path. It is a synthetic runtime check, not a battery-data result, and no remote
Qollab or IonQ backend was used.
