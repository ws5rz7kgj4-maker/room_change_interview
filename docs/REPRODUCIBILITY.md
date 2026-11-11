# Reproducibility and GitHub setup

[中文](REPRODUCIBILITY.zh-CN.md) · [Project overview](../README.md)

## What this release includes

This interview release contains documentation, figures, archived aggregate evidence, protocols and metric checks. It deliberately identifies the broader experiment code/weights as separate artifacts; a reader should not mistake this small repository for the complete raw-video detector.

No new training or model inference was performed while creating this release. The checks below distinguish arithmetic verification now from model replay recorded in the completed experiments.

## Check the included evidence

From the repository root, with Python 3.11 or later:

    python scripts/verify_metrics.py

This requires only Python's standard library. It verifies all 42 method/seed count records, their P/R/F1 means, reported contrasts, evidence hashes and the consistency of historical replay metadata. It does not independently reproduce the bootstrap or model outputs.

To rebuild the derived tables and figures:

    python -m pip install -r requirements-figures.txt
    python scripts/build_assets.py
    python scripts/verify_metrics.py

Chinese figure regeneration requires a CJK font, such as Noto Sans CJK. The checked-in PNG/SVG figures can be viewed without installing fonts. Generated SVGs use glyph paths.

## Full experiment archives

The original artifacts are in the author's **private** Hugging Face dataset repository. These links require an account with access; the summaries copied into this repository do not. Private access is a distribution limit, not a missing evaluation result.

| Experiment | Archive | SHA-256 |
|---|---|---|
| V5 | [expanded_match_precision.zip](https://huggingface.co/datasets/swenlio/room-change-crossroom-smoke-20261025-a72b4c6e/resolve/main/experiments/scenediff_reproduction/expanded_match_precision_20261105_v5/delivery/expanded_match_precision.zip?download=true) | 949c8aec5c82e204f82361c4b06a8bb228a70c85c9c5a75a5792905c3688b437 |
| V7 | [hard_identity_training.zip](https://huggingface.co/datasets/swenlio/room-change-crossroom-smoke-20261025-a72b4c6e/resolve/main/experiments/scenediff_reproduction/hard_identity_training_20261106_v7/delivery/hard_identity_training.zip?download=true) | 29cf3900f58b168b90925b261d5fd59722c66774234253f750fa36997dd6be0a |

The archives contain code, frozen heads, train/validation/calibration/test evidence, full predictions, example inputs/outputs, protocols and replay utilities. Large pretrained backbone weights and separately archived raw rendering sets are not bundled in these small archives.

After obtaining an archive, verify its hash before extracting it:

    python -c "import hashlib,pathlib; p=pathlib.Path('hard_identity_training.zip'); print(hashlib.sha256(p.read_bytes()).hexdigest())"

### V7: replay the highlighted ordinary control

Extract the archive into a fresh directory and open a terminal at that archive root:

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r code/requirements.txt
    python code/infer.py --root . --features examples/example.npz --seed 42 --method new_plain --output outputs/plain_prediction.json
    python code/verify_results.py --root . --output outputs/verification.json
    python code/retrain.py --root . --output outputs/retrained

The explicit method selects the ordinary control discussed in this portfolio. The historical archive's default primary is hard training; its fallback must not be described as a learned improvement.

### V5: replay the prespecified primary

In the extracted v5 archive root, install the environment listed in its code/README.md, then:

    python code/infer.py --root . --features examples/example.npz --seed 42 --method matchability_verifier --output reproduced/prediction.json
    python code/verify_results.py --root . --output reproduced/verification.json
    python code/retrain.py --root . --output reproduced/retrained

Use the pair_verifier method for the simpler learned control. These commands operate on included cached evidence; they do not take two arbitrary videos as input. Seeds 43 and 44 are also supported. Exact retraining equality is tied to the recorded environment.

## Put this material on GitHub

Suggested repository name: **room-change-association-study**.

Suggested English description: **Learned verification of object correspondences for room-change research, with synthetic benchmark evidence and reproducible evaluation.**

Suggested topics: computer-vision, object-association, scene-change-detection, synthetic-data, pytorch, robotics, reproducible-research.

Extract the supplied portfolio ZIP, open a terminal in its room-change-interview directory, and inspect README.md or README.zh-CN.md. For a new local repository:

    git init -b main
    git add README.md README.zh-CN.md docs results evidence assets scripts .github .gitignore requirements-figures.txt
    git commit -m "Document verified room-change association results"

Then connect this directory to the GitHub repository of your choice. No GitHub repository was created and nothing was published by preparing this package. If using an existing code repository, review path collisions before copying these files.

This release does not grant a new license to third-party code or weights and does not redistribute pretrained backbone weights.
