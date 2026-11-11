# Reviewed findings: hard-example identity training

The prespecified primary changes precision by +0.00 percentage points relative to the original full model and F1 by -4.81 points relative to expanded assignment on the same new test.

The combined point-estimate goal is not met.

| Method | Precision (%) | Recall (%) | F1 (%) |
|---|---:|---:|---:|
| Original full model | 69.66 | 62.03 | 65.61 |
| Frozen expanded assignment | 58.71 | 87.97 | 70.42 |
| Previous verifier, old cutoff | 63.91 | 81.56 | 71.64 |
| Previous verifier, fresh precision rule | 70.46 | 67.55 | 68.95 |
| New plain training, precision rule | 71.14 | 71.56 | 71.34 |
| New hard training, precision rule (primary) | 69.66 | 62.03 | 65.61 |
| New plain training, balanced rule | 68.45 | 74.38 | 71.24 |
| New hard training, balanced rule | 61.32 | 81.77 | 69.62 |

These are 192 new synthetic cases from 96 layouts, averaged across three fitted seeds after within-seed micro-aggregation. The original full model is rerun on these cases; do not substitute its historical test precision.

## Does training add value beyond changing the cutoff?

| Primary contrast | Precision difference (pp), interval | Recall difference (pp), interval | F1 difference (pp), interval |
|---|---:|---:|---:|
| Original full model | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| Frozen expanded assignment | +10.95 [+7.57, +14.31] | -25.94 [-29.98, -21.72] | -4.81 [-8.91, -0.47] |
| Previous verifier, old cutoff | +5.74 [+2.61, +8.78] | -19.53 [-23.11, -15.89] | -6.04 [-9.35, -2.50] |
| Previous verifier, fresh precision rule | -0.81 [-3.35, +1.50] | -5.52 [-8.10, -3.03] | -3.34 [-5.50, -1.18] |
| New plain training, precision rule | -1.48 [-4.64, +1.56] | -9.53 [-12.60, -6.46] | -5.74 [-8.35, -3.09] |

The hard-versus-plain F1 comparison does not establish a positive advantage: its interval does not lie entirely above zero.
Intervals are paired-layout descriptive 95% intervals, conditional on the fixed models, without multiplicity correction. Balanced variants use the same weights with maximum-calibration-F1 policies; their results are controls, not test-selected replacements for the primary.

## Frozen policy tiers

- Seed 42: primary reference_fallback; plain tier1_expanded_f1; recalibrated previous tier1_expanded_f1.
- Seed 43: primary reference_fallback; plain tier1_expanded_f1; recalibrated previous tier1_expanded_f1.
- Seed 44: primary reference_fallback; plain tier1_expanded_f1; recalibrated previous reference_fallback.

Tier 2 relaxes expanded-assignment F1 to original-model F1 on calibration. Reference fallback uses the original model and is not a learned success. Calibration targets are not test guarantees.

## What is verified

- Six new fits, three paired seeds, with hard and plain conditions sharing architecture/data/initialization/optimizer.
- Twelve weight hashes, fifteen new calibration policies, six checkpoint/mining checks and 4,608 case/method predictions replayed.
- A separate run of the supplied retrain command reproduced all six state dictionaries, complete histories and policies exactly.
- Train, validation, calibration and test layout seeds are disjoint; prior calibration/test features did not train weights.
- Core training/selection code was frozen before generation; all weights before calibration, all rules before test scoring.

## Limits

This is synthetic observed-instance association with simulator masks/grouping and five shared procedural asset families. It is not end-to-end two-phone-video 3D change detection, real-world validation, or a result above published SceneDiff. Training changes the small pair verifier, not reconstruction or the frozen backbone. The official SceneDiff test remains unopened.

Read REPORT.md for all subgroups, false-link and movement diagnostics, and every seed. Read code/README.md for inference, replay and retraining. Future method changes based on this confirmation require a new untouched test.
