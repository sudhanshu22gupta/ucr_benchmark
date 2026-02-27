"""Tests for result formatting and export."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ucr_benchmark._types import BenchmarkResult
from ucr_benchmark.results import to_csv, to_dataframe

_SAMPLE = BenchmarkResult(
    classifier_name="A",
    dataset_name="DS",
    accuracy=0.9,
    f1_weighted=0.88,
    train_time_s=1.2,
    predict_time_s=0.3,
)


class TestToDataframe:
    def test_columns(self):
        df = to_dataframe([_SAMPLE])
        assert list(df.columns) == [
            "classifier_name",
            "dataset_name",
            "accuracy",
            "f1_weighted",
            "train_time_s",
            "predict_time_s",
            "error",
        ]

    def test_values(self):
        df = to_dataframe([_SAMPLE])
        assert df.iloc[0]["accuracy"] == 0.9

    def test_empty_list(self):
        df = to_dataframe([])
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0


class TestToCsv:
    def test_round_trip(self, tmp_path: Path):
        csv_path = tmp_path / "results.csv"
        to_csv([_SAMPLE], csv_path)
        df = pd.read_csv(csv_path)
        assert len(df) == 1
        assert df.iloc[0]["classifier_name"] == "A"
