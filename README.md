<p align="center">
  <img src="docs/assets/hero.png" alt="RePack-Q: match second-life batteries by how they will age, not just how they look today" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-234f38"></a>
  <img alt="Qiskit 2.x" src="https://img.shields.io/badge/Qiskit-2.x-6929c4">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776ab">
  <img alt="Runs on Qollab" src="https://img.shields.io/badge/runs%20on-Qollab-d8ec6a">
  <img alt="Theme: Quantum Impact" src="https://img.shields.io/badge/theme-Quantum%20Impact-153b2a">
</p>

<p align="center">
  <b><a href="VIDEO_URL">▶ Demo video</a></b> &nbsp;·&nbsp;
  <b><a href="QOLLAB_URL">⚛ Run on Qollab</a></b> &nbsp;·&nbsp;
  <b><a href="#results">📊 Results</a></b> &nbsp;·&nbsp;
  <b><a href="docs/TECHNICAL.md">🛠 Technical reference</a></b>
</p>

---

**RePack-Q** is a hybrid quantum-classical pipeline for recommissioning retired EV battery cells. It forecasts how each cell will age, encodes "pick the most compatible *K* cells" as a QUBO, samples candidate packs with **Qiskit QAOA**, and scores every choice against **held-out future measurements from a real public battery dataset**.

### TL;DR

- **Problem.** Second-life storage packs fail at their weakest cell. Matching cells on today's state of health ignores how differently they will age.
- **Approach.** A leakage-free capacity forecast feeds a mission-weighted, fixed-size QUBO. Qiskit QAOA (p = 1) samples it, and four classical solvers (SOH sort, greedy, annealing, exact) run on the same pools.
- **Result.** QAOA returned a valid pack in **20/20** real-data pools and sampled the exact optimum in **17/20**. It also beat the industry-style SOH-sort baseline on mean future divergence. We report two findings plainly: at p = 1 the sampler is close to uniform random, and the forecast term did not yet beat a current-only objective. Both point to concrete next steps.

## The problem in one picture

<img src="docs/assets/problem.png" alt="Two synthetic cells have the same capacity at the decision cycle but diverge over the next 200 cycles" width="100%">

A series string is only as good as its weakest cell. Two cells can match today and still drift apart, and the whole pack loses usable capacity as they do. RePack-Q asks whether grouping cells on their **forecast** trajectory produces packs that stay balanced. It then tests that on real data the optimizer never saw.

## How it works

<img src="docs/assets/pipeline.png" alt="Pipeline: public data, forecast, filter, QUBO, QAOA, held-out scoring, with classical baselines on the same pools" width="100%">

