# Interview talking points

[中文](INTERVIEW.zh-CN.md) · [Project overview](../README.md)

## 30-second introduction

> I worked on object-instance association for room-change understanding. A central tradeoff was that expanding candidate matches recovered many true correspondences but also introduced false matches. I built a learned verification stage on top of frozen global assignment and evaluated it on held-out synthetic scenes. In the main positive experiment, precision rose from 61.51% to 65.60% and F1 from 73.72% to 75.32%, while preserving 96.21% of correct baseline links. I also built frozen-split evaluation, error accounting and replay checks. The current evidence is for the association module; real-video and full 3D change detection remain separate validation steps.

## Two-minute technical explanation

> The long-term input is two RGB recordings of a static room before and after changes. I focused this study on the identity question: do these observations show the same physical object?
>
> An early conservative approach discarded too many useful matches. I separated candidate coverage from verification. The first stage uses all-pair scores and optional one-to-one global assignment. The second stage learns pair correctness from appearance, score context and sparse local correspondences. Its threshold is selected on calibration data, and it cannot invent or reassign links.
>
> The main positive test contained 96 new layouts, two material variants per layout and three fitted seeds. Compared with expanded assignment, the verifier removed 19.19% of false links while retaining 96.21% of true links. Precision and F1 gains had positive paired-layout descriptive intervals. Recall fell by 3.49 points, which I report explicitly.
>
> I also tested additional existence learning and hard-example ranking. The existence branch did not clearly beat the simpler pair verifier, and the hard-training primary failed. A predeclared ordinary-training control later improved F1 by 5.74 points over the original full identity head on a separate test. My main conclusion is that high-recall candidate generation plus selective learned verification was useful here; extra complexity required evidence of its own.
>
> These results use supplied synthetic masks and grouping. They do not yet establish raw-phone-video robustness or superiority over a published full-system baseline.

## CV-ready bullets

- Developed and evaluated a learned object-correspondence verifier for room-change research; improved precision by **4.08 pp** and F1 by **1.60 pp** over a frozen expanded-assignment baseline on **96 held-out synthetic layouts**, with a **3.49 pp recall tradeoff**.
- Reduced false identity links by **19.19%** while retaining **96.21%** of baseline correct links; used three fitted seeds, separate calibration and paired-layout uncertainty estimates.
- Built reproducible experiment artifacts with frozen splits/checkpoints, per-case predictions and verification records covering **3,456** and **4,608** method/seed/case outputs in two experiments.

Use the first two bullets together or retain the scope in the first one. The prediction totals are not counts of independent test scenes.

## Questions to be ready for

**Which strong baseline did you beat?**  
An internal expanded-global-assignment baseline that already exceeded our original identity head's F1 on the same test. I have not established superiority over the published SceneDiff system or another external SOTA model.

**What is actually trained?**  
A small pair-verification network. DINOv3 and the original association scores remain frozen. This experiment does not train the reconstruction algorithm.

**Is the model using only RGB?**  
The intended complete system takes RGB recordings. This module's reported tests also rely on supplied simulator masks and within-recording grouping. The verifier's features exclude ground-truth identity, depth and pose, but that alone does not make the whole pipeline RGB-only.

**Why is this more than raising a score threshold?**  
The untrained original-score-filter control chose accept-all and reproduced expanded assignment. Learned verification improved the precision/F1 tradeoff under the same calibration objective. This is evidence for the learned features, not proof that every possible score heuristic would fail.

**Where does the improvement come from?**  
Selective removal of false links while retaining most correct links. The simpler pair-only verifier is nearly as effective as the existence-augmented model. Current evidence does not isolate an extra gain from that branch or a unique geometric mechanism.

**Does the newer ordinary model beat everything?**  
No. It improves recall and F1 over the original full head, with a higher precision point estimate. Its precision interval crosses zero; its F1 is slightly below the older verifier on that same test. It is a useful operating tradeoff, not uniform dominance.

**How did you prevent leakage?**  
Weight fitting, checkpoint selection and policy calibration use separate declared data roles. Weights and policies were frozen before final scoring. Test scenes informed later hypotheses only after they became development evidence; follow-up confirmation used new layouts.

**Are three seeds enough to claim generalization?**  
They check fitting variability, not three independent scene replications. Both material variants of a layout are dependent, so uncertainty is resampled at layout level. Asset families remain shared across splits.

**What is the research novelty?**  
The currently supported contribution is a reproducible engineering result and a controlled study of matching tradeoffs. Assignment, BCE, DINOv3 and SIFT are established tools. I would need closer prior-work comparison and stronger external evaluation before claiming algorithmic novelty.

**What would you do next?**  
Test whether training on actual within-scene competitors improves verification, then confirm on untouched layouts. Separately replace privileged masks/grouping with RGB-derived candidates, evaluate held-out phone videos and integrate identity with shared 3D geometry and visibility evidence.

**How were AI tools used?**  
Use the project workflow accurately: AI-assisted coding, experiment orchestration, analysis and documentation were part of the development process. Be ready to explain the code, experimental controls and limitations yourself; do not imply that every implementation line was written unaided.
