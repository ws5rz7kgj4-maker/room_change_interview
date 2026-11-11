# Complete same-test results

Values are percentages: micro-aggregate within each seed, then average three seeds. A and B use different test sets; do not compare their absolute scores as a longitudinal gain.

## A — v5

96 layouts, 192 material-paired cases; 640 true links per seed.

| Method | Precision | Recall | F1 | Mean TP | Mean FP | Mean FN |
|---|---:|---:|---:|---:|---:|---:|
| Original full identity head | 71.06 | 64.64 | 67.68 | 413.67 | 168.67 | 226.33 |
| Frozen expanded assignment | 61.51 | 91.98 | 73.72 | 588.67 | 368.33 | 51.33 |
| Previous geometry residual | 65.18 | 83.33 | 72.91 | 533.33 | 289.67 | 106.67 |
| Original-score filter | 61.51 | 91.98 | 73.72 | 588.67 | 368.33 | 51.33 |
| Learned pair verifier | 65.87 | 88.02 | 75.33 | 563.33 | 292.33 | 76.67 |
| Pair + existence verifier (primary) | 65.60 | 88.49 | 75.32 | 566.33 | 297.67 | 73.67 |

## B — v7

96 layouts, 192 material-paired cases; 640 true links per seed.

| Method | Precision | Recall | F1 | Mean TP | Mean FP | Mean FN |
|---|---:|---:|---:|---:|---:|---:|
| Original full identity head | 69.66 | 62.03 | 65.61 | 397.00 | 173.00 | 243.00 |
| Frozen expanded assignment | 58.71 | 87.97 | 70.42 | 563.00 | 396.00 | 77.00 |
| Previous verifier, old cutoff | 63.91 | 81.56 | 71.64 | 522.00 | 295.00 | 118.00 |
| Previous verifier, fresh policy | 70.46 | 67.55 | 68.95 | 432.33 | 181.00 | 207.67 |
| Ordinary training, precision policy (control) | 71.14 | 71.56 | 71.34 | 458.00 | 186.00 | 182.00 |
| Hard training, precision policy (primary) | 69.66 | 62.03 | 65.61 | 397.00 | 173.00 | 243.00 |
| Ordinary training, balanced policy | 68.45 | 74.38 | 71.24 | 476.00 | 220.67 | 164.00 |
| Hard training, balanced policy | 61.32 | 81.77 | 69.62 | 523.33 | 337.67 | 116.67 |

