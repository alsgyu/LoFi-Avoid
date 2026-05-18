# Integration With INHA Soccer Brain

## Purpose

The public repository stores experiments, figures, and models.

The robot stack remains the place where:

- depth is consumed online
- ros topics are replayed
- CSV run logs are exported

## Current Export Hook

The instrumented `brain_node` supports:

- `depth_avoid_eval.enable`
- `depth_avoid_eval.log_dir`
- `depth_avoid_eval.run_name`

When enabled, it creates:

- `manifest.txt`
- `depth_metrics.csv`
- `striker_metrics.csv`

## Example

```bash
ros2 run brain brain_node \
  --ros-args \
  -p depth_avoid_eval.enable:=true \
  -p depth_avoid_eval.log_dir:=/tmp/depth_avoid_eval \
  -p depth_avoid_eval.run_name:=baseline_empty_field
```

## Suggested Workflow

1. Replay a fixed rosbag with baseline code.
2. Save the run directory.
3. Replay the same rosbag with tuned filters.
4. Save the run directory.
5. Replay the same rosbag with model-enabled logic.
6. Copy all run directories into this repository or point the evaluation scripts at them directly.
