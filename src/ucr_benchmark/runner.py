"""Benchmark orchestration."""

from __future__ import annotations

import time
from collections.abc import Sequence
from pathlib import Path

from sklearn.metrics import accuracy_score, f1_score

from ucr_benchmark._hooks import NullHooks, RunHooks
from ucr_benchmark._types import BenchmarkResult
from ucr_benchmark.datasets import load_dataset
from ucr_benchmark.registry import get


def run(
    classifier_names: Sequence[str],
    dataset_names: Sequence[str],
    *,
    hooks: RunHooks | None = None,
    save_path: str | Path | None = None,
) -> list[BenchmarkResult]:
    """Run benchmarks for every classifier × dataset combination.

    Returns a list of :class:`BenchmarkResult`, one per combination.
    Exceptions are caught per-run and recorded in ``BenchmarkResult.error``.

    If *save_path* is given, results are written to that CSV file after all
    runs complete.
    """
    hooks = hooks or NullHooks()
    classifier_names = list(classifier_names)
    dataset_names = list(dataset_names)
    hooks.on_benchmark_start(classifier_names, dataset_names)

    results: list[BenchmarkResult] = []
    for clf_name in classifier_names:
        for ds_name in dataset_names:
            hooks.on_run_start(clf_name, ds_name)
            try:
                result = _single_run(clf_name, ds_name)
            except Exception as exc:
                result = BenchmarkResult(
                    classifier_name=clf_name,
                    dataset_name=ds_name,
                    error=str(exc),
                )
            hooks.on_run_end(result)
            results.append(result)

    hooks.on_benchmark_end(results)

    if save_path is not None:
        from ucr_benchmark.results import to_csv

        to_csv(results, save_path)

    return results


def _single_run(clf_name: str, ds_name: str) -> BenchmarkResult:
    factory = get(clf_name)
    clf = factory()
    X_train, y_train, X_test, y_test = load_dataset(ds_name)

    t0 = time.perf_counter()
    clf.fit(X_train, y_train)
    train_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    y_pred = clf.predict(X_test)
    predict_time = time.perf_counter() - t0

    return BenchmarkResult(
        classifier_name=clf_name,
        dataset_name=ds_name,
        accuracy=accuracy_score(y_test, y_pred),
        f1_weighted=f1_score(y_test, y_pred, average="weighted"),
        train_time_s=train_time,
        predict_time_s=predict_time,
    )
