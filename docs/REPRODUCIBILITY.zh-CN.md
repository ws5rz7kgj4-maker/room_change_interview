# 复现与 GitHub 使用方式

[English](REPRODUCIBILITY.md) · [项目主页](../README.zh-CN.md)

## 本包包含什么

这个面试展示包包含文档、图表、原始汇总证据、实验协议与指标检查脚本。完整实验代码和权重明确列为独立归档，避免把这个轻量仓库误认为已经完整交付的原始视频检测器。

整理本包时没有新增训练或模型推理。下面区分本次进行的数值核验，以及原实验已经记录的模型重放。

## 检查包内证据

在仓库根目录使用 Python 3.11 或更高版本：

    python scripts/verify_metrics.py

只依赖 Python 标准库。它核验全部 42 组方法／种子计数、对应 P/R/F1 均值、核心差值、文件哈希，以及历史重放元数据的一致性；不会独立重算 bootstrap 或模型预测。

重新生成派生表格与图：

    python -m pip install -r requirements-figures.txt
    python scripts/build_assets.py
    python scripts/verify_metrics.py

重建中文图需要 CJK 字体，例如 Noto Sans CJK。查看包内现成 PNG／SVG 不需要安装字体；SVG 使用字形路径。

## 完整实验归档

原始归档位于作者的 **Hugging Face 私有数据仓库**。以下链接需要具有访问权限的账号；本包已复制的统计摘要不受这个限制。私有访问是分发限制，不代表没有完成评估。

| 实验 | 归档 | SHA-256 |
|---|---|---|
| V5 | [expanded_match_precision.zip](https://huggingface.co/datasets/swenlio/room-change-crossroom-smoke-20261025-a72b4c6e/resolve/main/experiments/scenediff_reproduction/expanded_match_precision_20261105_v5/delivery/expanded_match_precision.zip?download=true) | 949c8aec5c82e204f82361c4b06a8bb228a70c85c9c5a75a5792905c3688b437 |
| V7 | [hard_identity_training.zip](https://huggingface.co/datasets/swenlio/room-change-crossroom-smoke-20261025-a72b4c6e/resolve/main/experiments/scenediff_reproduction/hard_identity_training_20261106_v7/delivery/hard_identity_training.zip?download=true) | 29cf3900f58b168b90925b261d5fd59722c66774234253f750fa36997dd6be0a |

归档包括代码、冻结匹配头、训练／验证／校准／测试特征、完整预测、示例输入输出、实验协议和重放工具。大型预训练骨干权重和另行归档的原始渲染集合不包含在这两个小型归档中。

取得文件后，先检查哈希：

    python -c "import hashlib,pathlib; p=pathlib.Path('hard_identity_training.zip'); print(hashlib.sha256(p.read_bytes()).hexdigest())"

### V7：运行本材料重点讨论的普通训练对照

将归档解压到新目录，在归档根目录打开终端：

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r code/requirements.txt
    python code/infer.py --root . --features examples/example.npz --seed 42 --method new_plain --output outputs/plain_prediction.json
    python code/verify_results.py --root . --output outputs/verification.json
    python code/retrain.py --root . --output outputs/retrained

显式指定的方法是这里展示的普通训练对照。历史归档默认主方法是困难训练，其回退结果不能表述为学习成功。

### V5：运行预先指定的主方法

在解压后的 v5 根目录，先按照其 code/README.md 安装依赖，再运行：

    python code/infer.py --root . --features examples/example.npz --seed 42 --method matchability_verifier --output reproduced/prediction.json
    python code/verify_results.py --root . --output reproduced/verification.json
    python code/retrain.py --root . --output reproduced/retrained

更简单的学习式对照使用 pair_verifier 方法。这些命令处理归档内的缓存证据，并非直接接受任意两段视频；也支持种子 43 和 44。重新训练的完全数值一致性依赖记录中的运行环境。

## 放到 GitHub

建议仓库名：**room-change-association-study**。

建议中文简介：**面向房间变化研究的学习式物体对应验证，包含仿真 benchmark 证据与可复现实验评估。**

建议标签：computer-vision、object-association、scene-change-detection、synthetic-data、pytorch、robotics、reproducible-research。

解压展示包，在 room-change-interview 目录打开终端，先阅读 README.md 或 README.zh-CN.md。新建本地仓库时运行：

    git init -b main
    git add README.md README.zh-CN.md docs results evidence assets scripts .github .gitignore requirements-figures.txt
    git commit -m "Document verified room-change association results"

之后连接你选择的 GitHub 仓库。本次整理没有创建 GitHub 仓库，也没有发布任何内容。若放入已有代码仓库，复制前先检查同名文件。

本包没有为第三方代码或权重授予新许可，也不重新分发预训练骨干权重。
