# INHA Brain Adapter

This folder documents the bridge between the public experiment repository and the INHA Soccer robot codebase.

## What Lives In The Robot Repo

- ROS publishers and subscribers
- depth callback implementation
- real-time obstacle construction
- run export hooks that emit CSV files

## What Lives In This Repo

- benchmark scripts
- figure generation
- data format docs
- training code
- model artifacts

## Current Contract

For each run, the robot repo exports:

- `manifest.txt`
- `depth_metrics.csv`
- `striker_metrics.csv`

Later, candidate-level CSV exports can be added without changing the public repository structure.
