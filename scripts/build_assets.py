"""Build exact JSON, bilingual scorecards and figures from archived results."""
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from verify_metrics import ROOT, collect

LABELS = {
    "reference_full": ("Original full identity head", "原完整身份匹配头"),
    "expanded_baseline": ("Frozen expanded assignment", "冻结的扩展全局匹配"),
    "previous_residual": ("Previous geometry residual", "前一版几何残差模型"),
    "score_filter": ("Original-score filter", "原始分数筛选"),
    "pair_verifier": ("Learned pair verifier", "学习式匹配对验证器"),
    "matchability_verifier": ("Pair + existence verifier (primary)", "匹配对＋存在性验证器（主方法）"),
    "previous_pair": ("Previous verifier, old cutoff", "前一版验证器＋旧阈值"),
    "recalibrated_pair": ("Previous verifier, fresh policy", "前一版验证器＋新校准策略"),
    "new_plain": ("Ordinary training, precision policy (control)", "普通训练＋精确率策略（对照）"),
    "new_hard": ("Hard training, precision policy (primary)", "困难样本训练＋精确率策略（主方法）"),
    "new_plain_balanced": ("Ordinary training, balanced policy", "普通训练＋均衡策略"),
    "new_hard_balanced": ("Hard training, balanced policy", "困难样本训练＋均衡策略")}


def scorecard(data, zh=False):
    lang = int(zh)
    lines = ["# " + ("完整同测试集结果" if zh else "Complete same-test results"), "",
             ("单位：百分比；每种方法先按种子进行微平均，再取三个种子的均值。A、B 是不同测试集，不可直接跨组作性能比较。"
              if zh else "Values are percentages: micro-aggregate within each seed, then average three seeds. A and B use different test sets; do not compare their absolute scores as a longitudinal gain."), ""]
    for key, title in (("experiment_A_v5", "A — v5"), ("experiment_B_v7", "B — v7")):
        lines += ["## " + title, "",
                  ("96 个布局，192 个配对材质案例；每个种子 640 条真实对应。" if zh else
                   "96 layouts, 192 material-paired cases; 640 true links per seed."), "",
                  "| " + ("方法 | 精确率 | 召回率 | F1 | 平均 TP | 平均 FP | 平均 FN |" if zh else
                           "Method | Precision | Recall | F1 | Mean TP | Mean FP | Mean FN |"),
                  "|---|---:|---:|---:|---:|---:|---:|"]
        for method, row in data[key]["methods"].items():
            vals = [f"{100*row[k]['mean']:.2f}" for k in ("precision", "recall", "f1")]
            vals += [f"{row[k]['mean']:.2f}" for k in ("tp", "fp", "fn")]
            lines.append("| " + LABELS[method][lang] + " | " + " | ".join(vals) + " |")
        lines += [""]
    return "\n".join(lines) + "\n"


def plot(data, zh=False):
    family = "DejaVu Sans"
    if zh:
        available = {f.name for f in font_manager.fontManager.ttflist}
        choices = ("Noto Sans CJK SC", "Noto Sans CJK JP", "Microsoft YaHei", "PingFang SC", "Arial Unicode MS")
        family = next((name for name in choices if name in available), None)
        if family is None:
            raise RuntimeError("Install a CJK font (for example Noto Sans CJK) to rebuild the Chinese figure.")
    plt.rcParams.update({"font.family": family,
                         "font.size": 11, "svg.fonttype": "path", "axes.unicode_minus": False})
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.5))
    title = "仿真实例匹配：两组独立实验中的提升" if zh else "Synthetic instance association: gains in two separate experiments"
    fig.suptitle(title, fontsize=18, weight="bold", y=.97)
    settings = [
        ("experiment_A_v5", "expanded_baseline", "matchability_verifier",
         "A · 学习式验证" if zh else "A · Learned verification",
         ["扩展全局匹配", "匹配对＋存在性验证"] if zh else ["Expanded assignment", "Pair + existence verifier"]),
        ("experiment_B_v7", "reference_full", "new_plain",
         "B · 普通训练对照" if zh else "B · Ordinary-training control",
         ["原完整匹配头", "普通训练＋精确率策略"] if zh else ["Original full identity head", "Ordinary training + precision policy"])]
    for ax, (key, baseline, candidate, subtitle, names) in zip(axes, settings):
        x = np.arange(3)
        for offset, method, color, label in ((-.19, baseline, "#A4ADBA", names[0]), (.19, candidate, "#197A7E", names[1])):
            values = [100*data[key]["methods"][method][metric]["mean"] for metric in ("precision", "recall", "f1")]
            bars = ax.bar(x+offset, values, width=.36, color=color, label=label, zorder=3)
            ax.bar_label(bars, labels=[f"{v:.2f}" for v in values], padding=4, fontsize=10)
        ax.set_title(subtitle, loc="left", fontsize=14, pad=15, weight="bold")
        ax.set_ylim(0, 105); ax.set_yticks(range(0, 101, 20))
        ax.set_xticks(x, ["精确率", "召回率", "F1"] if zh else ["Precision", "Recall", "F1"])
        ax.set_ylabel("百分比（%）" if zh else "Percent (%)")
        ax.grid(axis="y", color="#E4E8EC", zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(loc="upper center", bbox_to_anchor=(.5, -.12), frameon=False, fontsize=10)
    note = ("每组：96 个新布局 · 192 个案例 · 3 个拟合种子。组间测试集不同。B 的精确率提升区间包含零。"
            if zh else "Each: 96 fresh layouts · 192 cases · 3 fitted seeds. Different test sets. B's precision-gain interval includes zero.")
    fig.text(.5, .04, note, ha="center", fontsize=10, color="#454F5C")
    fig.subplots_adjust(top=.79, bottom=.25, left=.06, right=.985, wspace=.22)
    for ext in ("png", "svg"):
        fig.savefig(ROOT / "assets" / f"results_{'zh' if zh else 'en'}.{ext}", dpi=180, facecolor="white")
    plt.close(fig)


def main():
    data = collect()
    (ROOT/"results/verified_results.json").write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    for zh, suffix in ((False, ""), (True, ".zh-CN")):
        (ROOT/f"results/ALL_RESULTS{suffix}.md").write_text(scorecard(data, zh), encoding="utf-8")
        plot(data, zh)
    files = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted((ROOT/"evidence").iterdir()) if p.is_file() and p.name != "sha256_manifest.json"}
    (ROOT/"evidence/sha256_manifest.json").write_text(json.dumps(
        {"purpose": "Byte integrity of copied evidence; not independent experimental replication.", "files": files}, indent=2)+"\n")
    print("Built bilingual figures, complete result tables, verified-results JSON and evidence hashes.")


if __name__ == "__main__":
    main()
