# RePack-Q demo video script

**Target length: 2 minutes 40 seconds.** Use the local workbench for live Python-backed solver interaction. The Qollab HTML/JS package currently uses synthetic fixture replays unless a verified host bridge is connected. Never describe a replay as a live QAOA run or the synthetic reveal as real battery truth.

| Time | Visual and narration |
| --- | --- |
| 0:00–0:20 | **Show two cells with similar present SOH.** “Two used cells can look alike today and still age differently. RePack-Q asks whether matching on estimated future capacity can form more balanced second-life groups.” |
| 0:20–0:43 | **Show the dataset and data-flow panel.** “The retrospective study uses the public 86-cell Deep Sorting battery dataset. At a decision cutoff, the optimizer sees historical measurements and a simple forecast. Later measurements stay held out until evaluation.” |
| 0:43–1:02 | **Build a deliberately mismatched four-cell pack in the workbench.** Point to its spread and bottleneck metrics. “The demo fixture is synthetic, so this interaction explains the workflow; it is not a measured pack recommendation.” |
| 1:02–1:30 | **Run the local Python QAOA action or show the clearly labeled QAOA replay in Qollab.** Show the QUBO-to-Ising mapping, p=1 circuit summary, backend label, and measurement probabilities. “Each of eight candidates is a binary variable. QAOA samples fixed-size selections; we rank measured feasible packs by the physical objective. Parameter search is local, followed by one sampling job.” |
| 1:30–1:49 | **Compare QAOA with greedy, annealing, exact enumeration, and SOH sort.** “On the 20-trial benchmark, QAOA found a feasible sample every time and sampled the exact optimum in 17 trials. Exact enumeration remained much faster at this small size.” |
| 1:49–2:08 | **Use the reveal control.** “This shipped UI reveal is synthetic. The scientific benchmark scored against held-out real-derived measurements locally; the app only ships aggregate trial outcomes because dataset redistribution terms are unresolved.” |
| 2:08–2:29 | **Show benchmark summary and objective ablation.** “Trajectory awareness did not improve mean observed divergence in this seed set: exact current-only averaged 0.07188 OPD, versus 0.07321 for trajectory-aware selection.” |
| 2:29–2:40 | **Close on limitations and attribution.** “These small experiments show a way to test mission-aware battery grouping with QAOA. They establish no quantum speedup, battery safety, or lifetime gain. This effort is supported by Qollab & IonQ.” |

## Recording notes

- Keep the benchmark panel and synthetic/derived-real labels visible when discussing results.
- If Qollab shows the replay, say “precomputed local BasicSimulator replay.” If the local workbench runs QAOA, name the backend shown in its result.
- Do not imply that the app contains cell-level real data or that the future-reveal fixture is from the Deep Sorting dataset.
- Keep the final video under three minutes and add captions for spoken narration.
