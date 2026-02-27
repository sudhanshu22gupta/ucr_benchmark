"""Dataset name lists and loading helper."""

from __future__ import annotations

import numpy as np
from aeon.datasets import load_classification

QUICK_DATASETS: list[str] = [
    "ArrowHead",
    "BME",
    "Chinatown",
    "Coffee",
    "GunPoint",
]

STANDARD_DATASETS: list[str] = [
    "ArrowHead",
    "BME",
    "Chinatown",
    "Coffee",
    "ECG200",
    "GunPoint",
    "ItalyPowerDemand",
    "MiddlePhalanxTW",
    "Plane",
    "SonyAIBORobotSurface1",
    "SyntheticControl",
    "Trace",
    "TwoLeadECG",
    "UMD",
    "Wafer",
]


def load_dataset(
    name: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Load a UCR dataset by name.

    Returns ``(X_train, y_train, X_test, y_test)`` with 3-D X arrays
    shaped ``(n_samples, n_channels, n_timepoints)``.
    """
    X_train, y_train = load_classification(name, split="train")
    X_test, y_test = load_classification(name, split="test")
    return X_train, y_train, X_test, y_test
