# Method and experiment design

[中文](METHOD.zh-CN.md) · [Project overview](../README.md)

## The problem addressed here

Before deciding whether a chair moved, a system must determine whether observations in two recordings belong to the same physical instance. Similar-looking replacements, viewpoint differences and missing observations make this harder than recognizing an object category.

This study evaluates that identity-association step in static synthetic scenes. RGB appearance features are extracted using simulator-supplied support masks and within-recording grouping. The learned verifier never receives ground-truth identity, semantic category, motion, depth or camera-pose labels as inference features, but the upstream candidate construction is privileged. Therefore the benchmark cannot be described as RGB-only end-to-end inference.

## Candidate coverage and verification

Let the observed objects be $A=\{a_i\}_{i=1}^{n}$ and $B=\{b_j\}_{j=1}^{m}$.

**1. Frozen identity scores.** A learned 29-input MLP scores each candidate pair, with an unmatched logit $u$. The original full-head decision accepts reciprocal best matches above its unmatched alternative. The visual backbone and original head are frozen in the highlighted verifier experiments.

**2. Expanded optional global assignment.** With $s_{ij}$ denoting the original pair logit minus $u$, solve

$$
\max_{z}\sum_{i,j}(s_{ij}-\tau)z_{ij},
\quad z_{ij}\in\{0,1\},\quad
\sum_jz_{ij}\leq 1,\quad\sum_iz_{ij}\leq 1.
$$

Dummy unmatched assignments have zero utility. The implementation withholds links that are not required across numerically optimal solutions, preventing candidate order from resolving genuine ambiguity. The cutoff is calibrated before test scoring. Unlike retaining a fixed top fraction, this allows the amount of accepted evidence to vary.

**3. Learn to verify accepted links.** For every candidate pair, form a 65-dimensional feature vector:

| Group | Dimensions | Information |
|---|---:|---|
| Original evidence | 29 | Frozen visual descriptors, colour and observed-support summaries |
| Score context | 8 | Symmetric context derived from the original scores |
| Local correspondence | 28 | SIFT matching, homography/fundamental-matrix support and spatial coverage summaries |

A 65→32→16 encoder with ReLU activations and a linear output predicts pair correctness:

$$p_{ij}=\sigma(f_\theta(x_{ij})).$$

Ordinary training uses assigned-pair binary cross entropy, averaged within a case and weighted across layouts. The verifier can only remove links from the frozen expanded assignment; it cannot reassign partners or recover a link outside that assignment.

**4. Existence control in v5.** A pooled branch predicts whether each observed endpoint has a counterpart in the other observed set. The prespecified primary score is

$$q_{ij}=p_{ij}\sqrt{e_i e'_j}.$$

The pair-only control uses $q_{ij}=p_{ij}$. V5 provides no demonstrated extra F1 benefit from the pooled existence branch. V7 ordinary training disables that branch.

**5. Freeze an operating point.** Retain an expanded link if $q_{ij}\geq t$. Choose $t$ on a separate calibration split, not on test outcomes. V5 maximizes calibration F1 subject to baseline precision/F1, at least 90% of baseline recall and at least 30 accepts, with accept-all fallback. V7 uses an original-model precision target and explicitly reported reference fallback. These empirical constraints are not held-out guarantees.

## Handling incomplete evidence

Two label-independent candidate-drop variants accompany each original training case. Scores and contextual features are recomputed after subsetting; supervision is remapped separately. This trains on missing observed counterparts without treating every missing observation as physical removal.

The local correspondence features are sparse **2D geometric evidence**. They do not establish a common 3D map, free-space occupancy or metric object displacement.

## Experimental separation

| Split | V5 layouts / cases | V7 layouts / cases | Purpose |
|---|---:|---:|---|
| Train | 48 / 96 | 96 / 192 | Fit small verifier weights |
| Validation | 12 / 24 | 24 / 48 | Select checkpoints |
| Calibration | 24 / 48 | 48 / 96 | Freeze acceptance policies |
| Confirmation test | 96 / 192 | 96 / 192 | Evaluate every fixed method |

Training augmentation yields 288 cases in v5 and 576 in v7. Each base layout has two material variants; those are dependent observations. Both tests contain 640 true links per seed. The tests use disjoint layout-seed ranges: v5 2026119500–2026119595; v7 2026122000–2026122095.

There are 3/5/7-object settings, four change modes, and five shared procedural object families. Test layouts are new, while asset families are shared with training. V7 reuses earlier training/validation data and adds new cases; it does not train on earlier test or calibration tables.

For each fitted seed,

$$P=\frac{TP}{TP+FP},\qquad R=\frac{TP}{TP+FN},\qquad F1=\frac{2TP}{2TP+FP+FN}.$$

Counts are pooled across cases **within a seed**, then each metric is averaged across seeds 42/43/44. The reported mean F1 is not reconstructed from mean P and mean R. Three seeds sharing the same test scenes are not three independent scene replications.

Uncertainty uses 4,000 paired bootstrap draws of the 96 base layouts, retaining both materials and every method/seed per layout. The 95% percentile intervals are descriptive, conditional on fitted models and frozen policies, without multiplicity adjustment.

## What this contributes

The practical contribution is a tested way to improve precision after expanding candidate coverage, together with accounting for false links removed and correct links lost. Assignment optimization, SIFT, DINOv3 and BCE classifiers are existing methods. The evidence does not isolate a novel geometric mechanism or establish a new SOTA algorithm.

For the complete room-change task, identity evidence would have to be integrated with shared 3D alignment, visibility/free-space reasoning, and semantic descriptions. That integration is outside the measured gains reported here.
