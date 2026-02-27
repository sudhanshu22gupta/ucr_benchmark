"""RunHooks base class for lifecycle extensibility (e.g. future MLFlow)."""

from __future__ import annotations

from ucr_benchmark._types import BenchmarkResult


class RunHooks:
    """Base class with no-op lifecycle hooks."""

    def on_benchmark_start(
        self, classifier_names: list[str], dataset_names: list[str]
    ) -> None:
        pass

    def on_run_start(self, classifier_name: str, dataset_name: str) -> None:
        pass

    def on_run_end(self, result: BenchmarkResult) -> None:
        pass

    def on_benchmark_end(self, results: list[BenchmarkResult]) -> None:
        pass


class NullHooks(RunHooks):
    """Default hooks implementation — does nothing."""

    # Inherits all no-ops from RunHooks.


# Future MLFlow integration:
#
# class MLFlowHooks(RunHooks):
#     def on_benchmark_start(self, classifier_names, dataset_names):
#         mlflow.set_experiment("ucr_benchmark")
#
#     def on_run_start(self, classifier_name, dataset_name):
#         mlflow.start_run(run_name=f"{classifier_name}/{dataset_name}")
#
#     def on_run_end(self, result):
#         mlflow.log_metrics({"accuracy": result.accuracy, ...})
#         mlflow.end_run()
