"""UCR Benchmark — benchmark time series classifiers on UCR archive datasets."""

from ucr_benchmark._types import BenchmarkResult
from ucr_benchmark.datasets import QUICK_DATASETS, STANDARD_DATASETS, load_dataset
from ucr_benchmark.registry import list_classifiers, register
from ucr_benchmark.results import to_csv, to_dataframe
from ucr_benchmark.runner import run

# Side-effect: register built-in classifiers.
import ucr_benchmark.classifiers as classifiers  # noqa: F401, E402

__all__ = [
    "BenchmarkResult",
    "QUICK_DATASETS",
    "STANDARD_DATASETS",
    "list_classifiers",
    "load_dataset",
    "register",
    "run",
    "to_csv",
    "to_dataframe",
]
