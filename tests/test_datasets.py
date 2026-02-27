"""Tests for dataset helpers."""

from __future__ import annotations

from unittest.mock import patch

import numpy as np

from ucr_benchmark.datasets import QUICK_DATASETS, STANDARD_DATASETS, load_dataset


def test_quick_datasets_non_empty():
    assert len(QUICK_DATASETS) > 0
    assert all(isinstance(n, str) for n in QUICK_DATASETS)


def test_standard_datasets_non_empty():
    assert len(STANDARD_DATASETS) > 0
    assert all(isinstance(n, str) for n in STANDARD_DATASETS)


def test_quick_is_subset_of_standard():
    assert set(QUICK_DATASETS).issubset(set(STANDARD_DATASETS))


def test_load_dataset_delegates_to_aeon():
    dummy_X = np.zeros((5, 1, 10))
    dummy_y = np.array(["a"] * 5)

    with patch("ucr_benchmark.datasets.load_classification") as mock_load:
        mock_load.return_value = (dummy_X, dummy_y)
        X_train, y_train, X_test, y_test = load_dataset("FakeDataset")

    assert mock_load.call_count == 2
    mock_load.assert_any_call("FakeDataset", split="train")
    mock_load.assert_any_call("FakeDataset", split="test")
    np.testing.assert_array_equal(X_train, dummy_X)
    np.testing.assert_array_equal(y_test, dummy_y)
