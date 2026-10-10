# RePack-Q

**Mission-Aware Quantum Recommissioning of Second-Life EV Batteries**

Match batteries by how they will age, not just how they look today.

RePack-Q is a hybrid optimization experiment for selecting a fixed-size series string from retired lithium-ion cells. It uses public longitudinal battery data, compares Qiskit QAOA with strong classical baselines, and evaluates held-out future capacity imbalance. It does not claim quantum speedup, predict certified pack lifetime, or determine whether a cell is safe to deploy.

The repository includes a read-only raw-data inspector and a streaming preprocessing pipeline for the primary Deep Sorting battery dataset. The generated real-data trajectories stay local because the Zenodo record does not state a redistribution license. The verified local Qiskit smoke path is in `src/repackq/quantum/qiskit_compat.py`. Qollab's project runtime and browser-to-Python invocation still need a user-run environment probe; see `DECISIONS.md`, `scripts/qollab_runtime_probe.py`, and [the Qollab spike instructions](docs/QOLLAB_SPIKE.md) before wiring the UI to a platform-specific API.

## Development setup

Use Python 3.10 or newer and install the pinned Qiskit dependency:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the deterministic local simulator smoke test and import check:

```sh
PYTHONPATH=src python -m repackq.api
PYTHONPATH=src python -m unittest discover -s tests -v
```

Serve the environment-check page locally with:

```sh
python3 -m http.server 8000 --directory web
```

Then open `http://localhost:8000`. A plain local browser does not provide the Qollab Python bridge; the page reports this until a verified Qollab adapter is connected. No external credentials or network access are required for the local Qiskit smoke test.

## Primary dataset preprocessing

