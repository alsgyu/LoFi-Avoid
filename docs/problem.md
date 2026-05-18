# Problem Definition

## Core Problem

We want reliable obstacle avoidance from depth on a humanoid robot with a low-resolution camera, under fast motion and vibration.

The practical failure modes are:

- texture-poor grass causes unstable stereo depth
- repeated green regions produce ambiguous disparity
- low resolution makes thin objects and noise look similar
- head motion and walking amplify frame-to-frame jitter
- false positives propagate into avoid and behavior decisions

## Existing Pipeline Assumption

The current robot stack already has a geometric obstacle pipeline:

1. depth image
2. preprocessing
3. 3D back-projection
4. robot-frame filtering
5. 2D grid binning with 3D points retained per cell
6. occupancy thresholding
7. PCA-based shape filtering
8. obstacle list

This repository assumes that geometry remains the first-stage candidate generator.

## Research Question

Which combination of:

- filtering
- heuristics
- temporal smoothing
- clustering
- lightweight machine learning

best reduces false positives while keeping latency low enough for real-time humanoid control?

## Success Criteria

- fewer false positives on empty field scenes
- lower obstacle jitter during head motion and walking
- more stable generic avoid signals
- better downstream decisions without introducing unsafe misses
