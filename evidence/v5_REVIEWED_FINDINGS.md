# Precision verification on top of expanded global assignment

Date: 5 November 2026.

The requested precision improvement is observed on the new test. Relative to the frozen expanded-assignment baseline, the primary verifier improves mean precision from **61.51% to 65.60%** and F1 from **73.72% to 75.32%**, at a recall cost from **91.98% to 88.49%**. This is evidence for a useful learned-verification tradeoff within this synthetic experiment, not a complete solution to incorrect associations.

## Same-test results

All methods are evaluated on the same 96 new layouts / 192 material-paired cases, with 640 true identity links per fitted seed. Metrics are micro-aggregated within each seed and then averaged over seeds 42, 43 and 44. Mean F1 is not recomputed from mean precision and recall.

| Method | Precision (%) | Recall (%) | F1 (%) | Mean TP | Mean FP | Mean FN |
|---|---:|---:|---:|---:|---:|---:|
| Original full model | 71.06 | 64.64 | 67.68 | 413.67 | 168.67 | 226.33 |
| Frozen expanded global assignment | 61.51 | 91.98 | 73.72 | 588.67 | 368.33 | 51.33 |
| Previous geometry residual | 65.18 | 83.33 | 72.91 | 533.33 | 289.67 | 106.67 |
| Original-score filter (no new training) | 61.51 | 91.98 | 73.72 | 588.67 | 368.33 | 51.33 |
| Trained pair verifier | 65.87 | 88.02 | 75.33 | 563.33 | 292.33 | 76.67 |
| Pair + existence verifier (prespecified primary) | 65.60 | 88.49 | 75.32 | 566.33 | 297.67 | 73.67 |

The primary changes are **+4.08 percentage points precision**, **-3.49 points recall**, and **+1.60 points F1**. All three fitted primary models improve both precision and F1 relative to their corresponding expanded baselines. The pair-only verifier also improves both metrics for all three seeds. Shared test layouts mean these seeds are not independent scene replications.

Historical values such as 61.74% precision and 74.08% F1 came from another test batch. Only the same-test comparisons above support this experiment's conclusions.

## Uncertainty and what contributed

The predeclared paired bootstrap uses 4,000 samples of 96 base-layout clusters, preserving both material variants and all method/seed comparisons. The primary-minus-baseline descriptive 95% intervals are:

| Metric difference | Percentage-point interval |
|---|---:|
| precision | [2.67, 5.56] |
| recall | [-5.10, -2.14] |
| f1 | [0.19, 3.05] |

The precision and F1 intervals exclude zero in this conditional analysis. This is stronger evidence for the requested tradeoff than a favorable point estimate alone. It is still one synthetic generator, conditional on fitted weights and fixed rules, without multiplicity correction or a real-world guarantee.

The simpler **pair verifier reaches 65.87% precision and 75.33% F1**. Adding explicit counterpart-existence learning changes mean F1 by **-0.02 points** relative to that control, with a **[-0.46, +0.43]-point** interval. There is no demonstrated incremental benefit from the existence branch. The result supports trained verification of expanded links; it does not justify attributing the improvement to the auxiliary existence mechanism or claiming a novel state-of-the-art method.

The untrained original-score filter chooses accept-all for all three calibration seeds and therefore reproduces the expanded baseline exactly. Under the specified criteria, a threshold on the original score did not provide the improvement achieved by the learned evidence. This does not prove that every alternative score rule would fail.

The previous residual model scores 72.91% F1, below the expanded baseline's 73.72%, on these new cases. Its preceding small advantage over expanded matching did not replicate. Relative to that previous residual, the primary verifier has a +2.40-point F1 estimate, but its [-0.08, +4.91]-point interval includes zero.

## What was removed, and what remains wrong

The primary verifier removes **70.67 false links** and loses **22.33 true links** on average per seed. Total false links fall from **368.33 to 297.67**, a **19.19% reduction**, while **96.21% of baseline true links are retained**. The pair-only verifier removes 76.00 false links and loses 25.33 true links. These filters never add a new link; their benefit is selective rejection rather than improved candidate recall or reassignment.

| Mode | Expanded baseline F1 (%) | Primary F1 (%) | Baseline mean FP | Primary mean FP |
|---|---:|---:|---:|
| Unchanged | 93.33 | 92.20 | 16.00 | 15.67 |
| Moved | 91.73 | 89.35 | 19.67 | 16.67 |
| Mixed | 72.39 | 73.92 | 95.00 | 79.33 |

