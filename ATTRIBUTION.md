# Attribution

**This effort is supported by Qollab & IonQ**

RePack-Q uses the following external resources. The raw battery data are not
included in this repository. The independent adapter and preprocessing
pipeline cite the dataset and the public code release used to verify the raw
schema and diagnostic-cycle cadence.

- Primary battery dataset: Wang, Gao, and Tian, *Data for: Deep sorting of reused batteries for enabling long-term consistency grouping with unknown prior conditions*, Zenodo DOI [10.5281/zenodo.14859405](https://doi.org/10.5281/zenodo.14859405).
- Associated public code release, for research reference only: Zenodo DOI [10.5281/zenodo.15350607](https://doi.org/10.5281/zenodo.15350607). No code from this release has been copied into this repository.
- Dataset file/schema reference: [version 1.0.0 extraction script](https://github.com/wshuquan/Deep_sorting_of_reused_batteries/blob/v1.0.0/Feature_engineering/3_capa_trajectory_extraction.py). It is cited as a schema and sampling reference only; RePack-Q independently implements CSV parsing and summaries.
- Qiskit: the open-source quantum software development kit by IBM and its contributors. See the [Qiskit project](https://github.com/Qiskit/qiskit) and [official API documentation](https://qiskit.qotlabs.org/docs/api/qiskit).
- Qollab hackathon information: [terms](https://qollab.xyz/programs/hackathon/terms) and [how it works](https://qollab.xyz/programs/hackathon/how-it-works), as listed in `SPEC.md`. Platform-specific runtime details still require verification in Qollab.

## Literature

The research design and next steps cite the following published work. No code or text from these sources is included; the full reference list is in the [README](README.md#references).

- Martinez-Laserna et al., *Renewable and Sustainable Energy Reviews* 93 (2018), [doi:10.1016/j.rser.2018.04.035](https://doi.org/10.1016/j.rser.2018.04.035): battery second-life review.
- Severson et al., *Nature Energy* 4 (2019), [doi:10.1038/s41560-019-0356-8](https://doi.org/10.1038/s41560-019-0356-8): data-driven cycle-life prediction.
- Lucas, *Frontiers in Physics* 2 (2014), [arXiv:1302.5843](https://arxiv.org/abs/1302.5843), and Glover, Kochenberger and Du, *4OR* 17 (2019), [arXiv:1811.11538](https://arxiv.org/abs/1811.11538): QUBO and Ising formulations.
- Farhi, Goldstone and Gutmann (2014), [arXiv:1411.4028](https://arxiv.org/abs/1411.4028), and Zhou et al., *Physical Review X* 10 (2020), [arXiv:1812.01041](https://arxiv.org/abs/1812.01041): QAOA.
- Hadfield et al., *Algorithms* 12 (2019), [arXiv:1709.03489](https://arxiv.org/abs/1709.03489), and Bärtschi and Eidenbenz (2019), [arXiv:1904.07358](https://arxiv.org/abs/1904.07358): constraint-preserving mixers and Dicke states (planned next step).
- Kaufman et al., *ACM TKDD* 6(4) (2012), [doi:10.1145/2382577.2382579](https://doi.org/10.1145/2382577.2382579): data leakage and learn/predict separation.

## Originality disclosure

Pre-build work consisted of problem selection, dataset research, and implementation planning. Project implementation, integration, experiments, UI, and submission materials were developed during the hackathon build window. Codex was used as an AI coding assistant for implementation, debugging, and documentation. Claude Code was used for the final documentation, figure-generation script, and README/project-page design. Public datasets, Qiskit, and cited open-source references are used as a data source, software dependency, or research reference and are attributed. No source code from the associated Deep Sorting code release was copied.
