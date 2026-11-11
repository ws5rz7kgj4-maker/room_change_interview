"""Recompute portfolio claims from archived counts; standard library only.

This checks reported arithmetic and source integrity. It does not rerun a model,
regenerate bootstrap samples, or independently certify the original experiment.
"""
import hashlib
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def check_methods(methods):
    checked = 0
    for name, row in methods.items():
        assert len(row["tp"]["values"]) == 3, name
        for i, (tp, fp, fn) in enumerate(zip(
                row["tp"]["values"], row["fp"]["values"], row["fn"]["values"])):
            assert all(isinstance(x, int) and x >= 0 for x in (tp, fp, fn))
            assert tp + fn == 640, (name, i)
            expected = dict(precision=tp / (tp + fp), recall=tp / (tp + fn),
                            f1=2 * tp / (2 * tp + fp + fn))
            for key, value in expected.items():
                assert math.isclose(value, row[key]["values"][i], abs_tol=1e-12), (name, i, key)
            checked += 1
        for key in ("precision", "recall", "f1", "tp", "fp", "fn"):
            assert math.isclose(mean(row[key]["values"]), row[key]["mean"], abs_tol=1e-12)
    return checked


def collect():
    a = read("evidence/v5_summary.json")
    b = read("evidence/v7_key_results.json")
    check_methods(a["methods"])
    check_methods(b["methods"])
    intervals_a = read("evidence/v5_paired_layout_bootstrap.json")

    def contrast(methods, candidate, baseline, intervals, key):
        return {
            "candidate": candidate, "baseline": baseline,
            "delta_percentage_points": {
                k: 100 * (methods[candidate][k]["mean"] - methods[baseline][k]["mean"])
                for k in ("precision", "recall", "f1")},
            "descriptive_95_interval_percentage_points": {
                k: [100 * x for x in v] for k, v in intervals["comparisons"][key].items()}}

    ca = contrast(a["methods"], "matchability_verifier", "expanded_baseline",
                  intervals_a, "matchability_verifier_minus_expanded_baseline")
    cb = contrast(b["methods"], "new_plain", "reference_full",
                  b["intervals"], "new_plain_minus_reference_full")
    expanded, selected = a["methods"]["expanded_baseline"], a["methods"]["matchability_verifier"]
    ca["false_link_reduction_percent"] = 100 * (1 - selected["fp"]["mean"] / expanded["fp"]["mean"])
    ca["true_link_retention_percent"] = 100 * selected["tp"]["mean"] / expanded["tp"]["mean"]
    assert a["primary_method"] == "matchability_verifier"
    assert read("evidence/v7_protocol.json")["primary_method"] == "new_hard"
    assert all(t == "reference_fallback" for t in b["primary_calibration_tiers"].values())
    assert b["methods"]["new_hard"] == b["methods"]["reference_full"]
    for i in range(3):
        for metric in ("precision", "f1"):
            assert selected[metric]["values"][i] > expanded[metric]["values"][i]
    assert ca["descriptive_95_interval_percentage_points"]["precision"][0] > 0
    assert ca["descriptive_95_interval_percentage_points"]["f1"][0] > 0
    assert cb["descriptive_95_interval_percentage_points"]["precision"][0] < 0
    assert cb["descriptive_95_interval_percentage_points"]["f1"][0] > 0
    return {
        "as_of": "2026-11-11",
        "metric": "observed-instance identity-link P/R/F1",
        "aggregation": "micro within each fitted seed, then arithmetic mean across seeds 42/43/44",
        "scope": "Synthetic masks/grouping are supplied; not end-to-end RGB video evaluation.",
        "experiment_A_v5": {
            "layouts": 96, "material_paired_cases": 192, "true_links_per_seed": 640,
            "primary_method": "matchability_verifier", "methods": a["methods"], "highlight": ca},
        "experiment_B_v7": {
            "layouts": 96, "material_paired_cases": 192, "true_links_per_seed": 640,
            "primary_method": "new_hard", "highlighted_control": "new_plain",
            "methods": b["methods"], "highlight": cb},
        "published_baseline_superiority_established": False,
        "real_phone_video_accuracy_established": False}


def main():
    claims = collect()
    assert claims == read("results/verified_results.json"), "Regenerate the portfolio results."
    manifest = read("evidence/sha256_manifest.json")
    for name, digest in manifest["files"].items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        assert actual == digest, "Source hash mismatch: " + name
    for version, predictions in (("v5", 3456), ("v7", 4608)):
        checks = read(f"evidence/{version}_verification.json")
        assert checks["test_case_method_predictions_replayed"] == predictions
        assert checks["all_scores_links_counts_and_summaries_identical"]
        assert not checks["test_used_for_training_or_selection"]
    print("PASS: 42 method/seed count-to-metric records, both headline contrasts,")
    print("      archived source hashes, and historical replay metadata are consistent.")
    print("This run checks the evidence package; it does not rerun model inference.")
    for key in ("experiment_A_v5", "experiment_B_v7"):
        h = claims[key]["highlight"]
        print(key, json.dumps(h, ensure_ascii=False))


if __name__ == "__main__":
    main()
