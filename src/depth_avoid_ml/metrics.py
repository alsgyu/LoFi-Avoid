from __future__ import annotations

from collections import Counter

import pandas as pd


def summarize_run(label: str, depth_df: pd.DataFrame, striker_df: pd.DataFrame) -> dict:
    decisions = Counter(striker_df["decision"]) if not striker_df.empty and "decision" in striker_df else Counter()

    def mean_or_zero(df: pd.DataFrame, col: str) -> float:
        if df.empty or col not in df:
            return 0.0
        return float(df[col].mean())

    def p95_or_zero(df: pd.DataFrame, col: str) -> float:
        if df.empty or col not in df:
            return 0.0
        return float(df[col].quantile(0.95))

    def max_or_zero(df: pd.DataFrame, col: str) -> float:
        if df.empty or col not in df:
            return 0.0
        return float(df[col].max())

    return {
        "label": label,
        "depth_frames": int(len(depth_df)),
        "striker_frames": int(len(striker_df)),
        "mean_sampled_valid_points": round(mean_or_zero(depth_df, "sampled_valid_points"), 3),
        "mean_candidate_points": round(mean_or_zero(depth_df, "candidate_points"), 3),
        "mean_nonempty_cells": round(mean_or_zero(depth_df, "nonempty_cells"), 3),
        "mean_occupied_cells": round(mean_or_zero(depth_df, "occupied_cells"), 3),
        "mean_pca_pass_cells": round(mean_or_zero(depth_df, "pca_pass_cells"), 3),
        "mean_final_obstacles": round(mean_or_zero(depth_df, "final_obstacles"), 3),
        "p95_final_obstacles": round(p95_or_zero(depth_df, "final_obstacles"), 3),
        "max_final_obstacles": round(max_or_zero(depth_df, "final_obstacles"), 3),
        "front_blocked_ratio": round(mean_or_zero(striker_df, "front_blocked"), 3),
        "dribble_ready_ratio": round(mean_or_zero(striker_df, "dribble_ready"), 3),
        "auto_visual_kick_ready_ratio": round(mean_or_zero(striker_df, "auto_visual_kick_ready"), 3),
        "quick_shoot_after_dribble_ratio": round(mean_or_zero(striker_df, "quick_shoot_after_dribble"), 3),
        "mean_left_lane_open_width": round(mean_or_zero(striker_df, "left_lane_open_width"), 3),
        "mean_right_lane_open_width": round(mean_or_zero(striker_df, "right_lane_open_width"), 3),
        "top_decisions": "|".join(f"{name}:{count}" for name, count in decisions.most_common(5)),
    }
