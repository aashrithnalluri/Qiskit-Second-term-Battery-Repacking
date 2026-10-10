"""Qollab Python entry point and callable API for the RePack-Q QAOA demo.

Running this file executes a small, synthetic Task 5 QAOA experiment on
Qiskit's local BasicSimulator. It does not need a Python console, Qollab bridge,
credentials, or a remote backend.
"""

import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

def _find_project_root() -> Path:
    """Locate the uploaded project when the host runner omits ``__file__``."""

    candidates: list[Path] = []
    entrypoint = globals().get("__file__")
    if entrypoint:
        candidates.append(Path(entrypoint).resolve().parent)
    candidates.append(Path.cwd().resolve())
    for entry in sys.path:
        if entry:
            candidates.append(Path(entry).resolve())

    visited: set[Path] = set()
    for candidate in candidates:
        for root in (candidate, *candidate.parents):
            if root in visited:
                continue
            visited.add(root)
            if (root / "repackq").is_dir() or (root / "src" / "repackq").is_dir():
                return root
    # Qollab may expose project files through its working directory without
    # placing them on disk; keep this fallback explicit for a useful import
    # error from the package import below.
    return Path.cwd().resolve()


_PROJECT_ROOT = _find_project_root()
_SOURCE_ROOT = (
    _PROJECT_ROOT / "src"
    if (_PROJECT_ROOT / "src" / "repackq").is_dir()
    else _PROJECT_ROOT
)
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(_SOURCE_ROOT))

from repackq.config import PV_TOU_MISSION
from repackq.models import CandidatePool, CellSnapshot
from repackq.optimization.objective import build_optimization_instance
from repackq.optimization.solvers import exact_enumeration
from repackq.quantum.engine import run_qaoa
from repackq.quantum.qiskit_compat import get_capabilities, run_smoke_test
from scripts.qollab_runtime_probe import runtime_report


def _make_toy_pool() -> tuple[CandidatePool, Any]:
    """Build a clearly synthetic four-cell, K=2 instance for runtime checks."""

    mission = replace(PV_TOU_MISSION, pack_size_k=2)
    snapshots = tuple(
        CellSnapshot(
            cell_id=f"TOY-{index}",
            protocol_id="qollab-runtime-check",
            cycle_index=20,
            capacity_ah=1.20 + index * 0.04,
            nominal_capacity_ah=2.4,
            soh=(1.20 + index * 0.04) / 2.4,
            internal_resistance_ohm=0.07 + index * 0.005,
            temperature_c=None,
            recent_capacity_slope_ah_per_cycle=-0.0001 * (index + 1),
            predicted_capacity_ah=1.18 + index * 0.03,
            prediction_uncertainty_ah=0.002 + index * 0.0004,
            horizon_cycles=mission.horizon_cycles,
            source_dataset="synthetic_qollab_runtime_check",
        )
        for index in range(4)
    )
    pool = CandidatePool(
        pool_id="synthetic-qollab-task5-smoke",
        decision_cycle=20,
        horizon_cycles=mission.horizon_cycles,
        candidate_ids=tuple(snapshot.cell_id for snapshot in snapshots),
        snapshots=snapshots,
        future_truth=None,
        seed=7,
    )
    return pool, mission


def run_task5_toy_demo(
    backend: Any | None = None,
    *,
    shots: int = 512,
    simulator_seed: int = 20261010,
) -> dict[str, Any]:
    """Run Task 5 QAOA end to end on a tiny synthetic instance.

    The default backend is local Qiskit BasicSimulator. Supplying ``backend``
    is an explicit caller choice; this function never creates credentials or
    discovers a Qollab provider on its own.
    """

    pool, mission = _make_toy_pool()
    instance = build_optimization_instance(pool, mission=mission)
    exact = exact_enumeration(instance)
    exact_bits = [
        tuple(1 if bit_index in selected else 0 for bit_index in range(instance.n))
        for selected in exact.metadata["tied_optima"]
    ]
    result = run_qaoa(
        instance,
        backend,
        shots=shots,
        optimizer_mode="grid",
        max_evaluations=121,
        exact_optimal_bitstrings=exact_bits,
        simulator_seed=simulator_seed if backend is None else None,
    )
    report = result.to_dict()
    report.update(
        {
            "data_classification": "synthetic",
            "purpose": "Task 5 runtime validation only; not a battery-data result.",
            "exact_best_cell_ids": [
                pool.candidate_ids[index]
                for index in exact.selected_indices
            ],
        }
    )
    return report


def qollab_runtime_probe(namespace: Any | None = None) -> dict[str, Any]:
    """Return safe runtime facts and inspect names in the caller's namespace."""

    if namespace is None:
        try:
            namespace = sys._getframe(1).f_globals
        except (AttributeError, ValueError):
            namespace = None
    return runtime_report(namespace)


def main() -> None:
    """Run and print the synthetic Task 5 QAOA check for Qollab's Python runner."""

    report: dict[str, Any] = {
        "application": "RePack-Q",
        "status": "starting",
        "capabilities": get_capabilities(),
        "execution_mode": "local Qiskit BasicSimulator; synthetic four-cell, K=2 instance",
        "qollab_backend_job_submitted": False,
    }
    try:
        result = run_task5_toy_demo()
    except Exception as exc:
        report["status"] = "failed"
        report["task5_qaoa"] = {
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    else:
        report["task5_qaoa"] = result
        report["status"] = "completed" if result["feasible"] else "completed_without_feasible_sample"
    print(json.dumps(report, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
