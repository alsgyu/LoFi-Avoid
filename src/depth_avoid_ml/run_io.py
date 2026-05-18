from __future__ import annotations

from pathlib import Path

import pandas as pd


def parse_run_spec(spec: str) -> tuple[str, Path]:
    if "=" in spec:
        label, path = spec.split("=", 1)
    else:
        path = spec
        label = Path(path).name
    return label, Path(path).expanduser().resolve()


def load_depth_metrics(run_dir: Path) -> pd.DataFrame:
    path = run_dir / "depth_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def load_striker_metrics(run_dir: Path) -> pd.DataFrame:
    path = run_dir / "striker_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