The overall improvement is not uniform across change modes: unchanged and moved groups lose F1 through rejected true links, while mixed cases improve. In the all-replaced group, where there are no true links, false matches decrease from **237.67 to 186.00** for the primary method. Correct unmatched decisions rise from **0.97% to 22.50%**, but the remaining error rate is still high. Positive-class recall is undefined for this group.

Mean precision and F1 improve at each tested object count (3, 5 and 7); those subgroup estimates do not establish generalization to arbitrary counts or new asset families. Full per-seed, per-count, per-mode and material-regime results are retained in REPORT.md and summary.json.

## Practical conclusion

Keep expanded global matching as the source of high-recall candidates and add learned pair verification. The more complex existence branch remains an experimental control: the present evidence does not establish an advantage over the simpler verifier. Prioritize independent replication and better rejection of replacement cases while monitoring losses on genuine moved objects. This recommendation is informed by the present test; any subsequent confirmation must use untouched data.

The run completed six genuine fits, all with nonzero parameter changes. Replay verified all twelve weight hashes, nine calibration selections, six validation checkpoint choices and **3,456 test case/method predictions**, including complete scores, links, counts, summaries and bootstrap results. No weights, rules or measurements changed during report preparation.

## What changed

The expanded baseline remains frozen. Its all-pair scores, optional one-to-one assignment and previously calibrated cutoff are reused unchanged. A new verifier is trained to remove unsupported accepted links. It cannot add links, repair an incorrect partner by reassignment or recover links absent from that expanded baseline. It has no top-half quota.

The primary model learns both pair correctness and whether each endpoint has an observable counterpart. A shared pair encoder feeds a pair-correctness head; mean/max pooling over candidate embeddings feeds an object-existence head. The acceptance score combines pair probability with the geometric mean of the two endpoint probabilities. A pair-only trained control disables the auxiliary existence objective and inference factor. An untrained control thresholds the original score. All use the same acceptance-selection criteria.

Two deterministic, label-independent random candidate-drop versions augment each original training case. Original scores and candidate-context features are recomputed after subsetting; supervision is remapped separately. This simulates incomplete candidate coverage, not a new physical removal label. The model's unmatched output remains an association decision rather than proof of a change in the room.

## Selection and separation

The six new verifier fits reuse only the preceding 48 training layouts / 96 cases. The separate 12 validation layouts / 24 cases select checkpoints. Each training case has three versions, for 288 augmented cases. All six selected checkpoints differ from initialization. The 20 unit checks passed, covering assignment, geometric features, permutation/direction symmetry, missing counterparts, tied thresholds and subset-only filtering.

The existing 24-layout / 48-case calibration set selects thresholds. This is reused development data, not a new independent test. Selection maximizes calibration F1, subject to precision and F1 at least as high as the frozen expanded baseline, at least 90% of its recall and at least 30 accepted links. Accept-all is an explicit fallback. These criteria do not guarantee held-out behavior.

All weights and thresholds were frozen before fresh test scoring. The new test has 96 layouts / 192 material-paired cases, with counts 3, 5 and 7 and four change modes. No previous test is added to the training or calibration tables. No new test outcome chooses a checkpoint, threshold, seed or reported method. Future modifications based on this test require a new test split.

## Execution and reproduction

The planned L4 feature job waited for hardware and was canceled before execution. Identical generation/feature code and seeds were then run on one A10G. Training was separated into a CPU development job while GPU work was pending, followed by CPU evaluation of the already frozen artifacts. This is an operational scheduling change, with no model, training-data or policy change. The GPU execution note and the development archive hashes are preserved.

The first evaluation stopped when saving its first prediction: empty output directories were not stored in the development ZIP. The retry creates these directories explicitly, preserves the failed run and uses identical frozen weights, policies and test data. No algorithm or calibration change was made in response to this I/O error.

The package contains all twelve checkpoints, six training histories, nine filter-selection rules, frozen baseline rules, train/validation/calibration/test feature tables, all 3,456 test case/method predictions, tests, replay verification and a deterministic RGB example. `code/README.md` explains CPU inference, complete verification and actual retraining without a GPU or Hub token. Full new rendered inputs are separately archived under `features/raw_inputs.zip`.

## Scope

These results concern observed-instance identity association with five procedural object families and privileged simulator masks/grouping. They do not measure end-to-end input from two ordinary phone videos, shared 3D reconstruction, moved/added/removed accuracy, semantic text quality, arbitrary-overlap performance or real-world generalization. No published SceneDiff superiority is established, and its official test remains unopened. This package is a reproducible module experiment, not the complete recruitment-challenge submission.
