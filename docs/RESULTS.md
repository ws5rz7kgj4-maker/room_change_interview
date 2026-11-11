# Results, conclusions and completed work

[中文](RESULTS.zh-CN.md) · [Complete same-test tables](../results/ALL_RESULTS.md)

## Headline evidence

| Experiment and comparison | Precision difference | Recall difference | F1 difference | Status |
|---|---:|---:|---:|---|
| A / v5 primary vs expanded assignment | +4.08 pp | -3.49 pp | +1.60 pp | Precision and F1 descriptive intervals above zero |
| A / v5 pair-only control vs expanded assignment | +4.36 pp | -3.96 pp | +1.61 pp | Precision and F1 descriptive intervals above zero |
| B / v7 ordinary-training control vs original full head | +1.48 pp | +9.53 pp | +5.74 pp | Recall/F1 intervals above zero; precision interval crosses zero |

“pp” means percentage points. Differences use unrounded values. The two experiments have different test sets. V5's primary is the pair + existence verifier; v7's primary is hard-example training, not the ordinary control.

## A: the clearest evidence for learned verification

The expanded baseline is a demanding internal comparator because it already improves F1 over the original full head on the same test: 73.72% versus 67.68%. The v5 primary improves further to 75.32%, with precision rising from 61.51% to 65.60%.

| Primary-minus-expanded metric | Estimate | Descriptive 95% interval |
|---|---:|---:|
| Precision | +4.08 pp | [+2.67, +5.56] pp |
| Recall | -3.49 pp | [-5.10, -2.14] pp |
| F1 | +1.60 pp | [+0.19, +3.05] pp |

Across seeds, it removes 70.67 false links and loses 22.33 true links on average. False links fall from 368.33 to 297.67: **19.19% fewer**. It retains **96.21%** of baseline true links. It does not create new links.

Both the primary and pair-only models improve precision and F1 over expanded assignment in every fitted seed. The pair-only model reaches 75.33% F1. The primary-minus-pair-only F1 difference is -0.02 pp, with an interval of [-0.46, +0.43] pp. This is evidence for verification, not for the additional existence mechanism.

The untrained original-score filter selects accept-all and exactly reproduces expanded assignment. The learned improvement is therefore more informative than simply comparing a filtered model with an untreated baseline. However, this does not rule out every other hand-designed score rule.

Gains are not uniform: unchanged and moved strata lose some F1, while mixed cases improve. In all-replaced cases, false links decrease from 237.67 to 186.00 on average, but many incorrect associations remain. Recall is undefined in that stratum because there are no true links.

## B: a useful ordinary-training control

The ordinary control improves original-head F1 from 65.61% to 71.34% and recall from 62.03% to 71.56%. Precision rises from 69.66% to 71.14% as a point estimate.

| Ordinary-minus-original metric | Estimate | Descriptive 95% interval |
|---|---:|---:|
| Precision | +1.48 pp | [-1.56, +4.64] pp |
| Recall | +9.53 pp | [+6.46, +12.60] pp |
| F1 | +5.74 pp | [+3.09, +8.35] pp |

The absolute false-link count actually increases from 173 to 186, while true links increase from 397 to 458. Better precision here does not mean fewer false links; it means a higher correct fraction among more accepted links.

Relative to expanded assignment, the ordinary control gains 12.43 precision points, loses 16.41 recall points and gains 0.92 F1 points. The F1 interval [-2.48, +4.60] pp includes zero. The previous verifier keeps higher F1, 71.64%, at lower precision, 63.91%. Thus no single model dominates all controls on every metric.

All ordinary-control policy tiers were selected on fresh calibration data. The hard-training primary could not meet its calibration criteria and used original-model fallback in all three seeds. Highlighting the ordinary control is an exploratory interpretation of a predeclared arm, not a successful confirmation of the original hard-training hypothesis.

## Engineering outcomes supported by archived records

| Completed item | Evidence |
|---|---|
| Six verifier fits in v5 | All selected checkpoints differ from initialization; 12 stored weight hashes checked |
| V5 replay | 9 calibration rules, 6 checkpoint selections, 3,456 case/method predictions reproduced |
| Six new fits in v7 | Matched ordinary/hard conditions across three seeds; 12 stored weight hashes checked |
| V7 replay | 15 calibration policies, 6 checkpoint/mining checks, 4,608 predictions reproduced |
| V7 training reproduction | All six state dictionaries, complete histories and policies reproduced exactly in the recorded environment |
| Auditability | Protocols, full-precision summaries, reports and historical replay records included here |

These 3,456 and 4,608 figures count method/seed/case predictions, **not unique independent scenes**. Each experiment has 96 test layouts.

## Lessons that inform the next step

1. Candidate coverage matters: a verifier cannot recover a true link that never enters its accepted-assignment pool.
2. Precision must be evaluated with retained recall and F1; aggressive rejection can look clean while losing useful correspondences.
3. More complicated training is not automatically better. V7 hard training failed, and v8's twelve diagnostic fits did not establish a new test gain.
4. The next local-competition experiment has prepared source code but no submitted training job or measured result in this evidence package. It is not a current achievement.

The strongest defensible conclusion is: **learned verification improves the precision/F1 tradeoff of a high-recall internal association baseline in a controlled synthetic setting.** Evidence for superiority over published strong baselines or for real-world room-change performance remains outstanding.
