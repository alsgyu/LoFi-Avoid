# LoFi-Avoid

Low-fidelity depth obstacle avoidance for humanoids.

LoFi-Avoid studies a simple but painful problem: low-resolution depth can look usable frame-by-frame, yet still produce unstable obstacle signals once the robot starts moving its head, walking, or operating in texture-poor scenes like grass fields.

This repository is for building and evaluating a practical pipeline that:

- measures those failures clearly
- compares geometry-only baselines against tuned filters
- adds lightweight ML only where it actually helps

The project starts from a practical conclusion: preprocessing and filtering are necessary, but they were not enough. Even after pushing the geometric pipeline with hand-tuned thresholds and cleanup, some scenes still produced false positives that were too costly to ignore. LoFi-Avoid exists to make that claim measurable and to justify where ML becomes necessary.

## Demo

<p align="center">
  <img src="second.gif" alt="LoFi-Avoid RGB and depth view" width="40%">
</p>

<p align="center">
  <sub>Failure case: depth flicker creates a false obstacle, and background structure is incorrectly treated as a valid obstacle cue (red points).</sub>
</p>

<p align="center">
  <img src="first.gif" alt="LoFi-Avoid false positive failure case" width="66%">
</p>

<p align="center">
  <sub>Paired RGB camera image and depth image from the same scene. Depth points are projected onto a 2D floor grid, accumulated by cell count, and then promoted to obstacle candidates when a local region becomes dense enough.</sub>
</p>

## Overview

LoFi-Avoid is not an end-to-end detector repository. It is a benchmark and experiment loop for improving obstacle avoidance under noisy depth.

The current design assumes this structure:

`depth -> geometric candidates -> candidate features -> lightweight classifier -> stable avoid signals`

That choice is deliberate:

- geometric candidates are easy to debug
- false positives can be measured directly
- lightweight models are cheap enough for real-time use
- the same benchmark can compare baseline, tuned, and model-based stages

The intended use of ML is narrow and deliberate: not to replace geometric preprocessing, but to clean up the hard failure cases that survive even after the best reasonable filtering and projection logic have been applied.

## Problem

Low-fidelity depth tends to fail in ways that matter to control:

- obstacle-free scenes can still produce unstable candidates
- head motion can amplify point-cloud jitter
- low resolution can make thin noise look like a real object
- background walls or structures can be promoted into false obstacles
- downstream avoid logic can overreact even when the scene is safe

The point of this repository is to make those effects reproducible and measurable.

## What This Repo Contains

- benchmark scripts for exported run data
- figure generation for baseline vs tuned vs model comparisons
- documentation for data format and evaluation
- starter ML baselines for candidate-level classification
- integration notes for the INHA Soccer robot stack

## Quick Start

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

## Evaluation Philosophy

Every method should be compared on the same recorded input.

The intended experiment order is:

1. geometry-only baseline
2. tuned filtering and heuristics
3. lightweight ML refinement

The main metrics are:

- sampled valid depth points
- candidate points
- occupied cells
- PCA-pass cells
- final obstacles
- downstream avoid-state stability

## Why Lightweight ML

The first model should be small, inspectable, and cheap.

LoFi-Avoid assumes the following order of operations:

1. build the strongest geometric baseline possible
2. quantify its remaining failure cases
3. add ML only for those remaining errors

A candidate-level tabular model such as `XGBoost` is a strong starting point because it can use features like:

- point count
- mean position and range
- vertical spread
- occupancy density
- PCA ratio
- temporal persistence

without replacing the whole perception stack.

## Repository Layout

```text
LoFi-Avoid/
  adapters/       Integration notes and bridges
  baselines/      Geometry and tuned-filter baselines
  configs/        Stage and model configs
  docs/           Problem, dataset, evaluation, integration
  evaluation/     Figure generation and benchmark scripts
  models/         Lightweight ML baselines
  src/            Shared Python utilities
```

## Integration

The current robot-side CSV exporter lives in the INHA Soccer stack.

See:

- [docs/integration_inha_brain.md](docs/integration_inha_brain.md)
- [adapters/inha_brain/README.md](adapters/inha_brain/README.md)

## Documentation

- [Problem definition](docs/problem.md)
- [Dataset and run format](docs/dataset.md)
- [Evaluation protocol](docs/evaluation.md)
- [INHA brain integration](docs/integration_inha_brain.md)
