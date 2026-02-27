"""Foundation types for the benchmark framework."""

from __future__ import annotations

import dataclasses
from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Classifier(Protocol):
    """Protocol matching sklearn/aeon classifiers."""

    def fit(self, X: np.ndarray, y: np.ndarray) -> Classifier: ...

    def predict(self, X: np.ndarray) -> np.ndarray: ...


ClassifierFactory = type["Classifier"] | type[object]  # any callable returning Classifier


@dataclasses.dataclass(frozen=True)
class BenchmarkResult:
    """Result of a single classifier × dataset run."""

    classifier_name: str
    dataset_name: str
    accuracy: float | None = None
    f1_weighted: float | None = None
    train_time_s: float | None = None
    predict_time_s: float | None = None
    error: str | None = None
