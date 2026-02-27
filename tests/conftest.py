"""Shared fixtures for the test suite."""

from __future__ import annotations

import numpy as np
import pytest

from ucr_benchmark import registry


class DummyClassifier:
    """Always predicts the first class seen during fit."""

    def fit(self, X: np.ndarray, y: np.ndarray) -> DummyClassifier:
        self.first_class_ = y[0]
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.full(X.shape[0], self.first_class_)


@pytest.fixture(autouse=True)
def _clean_registry():
    """Clear the registry before and after every test."""
    registry.clear()
    yield
    registry.clear()


@pytest.fixture()
def dummy_dataset():
    """Synthetic 3-D arrays mimicking a UCR dataset.

    Returns ``(X_train, y_train, X_test, y_test)`` with shape
    ``(n_samples, 1, 20)`` and two classes ``"0"`` / ``"1"``.
    """
    rng = np.random.default_rng(42)
    X_train = rng.standard_normal((20, 1, 20))
    y_train = np.array(["0"] * 10 + ["1"] * 10)
    X_test = rng.standard_normal((10, 1, 20))
    y_test = np.array(["0"] * 5 + ["1"] * 5)
    return X_train, y_train, X_test, y_test
