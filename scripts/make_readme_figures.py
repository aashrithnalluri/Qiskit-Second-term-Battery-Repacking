"""Render README / project-page figures from checked-in JSON assets.

Usage (needs matplotlib, which is not a runtime dependency):
    python -m pip install matplotlib
    python scripts/make_readme_figures.py

Every number drawn here is read from the repository's checked-in JSON:
the aggregate derived-real benchmark summary and the synthetic UI fixture.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"

# Palette shared with web/styles.css
PAPER = "#f4f4ec"
SURFACE = "#fffefa"
INK = "#17251d"
INK_SOFT = "#46554b"
MUTED = "#5d6b61"
LINE = "#dce1d7"
FOREST = "#234f38"
FOREST_DEEP = "#153b2a"
LEAF = "#d8ec6a"
LEAF_DARK = "#a6c342"
MINT = "#e7f0e5"
BLUE = "#7aa7be"
CLAY = "#c0694f"

DPI = 200

plt.rcParams.update(
    {
        "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 11,
        "axes.edgecolor": LINE,
        "axes.labelcolor": INK_SOFT,
        "axes.titlecolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
    }
)


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def save(fig, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=DPI)
    plt.close(fig)
    print(f"wrote docs/assets/{name}")


def tag(ax, text: str, *, x: float = 1.0, y: float = 1.02, ha: str = "right") -> None:
    ax.text(
        x, y, text, transform=ax.transAxes, ha=ha, va="bottom", fontsize=8.5,
        color=FOREST, bbox=dict(boxstyle="round,pad=0.35", fc=MINT, ec="none"),
    )


def title(fig, main: str, sub: str) -> None:
    h = fig.get_figheight()
    fig.text(0.04, 1 - 0.18 / h, main, fontsize=17, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 1 - 0.50 / h, sub, fontsize=10.5, color=MUTED, va="top")


# --------------------------------------------------------------------------
# Brand: hero banner + thumbnail
# --------------------------------------------------------------------------

def draw_brand(fig, *, big: bool) -> None:
    ax = fig.add_axes([0, 0, 1, 1])
    W = 16
    H = W * fig.get_figheight() / fig.get_figwidth()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), W, H, color=FOREST_DEEP))

    # Qubit wires feeding a string of cells on the right
    x0, sp = (10.4, 1.0) if big else (11.3, 0.82)
    wire_y = [H * f for f in (0.20, 0.35, 0.50, 0.65, 0.80)]
    gates = [x0 + 0.55 * sp, x0 + 1.75 * sp, x0 + 2.95 * sp]
    cell_x = x0 + 3.85 * sp
    for i, y in enumerate(wire_y):
        ax.plot([x0, cell_x], [y, y], color=LEAF, alpha=0.3, lw=1.1)
        for gx, kind in zip(gates, ("H", "ZZ", "X")):
            ax.add_patch(FancyBboxPatch((gx - 0.3, y - 0.2), 0.6, 0.4,
                                        boxstyle="round,pad=0.02,rounding_size=0.08",
                                        fc=FOREST, ec=LEAF, lw=0.8))
            ax.text(gx, y, kind, color=LEAF, ha="center", va="center", fontsize=7.5, fontweight="bold")
        if i < len(wire_y) - 1:
            ax.plot([gates[1]] * 2, [y + 0.2, wire_y[i + 1] - 0.2], color=LEAF, alpha=0.5, lw=1)
        fill = (0.85, 0.5, 0.9, 0.55, 0.8)[i]
        ax.add_patch(Rectangle((cell_x, y - 0.18), 1.0, 0.36, fc="none", ec=LEAF, lw=1.0))
        ax.add_patch(Rectangle((cell_x + 0.06, y - 0.12), 0.88 * fill, 0.24,
                               fc=LEAF if fill > 0.7 else BLUE, ec="none"))
        ax.add_patch(Rectangle((cell_x + 1.0, y - 0.07), 0.09, 0.14, fc=LEAF, ec="none"))

    size = 44 if big else 40
    word = ax.text(0.85, H * 0.70, "RePack", color=PAPER, fontsize=size, fontweight="bold", va="center")
    fig.canvas.draw()
    bb = word.get_window_extent().transformed(ax.transData.inverted())
    ax.text(bb.x1, H * 0.70, "-Q", color=LEAF, fontsize=size, fontweight="bold", va="center")
    tagline = ("Match second-life batteries by how they will age,\nnot just how they look today." if big
               else "Match second-life batteries\nby how they will age,\nnot just how they look today.")
    ax.text(0.9, H * (0.42 if big else 0.40), tagline, color=PAPER, fontsize=14 if big else 13.5,
            va="center", linespacing=1.45)
    ax.text(0.9, H * 0.16, "Qiskit QAOA  ·  leakage-free forecasts  ·  4 classical baselines  ·  runs on Qollab"
            if big else "Qiskit QAOA  ·  real battery data  ·  runs on Qollab",
            color=LEAF, fontsize=9.5 if big else 9.5, va="center")


def fig_hero() -> None:
    fig = plt.figure(figsize=(8, 2.6))
    draw_brand(fig, big=True)
    save(fig, "hero.png")


def fig_thumbnail() -> None:
    fig = plt.figure(figsize=(6, 3.15))
    draw_brand(fig, big=False)
    save(fig, "thumbnail.png")


# --------------------------------------------------------------------------
# Problem: similar today, different tomorrow (synthetic fixture)
# --------------------------------------------------------------------------

def fig_problem() -> None:
    inv = load("repackq-demo-inventory.json")["by_horizon"]["200"]
    fut = load("repackq-demo-future.json")["by_horizon"]["200"]["by_cell"]
    decision = inv["decision_cycle"]
    series = {}
    for hist in inv["histories"]:
        cid = hist[0]["cell_id"]
        pts = [(o["cycle_index"], o["capacity_ah"]) for o in hist if o["capacity_ah"] is not None]
        pts += [(o["cycle_index"], o["capacity_ah"]) for o in fut[cid]["observations"]
                if o["capacity_ah"] is not None]
        series[cid] = sorted(pts)

    def now(cid):
        return [c for x, c in series[cid] if x <= decision][-1]

    def last(cid):
        return series[cid][-1][1]

    # Pair with the most similar capacity today and the largest future gap.
    ids = sorted(series)
    best = max(((a, b) for i, a in enumerate(ids) for b in ids[i + 1:]),
               key=lambda p: abs(last(p[0]) - last(p[1])) - 4 * abs(now(p[0]) - now(p[1])))
    a, b = sorted(best, key=last, reverse=True)

    fig, ax = plt.subplots(figsize=(8, 3.9))
    fig.subplots_adjust(left=0.09, right=0.97, top=0.74, bottom=0.14)
    title(fig, "Two cells that look alike today can age apart",
          f"Matching on present capacity alone would pair {a} and {b}. Their next 200 cycles disagree.")
    xmax = max(series[a][-1][0], series[b][-1][0])
    ax.axvspan(decision, xmax + 5, color=MINT, zorder=0)
    ax.axvline(decision, color=FOREST, lw=1, ls="--")
    for cid, color in ((a, FOREST), (b, CLAY)):
        xs, ys = zip(*series[cid])
        hx = [x for x in xs if x <= decision]
        ax.plot(xs[: len(hx)], ys[: len(hx)], color=color, lw=2.4, marker="o", ms=4)
        ax.plot(xs[len(hx) - 1:], ys[len(hx) - 1:], color=color, lw=2.4, ls=(0, (4, 2)), marker="o", ms=4)
        ax.annotate(f"{cid}  {last(cid):.2f} Ah", (xs[-1], ys[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", color=color, fontsize=10, fontweight="bold")
    ax.set_xlim(0, xmax * 1.17)
    lo, hi = ax.get_ylim()
    ax.text(decision - 4, lo + (hi - lo) * 0.04, "known at\ndecision time", ha="right", va="bottom",
            color=INK_SOFT, fontsize=9.5)
    ax.text(decision + 4, lo + (hi - lo) * 0.04, "held out: used only to score the choice", ha="left",
            va="bottom", color=FOREST, fontsize=9.5)
    ax.set_xlabel("cycle")
    ax.set_ylabel("capacity (Ah)")
    tag(ax, "synthetic illustration · not dataset records")
    save(fig, "problem.png")


# --------------------------------------------------------------------------
# Pipeline diagram
# --------------------------------------------------------------------------

def fig_pipeline() -> None:
    fig = plt.figure(figsize=(8, 3.3))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    fig.text(0.035, 0.93, "How RePack-Q picks a pack", fontsize=17, fontweight="bold", color=INK, va="top")
    fig.text(0.035, 0.85, "Classical stages build a mission-weighted QUBO, Qiskit QAOA samples it,\n"
             "and held-out future data scores every solver the same way.", fontsize=10.5, color=MUTED, va="top")

    stages = [
        ("Public data", "86 retired cells\n(Deep Sorting)", "c"),
        ("Forecast", "capacity at the\nhorizon, no leaks", "c"),
        ("Filter", "SOH floor →\nN = 8 candidates", "c"),
        ("QUBO", "choose exactly\nK = 4 balanced", "q"),
        ("QAOA", "Ising, p = 1,\none sampling job", "q"),
        ("Score", "held-out future\npack divergence", "c"),
    ]
    w, gap, y0, hgt = 2.25, 0.33, 2.15, 1.75
    x = 0.55
    centers = []
    for name, desc, kind in stages:
        q = kind == "q"
        ax.add_patch(FancyBboxPatch((x, y0), w, hgt, boxstyle="round,pad=0.02,rounding_size=0.22",
                                    fc=FOREST_DEEP if q else SURFACE, ec=FOREST_DEEP if q else LINE, lw=1.2))
        ax.text(x + 0.22, y0 + hgt - 0.38, name, fontsize=12.5, fontweight="bold",
                color=LEAF if q else INK, va="center")
        ax.text(x + 0.22, y0 + 0.62, desc, fontsize=8.4, color=PAPER if q else INK_SOFT,
                va="center", linespacing=1.35)
        centers.append(x + w / 2)
        if len(centers) < len(stages):
            ax.annotate("", (x + w + gap - 0.04, y0 + hgt / 2), (x + w + 0.04, y0 + hgt / 2),
                        arrowprops=dict(arrowstyle="-|>", color=FOREST, lw=1.4))
        x += w + gap

    # Classical baselines branch under the solver stages
    yb = 1.0
    bl, br = centers[2] + 0.25, centers[5] - 0.25
    ax.add_patch(FancyBboxPatch((bl, yb - 0.36), br - bl, 0.72,
                                boxstyle="round,pad=0.02,rounding_size=0.2", fc=MINT, ec="none"))
    ax.text((bl + br) / 2, yb, "Baselines on same pools: SOH sort · greedy · annealing · exact",
            ha="center", va="center", fontsize=8.0, color=FOREST)
    ax.plot([centers[2], centers[2]], [y0, yb], color=FOREST, lw=1)
    ax.annotate("", (bl, yb), (centers[2], yb), arrowprops=dict(arrowstyle="-|>", color=FOREST, lw=1))
    ax.plot([br, centers[5]], [yb, yb], color=FOREST, lw=1)
    ax.annotate("", (centers[5], y0), (centers[5], yb), arrowprops=dict(arrowstyle="-|>", color=FOREST, lw=1))

    ax.add_patch(Rectangle((11.2, 4.45), 0.32, 0.22, color=FOREST_DEEP))
    ax.text(11.62, 4.56, "quantum", fontsize=8.5, color=INK_SOFT, va="center")
    ax.add_patch(Rectangle((12.75, 4.45), 0.32, 0.22, fc=SURFACE, ec=LINE))
    ax.text(13.17, 4.56, "classical", fontsize=8.5, color=INK_SOFT, va="center")
    save(fig, "pipeline.png")


# --------------------------------------------------------------------------
# QAOA measured distribution (synthetic fixture replay)
# --------------------------------------------------------------------------

def fig_qaoa_samples() -> None:
    q = load("repackq-demo-qaoa-replay.json")
    counts = q["raw_counts"]
    shots = q["shots_observed"]
    k = q["best_feasible_sample"]["cardinality"]
    n = len(next(iter(counts)))
    best = q["best_feasible_sample"]["bitstring"]
    states = [format(i, f"0{n}b") for i in range(2 ** n)]
    states.sort(key=lambda s: (s.count("1") != k, -counts.get(s, 0)))
    feas = sum(1 for s in states if s.count("1") == k)

    fig, ax = plt.subplots(figsize=(8, 3.9))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.74, bottom=0.16)
    title(fig, "What one QAOA run measures",
          f"{shots} shots over all {2 ** n} bitstrings. Each bit is one cell; "
          f"valid packs have exactly {k} ones.")
    colors = [FOREST if s.count("1") == k else LINE for s in states]
    colors = [LEAF_DARK if s == best else c for s, c in zip(states, colors)]
    ax.bar(range(len(states)), [counts.get(s, 0) for s in states], width=1.0, color=colors, lw=0)
    uniform = shots / 2 ** n
    ax.axhline(uniform, color=CLAY, lw=1.1, ls="--")
    ax.text(len(states) - 2, uniform + 0.6, f"uniform random ({uniform:.0f} per state)", color=CLAY,
            fontsize=8.5, ha="right", va="bottom")
    bi = states.index(best)
    ax.annotate(f"best valid pack {best}\n= exact optimum", (bi, counts[best]),
                xytext=(feas + 25, counts[best] + 8), fontsize=9, color=FOREST,
                arrowprops=dict(arrowstyle="-", color=FOREST, lw=0.8))
    ax.axvspan(-0.5, feas - 0.5, color=MINT, zorder=0)
    ax.text(feas / 2, ax.get_ylim()[1] * 0.97, f"{feas} valid packs\n{q['feasible_probability_mass']:.0%} of shots",
            ha="center", va="top", fontsize=9, color=FOREST)
    ax.text(feas + (len(states) - feas) / 2, ax.get_ylim()[1] * 0.97,
            f"{len(states) - feas} wrong-size selections", ha="center", va="top", fontsize=9, color=MUTED)
    ax.set_xlim(-0.5, len(states) - 0.5)
    ax.set_xticks([])
    ax.set_xlabel("bitstrings, valid packs first, each group sorted by count")
    ax.set_ylabel("shots")
    tag(ax, "synthetic fixture · Qiskit BasicSimulator · p = 1")
    save(fig, "qaoa-samples.png")


# --------------------------------------------------------------------------
# Benchmark (aggregate derived-real)
# --------------------------------------------------------------------------

METHODS = [
    ("soh_sort", "SOH sort"),
    ("compatibility_greedy", "Greedy"),
    ("simulated_annealing", "Annealing"),
    ("exact_enumeration", "Exact"),
    ("qaoa", "QAOA (p = 1)"),
]


def fig_benchmark() -> None:
    s = load("web/data/benchmark/summary.json")
    alg = s["algorithms"]
    n = s["trial_count"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
    fig.subplots_adjust(left=0.14, right=0.97, top=0.72, bottom=0.22, wspace=0.12)
    title(fig, f"Benchmark: {n} retrospective pools from real battery data",
          f"Pick K = {s['pack_size_k']} of N = {s['candidate_sizes'][0]} cells, score against the held-out "
          f"next {s['horizon_cycles']} cycles. Lower divergence = better-balanced pack.")
    ys = list(range(len(METHODS)))[::-1]
    for y, (key, label) in zip(ys, METHODS):
        r = alg[key]
        c = FOREST_DEEP if key == "qaoa" else (CLAY if key == "soh_sort" else BLUE)
        a1.plot([r["observed_opd_median"], r["observed_opd_mean"]], [y, y], color=LINE, lw=3, zorder=1)
        a1.scatter(r["observed_opd_mean"], y, s=90, color=c, zorder=3)
        a1.scatter(r["observed_opd_median"], y, s=55, facecolor=PAPER, edgecolor=c, lw=1.6, zorder=3)
        a1.text(r["observed_opd_mean"] + 0.0006, y + 0.22, f"{r['observed_opd_mean']:.4f}", fontsize=8.5,
                color=c, va="bottom", ha="center")
        a2.barh(y, r["runtime_ms_mean"], color=c, height=0.55)
        a2.text(r["runtime_ms_mean"] * 1.3, y, fmt_ms(r["runtime_ms_mean"]), va="center", fontsize=8.5,
                color=INK_SOFT)
    a1.set_yticks(ys, [lbl for _, lbl in METHODS])
    a1.set_xlabel("observed future divergence (CV)   ● mean  ○ median")
    a1.set_ylim(-0.6, len(METHODS) - 0.3)
    a2.set_xscale("log")
    a2.set_yticks([])
    a2.set_xlim(0.01, 3e4)
    a2.set_xlabel("mean runtime (ms, log)")
    a2.set_ylim(-0.6, len(METHODS) - 0.3)
    tag(a2, "derived-real · aggregate only")
    save(fig, "benchmark.png")


def fmt_ms(ms: float) -> str:
    return f"{ms / 1000:.2f} s" if ms >= 1000 else (f"{ms:.1f} ms" if ms >= 1 else f"{ms * 1000:.0f} µs")


def fig_scorecard() -> None:
    s = load("web/data/benchmark/summary.json")
    qq = s["qaoa_quality"]
    alg = s["algorithms"]
    n = s["trial_count"]
    N, K = s["candidate_sizes"][0], s["pack_size_k"]
    uniform_mass = comb(N, K) / 2 ** N
    cards = [
        (f"{qq['trials_with_feasible_sample']}/{n}", "pools where QAOA\nreturned a valid pack", None),
        (f"{round(qq['optimum_sample_rate'] * n)}/{n}", "pools where the exact\noptimum was sampled",
         f"median gap to optimum {qq['median_best_sampled_gap']:.0f}"),
        (f"{qq['mean_feasible_probability_mass']:.1%}", "of shots were\nvalid packs",
         f"uniform random: {uniform_mass:.1%}"),
        (fmt_ms(qq["mean_timings_ms"]["total_ms"]), "per QAOA run,\nlocal simulator",
         f"exact enumeration: {fmt_ms(alg['exact_enumeration']['runtime_ms_mean'])}"),
    ]
    fig = plt.figure(figsize=(8, 2.75))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    fig.text(0.035, 0.93, f"QAOA scorecard across {n} real-data pools", fontsize=17, fontweight="bold",
             color=INK, va="top")
    fig.text(0.035, 0.82, "It works end-to-end on every pool. The context lines show what the "
             "next iteration has to beat.", fontsize=10.5, color=MUTED, va="top")
    w, gap, x = 3.55, 0.27, 0.55
    for big, label, ctx in cards:
        ax.add_patch(FancyBboxPatch((x, 0.45), w, 3.2, boxstyle="round,pad=0.02,rounding_size=0.25",
                                    fc=SURFACE, ec=LINE, lw=1.1))
        ax.text(x + 0.3, 2.85, big, fontsize=25, fontweight="bold", color=FOREST_DEEP, va="center")
        ax.text(x + 0.3, 1.72, label, fontsize=9.5, color=INK_SOFT, va="center", linespacing=1.3)
        if ctx:
            ax.text(x + 0.3, 0.82, ctx, fontsize=8.5, color=CLAY, va="center")
        x += w + gap
    save(fig, "qaoa-scorecard.png")


def fig_ablation() -> None:
    s = load("web/data/benchmark/summary.json")
    ab = s["objective_ablation"]
    n = ab["valid_paired_trials"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8, 3.3), gridspec_kw=dict(width_ratios=[1, 1.25]))
    fig.subplots_adjust(left=0.1, right=0.97, top=0.70, bottom=0.18, wspace=0.35)
    title(fig, "Does forecasting future capacity help? Not yet.",
          "Both rows use exact enumeration on the same pools, so only the objective differs.")
    vals = [ab["exact_current_only_opd_mean"], ab["exact_trajectory_aware_opd_mean"]]
    labels = ["current-only", "trajectory-aware"]
    a1.bar(labels, vals, color=[BLUE, FOREST_DEEP], width=0.55)
    for i, v in enumerate(vals):
        a1.text(i, v + 0.001, f"{v:.4f}", ha="center", va="bottom", fontsize=9.5, color=INK)
    a1.set_ylim(0, max(vals) * 1.25)
    a1.set_ylabel("mean future divergence")
    wins, rest = ab["trajectory_aware_lower_opd_trials"], ab["trajectory_aware_equal_or_higher_opd_trials"]
    a2.barh([0], [wins], color=FOREST_DEEP, height=0.5)
    a2.barh([0], [rest], left=[wins], color=LINE, height=0.5)
    a2.text(wins / 2, 0, f"{wins} better", ha="center", va="center", color=PAPER, fontsize=10, fontweight="bold")
    a2.text(wins + rest / 2, 0, f"{rest} tied or worse", ha="center", va="center", color=INK_SOFT, fontsize=10)
    a2.set_xlim(0, n)
    a2.set_yticks([])
    a2.set_xlabel(f"trajectory-aware vs current-only, {n} paired pools")
    a2.spines["left"].set_visible(False)
    tag(a2, "derived-real · aggregate only")
    save(fig, "ablation.png")


def fig_equation() -> None:
    # Rendered as an image so it displays identically on GitHub and Qollab.
    with plt.rc_context({"mathtext.fontset": "cm"}):
        fig = plt.figure(figsize=(8, 0.95))
        fig.text(0.5, 0.5,
                 r"$\min_{x}\ \sum_{i<j} w_{ij}\,x_i x_j\ +\ \sum_i h_i\,x_i\ +\ "
                 r"\lambda\left(\sum_i x_i - K\right)^2$",
                 ha="center", va="center", fontsize=21, color=INK)
        save(fig, "qubo-equation.png")


# Equations for the README "The math" section, transcribed from the code:
# prediction/trajectory.py, optimization/normalization.py,
# optimization/objective.py, quantum/qiskit_compat.py, prediction/metrics.py.
EQUATIONS = {
    "forecast-fit": r"(a_i, b_i) = \mathrm{arg\,min}_{a,b}\ \sum_k \omega_k \left(C_{ik} - a - b\,(t_k - t_0)\right)^2,"
                    r"\qquad \omega_k\ \mathrm{evenly\ spaced\ in}\ [0.5,\ 1]",
    "forecast-pred": r"\hat{C}_i = \mathrm{clip}\left(C_i(t_0) + \min(b_i,\ 0)\,H,\ \ 0,\ \ C_i(t_0)\right)",
    "forecast-unc": r"u_i = \sqrt{\frac{\sum_k \omega_k r_{ik}^2}{\sum_k \omega_k}}\ \sqrt{1 + \frac{H}{\Delta t_i}},"
                    r"\qquad u_i \leq 0.25\, C_{\mathrm{nom}}",
    "normalize": r"\tilde{z}_i = \frac{z_i - \mathrm{median}(z)}{\mathrm{IQR}(z)}"
                 r"\qquad \mathrm{for}\ \ z \in \{c,\ r,\ \hat{C},\ u\}",
    "objective": r"f(x) = \sum_{i<j} x_i x_j \left[ w_C (\tilde{c}_i - \tilde{c}_j)^2 + w_R (\tilde{r}_i - \tilde{r}_j)^2"
                 r" + w_F (\tilde{p}_i - \tilde{p}_j)^2 \right] + \sum_i x_i \left( w_U \tilde{u}_i - w_H s_i \right)",
    "penalty": r"\lambda \left(\sum_i x_i - K\right)^2 = \lambda \left[ \sum_i (1 - 2K)\, x_i"
               r" + 2 \sum_{i<j} x_i x_j + K^2 \right] \qquad (x_i^2 = x_i)",
    "qubo": r"E(x) = \sum_i q_i\, x_i + \sum_{i<j} Q_{ij}\, x_i x_j + c,"
            r"\qquad \lambda = 4 \max\left(1,\ \max Q^{\mathrm{phys}}_{ij},\ \max |q^{\mathrm{phys}}_i|\right)\ \times 2^m",
    "ising": r"x_i = \frac{1 - Z_i}{2}\ \ \Rightarrow\ \ H_C = \sum_i h_i Z_i + \sum_{i<j} J_{ij} Z_i Z_j + E_0",
    "ising-coeffs": r"J_{ij} = \frac{Q_{ij}}{4}, \qquad h_i = -\frac{q_i}{2} - \frac{1}{4} \sum_{j \neq i} Q_{ij},"
                    r"\qquad E_0 = c + \frac{1}{2}\sum_i q_i + \frac{1}{4}\sum_{i<j} Q_{ij}",
    "qaoa-state": r"|\gamma, \beta\rangle = e^{-i \beta H_M}\, e^{-i \gamma H_C}\, H^{\otimes N}\, |0\rangle^{\otimes N},"
                  r"\qquad H_M = \sum_i X_i",
    "qaoa-gates": r"e^{-i\gamma h_i Z_i} = R_Z(2\gamma h_i), \qquad"
                  r" e^{-i\gamma J_{ij} Z_i Z_j} = \mathrm{CX}_{ij}\, R_Z(2\gamma J_{ij})_j\, \mathrm{CX}_{ij}, \qquad"
                  r" e^{-i\beta X_i} = R_X(2\beta)",
    "qaoa-params": r"(\gamma^*, \beta^*) = \mathrm{arg\,min}_{\gamma, \beta}\ \langle \gamma, \beta |\, H_C\, | \gamma, \beta \rangle",
    "metrics-pack": r"\mathrm{OPD}(S) = \frac{\sigma\left(\{C^{\mathrm{fut}}_i\}_{i \in S}\right)}"
                    r"{\mu\left(\{C^{\mathrm{fut}}_i\}_{i \in S}\right)}, \qquad"
                    r" \mathrm{bottleneck}(S) = \min_{i \in S} C^{\mathrm{fut}}_i",
    "metrics-solver": r"\mathrm{gap} = \max\left(0,\ f(x) - f(x^*)\right), \qquad"
                      r" P_{\mathrm{valid}} = \sum_{|x| = K} p(x), \qquad"
                      r" P_{\mathrm{uniform}} = \frac{C(8,4)}{2^8} = \frac{70}{256} \approx 27.3\%",
}


def fig_math() -> None:
    out = OUT / "math"
    out.mkdir(parents=True, exist_ok=True)
    with plt.rc_context({"mathtext.fontset": "cm"}):
        for name, tex in EQUATIONS.items():
            fig = plt.figure(figsize=(0.1, 0.1))
            fig.text(0, 0, f"${tex}$", fontsize=17, color=INK)
            fig.savefig(out / f"{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.12)
            plt.close(fig)
            print(f"wrote docs/assets/math/{name}.png")


def main() -> None:
    fig_math()
    fig_equation()
    fig_hero()
    fig_thumbnail()
    fig_problem()
    fig_pipeline()
    fig_qaoa_samples()
    fig_benchmark()
    fig_scorecard()
    fig_ablation()


if __name__ == "__main__":
    main()
