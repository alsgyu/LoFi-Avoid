# DepthAvoidML

Open-source experiments for depth-based obstacle avoidance on humanoids with low-resolution cameras.

This repository is meant to study a practical problem:

- depth is noisy on texture-poor soccer fields
- humanoids move quickly and shake the camera
- low-resolution sensors make obstacle boundaries unstable
- false positives propagate into avoid, dribble, clearing, and planner decisions

The goal is not only to train a model, but to build a full evaluation pipeline that makes it easy to compare:

1. current geometry-only baseline
2. heuristic tuning and filtering
3. lightweight ML refinement on top of geometric candidates

## Scope

This repository is intentionally broader than a single striker task.

We treat `striker decision` as one useful downstream adapter because it exposes clear signals such as `front_blocked` and `lane_open`, but the core problem here is generic obstacle avoidance. The shared target is:

- produce stable obstacle candidates from noisy depth
- reduce false positives and jitter
- improve generic avoid signals that any behavior can consume

## Repository Layout

```text
DepthAvoidML/
  adapters/                Bridge code and notes for external systems
  baselines/               Geometry-only and tuned-filter baselines
  configs/                 Stage and model configs
  docs/                    Problem, data, evaluation, integration docs
  evaluation/              Figure generation and benchmark scripts
  examples/                Sample run layout
  models/                  Lightweight ML candidates
  src/depth_avoid_ml/      Shared Python utilities
  tests/                   Future unit tests
```

## Recommended Workflow

1. Record or replay `rosbag2` from the robot stack.
2. Export run-level CSV logs from the instrumented robot code.
3. Copy those exported runs into this repository.
4. Generate baseline figures and summaries.
5. Apply heuristic tuning and compare the same bag again.
6. Add labels and train a lightweight classifier for false-positive rejection.
7. Compare `baseline -> tuned -> model` using the same benchmark protocol.

## Current Stage Design

### Stage 1: Baseline

- no algorithm changes
- only export and quantify current behavior
- establish figures for point counts, occupied cells, final obstacles, and downstream avoid signals

### Stage 2: Tuned Filters

- ROI cuts
- depth range tuning
- plane removal
- temporal consistency
- clustering and shape filters

### Stage 3: ML Refinement

- keep geometry as candidate generator
- train a small classifier to remove false positives
- preserve low latency and keep a safe fallback path

## Why Lightweight ML Instead of End-to-End?

For this problem, a small model is the right first step.

- it can run in real time on CPU
- it needs much less data than a full perception model
- it is easier to debug
- it fits naturally into the existing pipeline

The intended insertion point is:

`depth -> geometric candidates -> features -> ML classifier -> smoothed obstacle output`

## First Model Recommendation

Start with `XGBoost` or another tree-based tabular model on candidate-level features such as:

- point count
- mean range
- height spread
- cell occupancy
- PCA ratio
- temporal persistence
- overlap with semantic detections

## Quickstart

Create a Python environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Generate figures from exported runs:

```bash
python evaluation/plot_runs.py \
  --run baseline=/path/to/baseline_run \
  --run tuned=/path/to/tuned_run \
  --run model=/path/to/model_run \
  --out-dir outputs/figures
```

## Integration

The current robot-side CSV exporter lives in the INHA Soccer codebase and is documented in:

- [docs/integration_inha_brain.md](docs/integration_inha_brain.md)
- [adapters/inha_brain/README.md](adapters/inha_brain/README.md)

## Roadmap

- baseline benchmark and figures
- tuned filter benchmark
- candidate-level label format
- XGBoost baseline model
- generic avoid metrics
- optional semantic fusion and temporal models
