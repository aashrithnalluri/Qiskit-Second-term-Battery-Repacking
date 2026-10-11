# RePack-Q demo video script

**Target: 2:30** (hard limit 3:00). The video cuts between full-screen figures from `docs/assets/` and a live screen recording of the Qollab app in Chrome. Run QAOA on a **free simulator**. Never describe simulator output as IonQ hardware, or the app's synthetic fixture as real battery data.

| Time | On screen | Narration |
| --- | --- | --- |
| 0:00–0:12 | `hero.png` | "Millions of EV batteries are retiring with most of their capacity left. RePack-Q helps give them a second life as home storage." |
| 0:12–0:30 | `problem.png` | "A series pack is only as good as its weakest cell. These two cells look identical today, but over the next 200 cycles one fades much faster, and the pack fades with it. So we ask: can we match cells by how they *will* age?" |
| 0:30–0:52 | `pipeline.png` | "We use a real public dataset of 86 retired cells. A leakage-free forecast predicts each cell's future capacity. We encode 'pick the four most compatible cells out of eight' as a QUBO and map it to an Ising Hamiltonian. Qiskit QAOA samples it, and four classical solvers run on the exact same pools. Future data stays hidden until scoring." |
| 0:52–1:30 | **Live Qollab app** | Choose the mission, then hand-build a mismatched pack and point at its spread and bottleneck. Run the classical comparison. Click **Run QAOA** on the free simulator and show the measured bitstrings and feasible mass. "This inventory is a synthetic demo fixture. Each of the eight qubits is one cell; a valid pack has exactly four ones. One sampling job on Qollab's simulator gives us the distribution." Click **Reveal future**. |
| 1:30–1:45 | `qaoa-samples.png` | "Here's one run. The highlighted bars are valid packs, and the best valid pack QAOA sampled is the exact optimum." |
| 1:45–2:05 | `benchmark.png`, then `qaoa-scorecard.png` | "On 20 pools from the real dataset, every QUBO-based solver, QAOA included, built better-balanced packs than sorting by state of health. QAOA returned a valid pack in all 20 and found the exact optimum in 17. To be candid: at depth one, its valid-shot rate is close to uniform random, and exact search is faster at this size. No speedup is claimed." |
| 2:05–2:20 | `ablation.png` | "And we tested our own hypothesis. The forecast term didn't beat current-only matching yet, at 7 wins out of 20. We publish that because the held-out evaluation exists to catch exactly this." |
| 2:20–2:30 | README "What's next" table, or `hero.png` | "Next: a constraint-preserving XY mixer so every shot is a valid pack, a stronger forecaster, and larger pools. Code and data pipeline are open source under MIT. This effort is supported by Qollab and IonQ." |

## Recording checklist

- Record with macOS **Cmd-Shift-5** (whole screen or window) in **Chrome**. Safari can't run Qollab projects.
- Open the figures full-screen from `docs/assets/` (Preview, then View → Enter Full Screen) and record those segments, or drop the PNGs into iMovie/CapCut over the voiceover.
- Name the selected simulator out loud. Show the counts from your actual run rather than quoting fixed numbers.
- Export at 1080p and upload to **YouTube as Unlisted** (anyone with the link, no sign-in). Paste the URL into `README.md`, `docs/QOLLAB_PROJECT_PAGE.md` (replace `VIDEO_URL`), the Qollab project page, and the submission form.