Download the official `Second_life_phase.zip` from [Zenodo record 10.5281/zenodo.14859405](https://doi.org/10.5281/zenodo.14859405) into `data/raw/`, then run:

```sh
python src/scripts/inspect_dataset.py --raw-root data/raw --phase second_life --summary
python src/scripts/preprocess_primary.py \
  --raw-root data/raw/Second_life_phase.zip \
  --phase second_life \
  --nominal-capacity 2.4 \
  --output data/processed/trajectories.json
```

The inspector scans raw rows without changing them. Preprocessing also reads ZIP files without extraction and writes `trajectories.json`, `provenance.json`, and `preprocessing_summary.json`. See [data/README.md](data/README.md) for sampling, schema, and redistribution details. The generated cell-level observations are local derived data and must not be redistributed while the dataset license remains unspecified.

## Task 3: trajectory forecasts and retrospective pools

The classical modeling layer uses the default `pv_tou` mission (200-cycle
horizon, pack size 4, minimum SOH 0.50). It fits a weighted linear regression
to the latest eight valid capacity diagnostics (minimum four), clamps positive
fade slopes to zero, clamps predictions to `[0, current capacity]`, and reports
a residual-based uncertainty proxy. `frequency_response` is exposed only as an
experimental placeholder: it uses the same model and weights and has no
frequency-response-specific degradation calibration.

Prediction functions accept only a history sequence and reject any observation
after the decision cycle. `split_history_future` creates separate history and
held-out sequences; `lookup_future_truth` accepts only the future side. Series
pack metrics include weakest-cell usable capacity, capacity spread/CV,
resistance spread, predicted divergence, observed future divergence, and the
observed future bottleneck.

After preprocessing the real dataset, predictor quality can be summarized with:

```sh
PYTHONPATH=src python src/scripts/evaluate_predictor.py \
  --input data/processed/trajectories.json \
  --output data/processed/prediction_evaluation.json
```

Generate three or more seeded retrospective candidate pools with:

```sh
PYTHONPATH=src python src/scripts/build_demo_pools.py \
  --input data/processed/trajectories.json \
  --output data/processed/demo_pools.json
```

The pool builder requires `real` or `derived-real` input and refuses the
synthetic UI fixture. It chooses a decision cycle with the largest eligible
cell count unless `--decision-cycle` is supplied. The default demo pool is the
seeded pool whose predicted pack divergence is nearest the median across the
predeclared pool set; held-out outcomes do not select it. Generated pool files
contain held-out future observations and are ignored by Git along with the
processed cell trajectories because redistribution terms are unresolved.

## Task 4: matching objective and classical solvers

`src/repackq/optimization/` implements pool-local median/IQR normalization
(with z-score and constant-feature fallbacks), the `current_only` and
`trajectory_aware` objective modes, the fixed-cardinality QUBO, and the exact
`x = (1 - Z) / 2` Ising mapping. Missing resistance or temperature values stay
missing and omit only the affected pair term. The current-only builder does
not normalize or score forecast capacity or uncertainty. QUBO cardinality
penalties are calibrated by exhaustive small-instance enumeration, and the
exact solver checks that the penalized global minimum is feasible.

The classical comparison uses SOH sorting, multi-seed compatibility greedy,
fixed-cardinality swap simulated annealing, and exact enumeration. For a real
retrospective comparison, first generate `data/processed/demo_pools.json` with
the Task 3 command above, then run:

```sh
PYTHONPATH=src python src/scripts/compare_classical.py \
  --input data/processed/demo_pools.json \
  --objective-mode trajectory_aware
```

When that local real-data export is absent, the CLI uses the checked-in
`synthetic-fixture` solely to demonstrate the solver path and labels that
output as non-scientific. Select `--objective-mode current_only` to compare
the present-state formulation with the trajectory-aware formulation under
the same candidate pool.

## Task 5: Qiskit QAOA engine

The QAOA engine verifies the QUBO-to-Ising mapping exhaustively for `N <= 12`,
builds the diagonal cost operator and p-layer X-mixer circuit, and optimizes
parameters with local Qiskit Statevector evaluations. It uses SciPy COBYLA
when available and includes a dependency-light p=1 grid/refinement fallback.
The final measured circuit is transpiled and submitted once through an injected
backend; the local demo uses Qiskit's bundled `BasicSimulator` and needs no
credentials.

After generating a real or derived-real pool export with the Task 3 commands,
run the default `N=8`, `K=4`, 1024-shot experiment locally:

```sh
PYTHONPATH=src python src/scripts/run_qaoa_demo.py \
  --input data/processed/demo_pools.json
```

The script compares the best feasible measured state against exact enumeration
and labels the pool's data classification. It refuses synthetic fixtures for
this scientific run. `run_qaoa()` also accepts a Qiskit-compatible backend
object from a host application; the Qollab runtime entry point is documented in
[docs/QOLLAB_SPIKE.md](docs/QOLLAB_SPIKE.md).

For a Qollab Python-runner integration check, the root `main.py` automatically
runs `run_task5_toy_demo()` on a four-cell synthetic instance using Qiskit's
local `BasicSimulator`, then prints the complete result as JSON. This path is
for runtime validation only; it does not submit a Qollab or IonQ job and does
not replace the N=8/K=4 scientific run above. It needs Qiskit core only; the
Qiskit Algorithms, Qiskit Optimization, and visualization add-ons are not used.

## Task 6: reproducible benchmark

The fixed 20-seed Task 6 configuration is in
[`configs/task6_benchmark.json`](configs/task6_benchmark.json). After preprocessing
the primary dataset, run the complete local comparison with:

```sh
PYTHONPATH=src python src/scripts/run_benchmarks.py \
  --input data/processed/trajectories.json \
  --config configs/task6_benchmark.json
```

The command resumes from a fsynced JSONL checkpoint in
`data/processed/benchmark/`, writes full local aggregate outputs there, creates
small replay assets under `web/data/benchmark/`, and regenerates
[`docs/RESULTS.md`](docs/RESULTS.md). It runs SOH sorting, greedy, simulated
annealing, exact enumeration, and local p=1 QAOA, plus an exact current-only vs
trajectory-aware ablation. The web export contains three trials chosen by the
predeclared seed order and candidate size; each row contains aggregate pack
metrics, with no cell identifiers or snapshot values.

The full canonical trajectory asset stays local because dataset redistribution
terms are unspecified. Benchmark metadata records that license state and marks
the web export as aggregate-only. Rerun the command locally to regenerate the
metrics from the source asset. No Qollab backend is used by this command.

## Repository map

- `src/repackq/` — Python package, Qiskit compatibility layer, and QAOA engine.
- `src/scripts/` — dataset inspection, preprocessing, predictor evaluation, candidate-pool, classical solver comparison, local QAOA demo, and benchmark CLIs.
- `configs/task6_benchmark.json` — fixed benchmark seeds and solver settings.
- `web/data/benchmark/` — small aggregate-only benchmark replay assets.
- `web/` — optional, zero-build environment-check page; Qollab's Python run uses the root `main.py` entry point.
- `scripts/` — Qollab runtime introspection probe.
- `tests/` — Qiskit operator/circuit/bit-order and QAOA coverage, dataset adapter coverage, Task 3 leakage/prediction/trial metrics, Task 4 optimization, and Task 6 benchmark exports/checkpoint coverage.
- `data/raw/` — ignored location for downloaded raw datasets; no raw data is included.
- `data/processed/` — local generated trajectories, provenance, and QA report; cell-level trajectories and the per-file QA report are ignored by Git because redistribution terms are unresolved.
- `data/fixtures/synthetic_demo.json` — clearly labeled eight-cell synthetic fixture for UI development, not scientific results.
- `tests/fixtures/` — clearly synthetic adapter fixtures, not benchmark observations.

## License and attribution

The project is licensed under MIT. Dataset and platform references are listed in [ATTRIBUTION.md](ATTRIBUTION.md). The required attribution is: **This effort is supported by Qollab & IonQ**.