1. **Data.** The [Deep Sorting of Reused Batteries](https://doi.org/10.5281/zenodo.14859405) dataset covers 86 NMC/graphite cells over a 30-month aging campaign. We extract diagnostic capacity, resistance and temperature summaries.
2. **Forecast without leakage.** A weighted linear fit to each cell's recent capacity predicts its capacity at the mission horizon. Prediction functions reject any observation after the decision cycle (enforced by `tests/test_no_leakage.py`).
3. **QUBO.** For binary choices $x_i$ (cell *i* in the pack), we minimize pairwise mismatch in normalized present capacity, resistance and forecast capacity, plus uncertainty and health terms. A calibrated penalty enforces exactly *K* cells:

$$
\min_{x\in\{0,1\}^N}\; \sum_{i<j} w_{ij}\,x_i x_j \;+\; \sum_i h_i\,x_i \;+\; \lambda\Big(\sum_i x_i - K\Big)^2
$$

4. **QAOA.** The QUBO maps to an Ising Hamiltonian via $x_i = (1 - Z_i)/2$; the mapping is verified exhaustively for N ≤ 12. Parameters are optimized on an ideal Statevector. The measured circuit is then transpiled for the backend you pick in Qollab and sent as **one sampling job**.
5. **Score.** Each solver's pack is scored on the **held-out** future capacities: observed pack divergence (CV), bottleneck capacity, objective gap and runtime.

<img src="docs/assets/qaoa-samples.png" alt="Histogram of one QAOA run's 1024 shots, valid 4-cell packs highlighted, best valid pack equals the exact optimum" width="100%">

## Run it

### On Qollab (recommended for judges)

1. Open the **[RePack-Q project on Qollab](QOLLAB_URL)** in Chrome, Edge, Brave or Firefox. Safari can't run Qollab projects yet.
2. Press **Run** and pick a **free simulator**.
3. Build a pack in the workbench, compare the classical solvers, then click **Run QAOA**. Use **Reveal future** to score your choice.

### Locally

```sh
python -m venv .venv && . .venv/bin/activate
python -m pip install -r requirements.txt
python run_repackq_web.py            # opens the workbench at http://127.0.0.1:8000/
```

```sh
PYTHONPATH=src python -m unittest discover -s tests -v   # full test suite
```

On Windows, double-click `Launch RePack-Q.bat`. Dataset preprocessing, the 20-pool benchmark, and Qollab packaging are covered in **[docs/TECHNICAL.md](docs/TECHNICAL.md)**.

## Results

Twenty fixed-seed pools from the real dataset, each choosing **K = 4 of N = 8** cells at cycle 16 and scored on the held-out next 200 cycles. Full tables and provenance hashes are in [docs/RESULTS.md](docs/RESULTS.md).

<img src="docs/assets/benchmark.png" alt="Mean and median observed future divergence and runtime for SOH sort, greedy, annealing, exact and QAOA" width="100%">

**Optimizing compatibility beats sorting by SOH.** Every QUBO-based solver, QAOA included, produced better-balanced packs on average than the SOH-sort baseline (mean divergence 0.0762 for QAOA and 0.0732 for exact vs 0.0767 for SOH sort).

<img src="docs/assets/qaoa-scorecard.png" alt="QAOA scorecard: 20 of 20 valid packs, 17 of 20 optimum sampled, 29.3 percent valid shots vs 27.3 percent uniform, 1.51 s vs 4.3 ms exact" width="100%">

**QAOA runs end-to-end on every pool.** It returns valid packs every time and hits the exact optimum in 17 of 20 pools. Our own check: at p = 1 with a standard X mixer, valid-pack shot mass (29.3%) sits just above uniform random (27.3%). The **search over packs** is doing most of the work, not amplitude concentration. That gives a clear target for the next iteration (see below). At N = 8, exact enumeration is far faster. **No quantum speedup is claimed.**

<img src="docs/assets/ablation.png" alt="Ablation: exact current-only mean divergence 0.0719 vs trajectory-aware 0.0732; trajectory-aware better in 7 of 20 pools" width="100%">

**The forecast term didn't help yet.** With the solver held fixed (exact enumeration), adding forecast capacity to the objective improved balance in 7/20 pools and was tied or worse in 13/20. We publish this negative result because the leakage-free evaluation exists to catch exactly this kind of thing.

| Method | Mean future divergence ↓ | Mean bottleneck (Ah) ↑ | Mean runtime |
|---|---:|---:|---:|
| SOH sort | 0.07672 | 1.460 | 0.02 ms |
| Greedy | 0.07321 | 1.435 | 2.3 ms |
| Simulated annealing | 0.07321 | 1.435 | 69 ms |
| Exact enumeration | 0.07321 | 1.435 | 4.3 ms |
| **QAOA, best sampled valid pack** | 0.07620 | 1.429 | 1.51 s |

Predictor check across 4,642 held-out forecasts: MAE **0.115 Ah**, median absolute error **5.6%**.

## What we learned → what's next

| Finding | Next step |
|---|---|
| p = 1 QAOA with an X mixer spends ~70% of shots on wrong-size packs | **Constraint-preserving XY mixer + Dicke-state start**, so every shot is a valid pack. Then deeper p and warm-started angles |
| Forecast term didn't beat current-only matching | Stronger degradation predictor (resistance growth, temperature), larger pools, multiple decision cycles |
| N = 8 is trivially enumerable | Scale to N = 16–24, where enumeration stops being free, and compare against the same classical baselines |
| IonQ submission from Qollab's browser runtime is blocked by its no-POST policy | Run the same circuit through a supported server-side IonQ path. The pipeline already submits one job per run |

## Limitations

- Retrospective study on one public dataset. The 20 pools are draws from one inventory and may overlap. Results are descriptive, not significance tests.
- The 200-cycle horizon is in dataset cycle indices. It is not calendar time or a real household load trace.
- The interactive app ships a **synthetic** 8-cell fixture. The dataset's license doesn't state redistribution terms, so real cell-level data stays local and only aggregate benchmark results are published.
- Not a safety tool, a lifetime guarantee, or evidence of quantum advantage. All quantum results come from simulators. No IonQ hardware result is claimed.

## Repository map

| Path | What's there |
|---|---|
| `src/repackq/` | Data adapters, leakage-free prediction, QUBO/objective, classical solvers, Qiskit QAOA engine, benchmark, UI API |
| `src/scripts/` | CLIs: inspect, preprocess, evaluate predictor, build pools, compare solvers, QAOA demo, benchmark |
| `web/` | Zero-build browser workbench, synthetic fixture, aggregate benchmark replay |
| `index.html`, `main.js`, `main.py` | Qollab entry points (HTML/JS ↔ Python bridge) |
| `tests/` | Leakage, QUBO↔Ising mapping, QAOA, solvers, dataset adapter, benchmark, UI API |
| `scripts/make_readme_figures.py` | Regenerates every figure in this README from checked-in JSON |
| `docs/` | [Results](docs/RESULTS.md) · [Technical reference](docs/TECHNICAL.md) · [Qollab notes](docs/QOLLAB_SPIKE.md) · [Demo script](docs/DEMO_SCRIPT.md) |

## Originality, AI assistance and sources

Pre-build work consisted of problem selection, dataset research and implementation planning. Project implementation, integration, experiments, UI and submission materials were developed during the hackathon build window. Codex was used as an AI coding assistant for implementation, debugging and documentation. Claude Code was used for the final documentation, figure-generation script and README/project-page design. The project-specific data pipeline, optimization model, QAOA engine, benchmark and interface are implemented in this repository. The associated Deep Sorting code release was consulted as a schema and sampling reference only; no code from it was copied. External data and software are listed in [ATTRIBUTION.md](ATTRIBUTION.md).

## License and attribution

MIT. See [LICENSE](LICENSE). Dataset terms are separate from the software license.

**This effort is supported by Qollab & IonQ**
