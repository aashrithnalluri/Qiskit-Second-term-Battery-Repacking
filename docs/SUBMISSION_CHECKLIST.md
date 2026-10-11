# RePack-Q submission checklist

## Project and evidence

- [x] MIT `LICENSE` is present.
- [x] Required attribution text is present: **This effort is supported by Qollab & IonQ**.
- [x] Qollab project-page copy is ready in [`QOLLAB_PROJECT_PAGE.md`](QOLLAB_PROJECT_PAGE.md).
- [x] Benchmark results and provenance are documented in [`RESULTS.md`](RESULTS.md).
- [x] Two-to-three-minute video script is ready in [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
- [x] Run the Task 8 Python smoke ZIP in a clean Qollab Python project and retain its JSON output; Python 3.14.2/Qiskit 2.5.2 passed.
- [x] Identify and test the host-exposed local `BasicSimulator` backend (one QAOA sampling job; no remote submission).
- [x] Upload the standalone app to Qollab and verify that the page renders without browser errors.
- [x] Verify replay labels and reload/reset behavior in Qollab.
- [ ] Verify live QAOA result rendering through a Qollab browser-to-Python bridge.
- [ ] Verify the IonQ simulator path if Qollab exposes a compatible backend.
- [ ] Record and publish the public demo video; add its URL to the project page/submission.
- [ ] Publish the MIT-licensed project on Qollab.
- [ ] Submit before the hackathon deadline.

## Data and release hygiene

- [x] No raw dataset files are included.
- [x] The shipped interactive inventory and reveal are labeled synthetic.
- [x] The benchmark replay contains aggregate derived-real metrics without cell IDs or pack membership.
- [x] Dataset redistribution rights are called out as unresolved; cell-level derived data remain local.
- [x] External dataset, code-reference, Qiskit, and Qollab references are listed in [`ATTRIBUTION.md`](../ATTRIBUTION.md).
- [ ] Review the final rebuilt ZIP and Qollab page before submission.
