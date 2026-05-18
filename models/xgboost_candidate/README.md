# XGBoost Candidate Classifier

This model is intended to classify geometric obstacle candidates as:

- real obstacle
- false positive

## Why This Model First

- strong baseline for tabular features
- fast to train
- low-latency inference
- easy to inspect feature importance

## Expected Input

Candidate-level CSV with one row per candidate and a binary target column.

See [docs/dataset.md](../../docs/dataset.md) for the intended schema.
