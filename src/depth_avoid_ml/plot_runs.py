from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .metrics import summarize_run
from .run_io import load_depth_metrics, load_striker_metrics, parse_run_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate figures from exported run CSVs.")
    parser.add_argument(
        "--run",
        action="append",
        required=True,
        help="Run spec as LABEL=/abs/path/to/run_dir or just /abs/path/to/run_dir.",
    )
    parser.add_argument("--out-dir", required=True)
    return parser.parse_args()


def normalize_time(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=float)
    return df["stamp_sec"] - float(df["stamp_sec"].iloc[0])


def moving_average(series: pd.Series, window: int = 15) -> pd.Series:
    if series.empty:
        return series
    return series.rolling(window=window, min_periods=1).mean()


def plot_single_run(label: str, run_dir: Path, out_dir: Path) -> dict:
    depth_df = load_depth_metrics(run_dir)
    striker_df = load_striker_metrics(run_dir)
    summary = summarize_run(label, depth_df, striker_df)

    if not depth_df.empty:
        t = normalize_time(depth_df)
        plt.figure(figsize=(12, 6))
        for col in [
            "sampled_valid_points",
            "candidate_points",
            "nonempty_cells",
            "occupied_cells",
            "pca_pass_cells",
            "final_obstacles",
        ]:
            lw = 2.4 if col == "final_obstacles" else 1.5
            plt.plot(t, depth_df[col], label=col, linewidth=lw)
        plt.title(f"{label}: Depth Pipeline Counts")
        plt.xlabel("Time Since Run Start (s)")
        plt.ylabel("Count")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / f"{label}_depth_pipeline_counts.png", dpi=180)
        plt.close()

        plt.figure(figsize=(8, 5))
        plt.hist(depth_df["final_obstacles"], bins=20, color="#4472c4", alpha=0.85)
        plt.title(f"{label}: Final Obstacle Histogram")
        plt.xlabel("Final Obstacles Per Frame")
        plt.ylabel("Frames")
        plt.grid(alpha=0.25)
        plt.tight_layout()
        plt.savefig(out_dir / f"{label}_final_obstacles_hist.png", dpi=180)
        plt.close()

    if not striker_df.empty:
        t = normalize_time(striker_df)
        plt.figure(figsize=(12, 6))
        plt.plot(t, striker_df["left_lane_open_width"], label="left_lane_open_width")
        plt.plot(t, striker_df["right_lane_open_width"], label="right_lane_open_width")
        plt.plot(t, moving_average(striker_df["front_blocked"]), label="front_blocked_ma15")
        plt.plot(t, moving_average(striker_df["dribble_ready"]), label="dribble_ready_ma15")
        plt.plot(t, moving_average(striker_df["auto_visual_kick_ready"]), label="auto_visual_kick_ready_ma15")
        plt.title(f"{label}: Downstream Signals")
        plt.xlabel("Time Since Run Start (s)")
        plt.ylabel("Width / Ratio")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / f"{label}_striker_signals.png", dpi=180)
        plt.close()

        decision_counts = striker_df["decision"].value_counts()
        plt.figure(figsize=(10, 5))
        plt.bar(decision_counts.index, decision_counts.values, color="#70ad47")
        plt.title(f"{label}: Decision Distribution")
        plt.xlabel("Decision")
        plt.ylabel("Frames")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()
        plt.savefig(out_dir / f"{label}_decision_distribution.png", dpi=180)
        plt.close()

    return summary


def plot_compare_runs(summaries: list[dict], out_dir: Path) -> None:
    if len(summaries) < 2:
        return
    labels = [row["label"] for row in summaries]
    xs = list(range(len(labels)))
    width = 0.26

    plt.figure(figsize=(12, 6))
    plt.bar([x - width for x in xs], [row["mean_candidate_points"] for row in summaries], width=width, label="mean_candidate_points")
    plt.bar(xs, [row["mean_pca_pass_cells"] for row in summaries], width=width, label="mean_pca_pass_cells")
    plt.bar([x + width for x in xs], [row["mean_final_obstacles"] for row in summaries], width=width, label="mean_final_obstacles")
    plt.xticks(xs, labels, rotation=15, ha="right")
    plt.ylabel("Mean Count")
    plt.title("Depth Pipeline Comparison")
    plt.grid(axis="y", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "compare_depth_pipeline.png", dpi=180)
    plt.close()

    plt.figure(figsize=(12, 6))
    width = 0.25
    plt.bar([x - width for x in xs], [row["front_blocked_ratio"] for row in summaries], width=width, label="front_blocked_ratio")
    plt.bar(xs, [row["dribble_ready_ratio"] for row in summaries], width=width, label="dribble_ready_ratio")
    plt.bar([x + width for x in xs], [row["auto_visual_kick_ready_ratio"] for row in summaries], width=width, label="auto_visual_kick_ready_ratio")
    plt.xticks(xs, labels, rotation=15, ha="right")
    plt.ylabel("Ratio")
    plt.ylim(0.0, 1.0)
    plt.title("Downstream Signal Comparison")
    plt.grid(axis="y", alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "compare_downstream_signals.png", dpi=180)
    plt.close()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    summaries = []
    for run_spec in args.run:
        label, run_dir = parse_run_spec(run_spec)
        if not run_dir.exists():
            raise SystemExit(f"Run directory not found: {run_dir}")
        summaries.append(plot_single_run(label, run_dir, out_dir))

    if summaries:
        pd.DataFrame(summaries).to_csv(out_dir / "run_summary.csv", index=False)
    plot_compare_runs(summaries, out_dir)


if __name__ == "__main__":
    main()
