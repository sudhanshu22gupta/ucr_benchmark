"""DataFrame construction and CSV export for benchmark results."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pandas as pd

from ucr_benchmark._types import BenchmarkResult


def to_dataframe(results: list[BenchmarkResult]) -> pd.DataFrame:
    """Convert a list of ``BenchmarkResult`` to a pandas DataFrame."""
    return pd.DataFrame([dataclasses.asdict(r) for r in results])


def to_csv(results: list[BenchmarkResult], path: str | Path) -> None:
    """Write benchmark results to a CSV file."""
    to_dataframe(results).to_csv(path, index=False)
