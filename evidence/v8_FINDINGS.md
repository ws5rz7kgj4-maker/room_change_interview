# Identity-verifier development diagnosis

Date: 6 November 2026.

## Outcome

Twelve new development fits completed. No tested tree/mixture candidate passed the frozen validation resource gate, so no new GPU feature generation, calibration or confirmation test was run. The unchanged v7 ordinary model remains the usable candidate. This report establishes no new test-performance improvement.

## Which hard-training component caused trouble?

| Condition | Mean validation BCE (lower is better) | Candidate-link AP (%) | Mean Brier score (lower is better) |
|---|---:|---:|---:|
| Frozen v7 ordinary training | 0.54942 | 84.51 | 0.18728 |
| Frozen v7 weights + ranking | 0.63511 | 78.06 | 0.22528 |
| Hard-example weights only | 0.56782 | 84.58 | 0.19561 |
| Global ranking only | 0.60540 | 79.77 | 0.21173 |
| Boosted trees, depth 2 | 0.59408 | 82.72 | 0.20349 |
| Boosted trees, depth 3 | 0.59028 | 83.32 | 0.20293 |

Removing ranking while retaining hard weights changes validation AP from 78.06% to 84.58%. Ranking alone yields 79.77%, compared with 84.51% for ordinary training.

In this controlled setup, the current global-ranking objective is the main source of reduced score discrimination. Weighting alone roughly preserves ranking while worsening probability-loss/Brier scores. The experiment does not show that weighting improves deployment, or that all ranking losses are harmful.

AP is average precision among the same fixed expanded candidate links, with case/layout weights. It summarizes ranking over thresholds. It is not the held-out precision of an accepted-link operating point, not F1, and not end-to-end 3D change-detection accuracy. These validation cases also select checkpoints, so these are development diagnostics rather than an independent confirmation.

## Why the proposed replacement was not advanced

The best tree depth was depth3, with mean validation BCE 0.59028. The ordinary verifier achieved 0.54942. The selected tree fraction was 0.00; consequently the selected combination is exactly the old ordinary verifier.

| Tree fraction | Mean validation BCE |
|---:|---:|
| 0.00 | 0.54942 |
| 0.25 | 0.55040 |
| 0.50 | 0.55722 |
| 0.75 | 0.57007 |
| 1.00 | 0.59028 |

The prespecified gate required a BCE reduction of at least 0.005. The observed reduction was zero. This gate controls whether to spend fresh confirmation data; it is not an assertion that BCE perfectly captures the final precision/recall objective. Only two declared tree configurations were tested, so this does not establish a general disadvantage of boosted trees.

## Per-seed development results

| Seed | Condition | Validation BCE | Candidate-link AP (%) |
|---:|---|---:|---:|
| 42 | Frozen v7 ordinary training | 0.54640 | 84.55 |
| 42 | Frozen v7 weights + ranking | 0.63483 | 77.58 |
| 42 | Hard-example weights only | 0.56602 | 84.18 |
| 42 | Global ranking only | 0.59427 | 79.92 |
| 42 | Boosted trees, depth 2 | 0.59007 | 82.70 |
| 42 | Boosted trees, depth 3 | 0.58024 | 84.06 |
| 43 | Frozen v7 ordinary training | 0.54591 | 84.53 |
| 43 | Frozen v7 weights + ranking | 0.64202 | 77.05 |
| 43 | Hard-example weights only | 0.56497 | 85.13 |
| 43 | Global ranking only | 0.61678 | 79.60 |
| 43 | Boosted trees, depth 2 | 0.59353 | 82.87 |
| 43 | Boosted trees, depth 3 | 0.59460 | 83.36 |
| 44 | Frozen v7 ordinary training | 0.55595 | 84.45 |
| 44 | Frozen v7 weights + ranking | 0.62847 | 79.55 |
| 44 | Hard-example weights only | 0.57247 | 84.44 |
| 44 | Global ranking only | 0.60514 | 79.80 |
| 44 | Boosted trees, depth 2 | 0.59865 | 82.59 |
| 44 | Boosted trees, depth 3 | 0.59600 | 82.55 |

## What the evidence suggests next

The failed ranking term compared extreme positives and negatives across unrelated training layouts within a category. A plausible next hypothesis is that this overemphasized difficult visual ambiguity instead of resolving actual competitors for a particular observed object. That mechanism has not been isolated by this experiment. A follow-up should compare local within-scene competitors and modest auxiliary-loss strength against ordinary BCE, selecting on development evidence and confirming on new scenes. Do not continue increasing the current global-ranking pressure.

## Reproducibility and limits

All 27 stored weight files (including three selected-tree aliases), all six core source hashes, and input/policy/selection hashes were verified. Twelve separate reproduction fits reproduced every new neural state/tree, full history, diagnostic and model/mixture selection exactly. CPU reproduction took 171.32 seconds.

Both user-facing inference commands were run and their JSON outputs compared exactly. The default inference remains the unchanged v7 ordinary model with its previous frozen cutoff. Experimental scores are available separately; no new acceptance rule is invented. The example is a training case with regenerated RGB frames and cached evidence.

Only the existing 96 training layouts and 24 validation layouts were used for fitting/selection. The 576 augmented training cases come from original plus two candidate-drop variants of 192 material-paired cases. Former calibration/test feature tables and fresh confirmation data were not used. Historical frozen policies are retained for the existing-model example only.

This remains synthetic observed-instance association with privileged simulator masks/grouping and five shared procedural families. No real-phone-video, reconstruction, semantic-language, arbitrary-overlap or published-baseline superiority claim is supported. The official SceneDiff test remains unopened.

See README.md for CPU commands, code layout, weights and input/output examples. The protocol retains the unexecuted conditional GPU/test plan for transparency; those test files and results do not exist.
