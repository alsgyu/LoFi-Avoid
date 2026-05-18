#!/usr/bin/env python3
"""Train a first candidate-level XGBoost classifier.

This script is intentionally simple. It expects a flat CSV with:
  - one row per candidate
  - a binary `target` column
  - numeric feature columns
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

try:
    from xgboost import XGBClassifier
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "xgboost is required for this script. Install dependencies with `pip install -r requirements.txt`."
    ) from exc


DEFAULT_IGNORE = {"target", "run_name", "frame_idx", "candidate_id"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-csv", required=True, help="Labeled candidate CSV.")
    parser.add_argument("--output-model", required=True, help="Path to save the trained model.")
    parser.add_argument("--output-metrics", required=True, help="Path to save JSON metrics.")
    parser.add_argument("--output-importance", required=True, help="Path to save feature importance CSV.")
    parser.add_argument("--target-column", default="target")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.input_csv)
    if args.target_column not in df.columns:
        raise SystemExit(f"Missing target column: {args.target_column}")

    feature_cols = [
        col for col in df.columns
        if col not in DEFAULT_IGNORE and col != args.target_column
    ]
    if not feature_cols:
        raise SystemExit("No feature columns found in input CSV.")

    X = df[feature_cols]
    y = df[args.target_column].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="logloss",
        random_state=42,
    )
    model.fit(X_train, y_train)

    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)

    metrics = {
        "rows": int(len(df)),
        "features": feature_cols,
        "accuracy": float(accuracy_score(y_test, pred)),
        "f1": float(f1_score(y_test, pred)),
        "average_precision": float(average_precision_score(y_test, prob)),
        "roc_auc": float(roc_auc_score(y_test, prob)),
    }

    Path(args.output_model).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_metrics).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_importance).parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, args.output_model)
    with open(args.output_metrics, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    importance = pd.DataFrame(
        {
            "feature": feature_cols,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)
    importance.to_csv(args.output_importance, index=False)


if __name__ == "__main__":
    main()
