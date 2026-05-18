# Dataset and Run Format

## Philosophy

This project starts from run-level exports rather than a custom binary format.

That keeps experiments reproducible and easy to move between:

- robot code repositories
- rosbag replays
- public benchmark repositories

## Expected Run Directory

Each run directory should look like this:

```text
run_name/
  manifest.txt
  depth_metrics.csv
  striker_metrics.csv
```

These files come from the robot-side instrumentation layer.

## Current Exported CSVs

### depth_metrics.csv

Frame-level geometry pipeline summary:

- `sampled_valid_points`
- `candidate_points`
- `nonempty_cells`
- `occupied_cells`
- `pca_pass_cells`
- `final_obstacles`

### striker_metrics.csv

Current downstream adapter for soccer-specific analysis:

- `front_blocked`
- `nearest_front_obstacle_x`
- `front_obstacle_max_x`
- `left_lane_open_width`
- `right_lane_open_width`
- `dribble_ready`
- `auto_visual_kick_ready`
- `quick_shoot_after_dribble`
- `decision`

## Future Labels

This repository is designed to grow into two label granularities.

### Frame-Level Labels

Useful for generic avoid benchmarking:

- `corridor_blocked`
- `left_escape_open`
- `right_escape_open`
- `should_avoid`

### Candidate-Level Labels

Useful for lightweight ML refinement:

- `candidate_is_real_obstacle`

Expected schema:

```text
candidate_labels.csv
  run_name
  frame_idx
  candidate_id
  target
  point_count
  mean_x
  mean_y
  mean_z
  extent_x
  extent_y
  extent_z
  pca_ratio
  persistence_frames
```

## Why Keep Striker Metrics If The Goal Is Generic?

Because the striker adapter is already available and makes current failure modes visible early.

It is a bootstrap task, not the final abstraction.
