# Evaluation Protocol

## Principle

Every algorithmic change should be compared on the same input run.

The recommended experimental sequence is:

1. baseline
2. tuned filters
3. ML refinement

## Metric Layers

### 1. Perception-Level

- mean final obstacles per frame
- p95 final obstacles per frame
- occupied cell count
- PCA pass count
- obstacle jitter over time

### 2. Generic Avoid-Level

- corridor blocked ratio
- unnecessary stop ratio
- false avoid ratio
- persistence of avoid state

### 3. Task Adapter-Level

Current adapter:

- striker lane and kick-precondition signals

Future adapters:

- defender clearing corridor
- goalie clear-front condition
- generic walk corridor free/blocked

## Benchmark Scenes

Recommended scenes:

- empty field, static robot
- empty field, head yaw/pitch scan
- empty field, walking robot
- single person
- wall or board
- game-like congestion near ball

## Figure Set

Required minimum:

- depth pipeline count timeline
- final obstacle histogram
- downstream signal timeline
- stage comparison summary
