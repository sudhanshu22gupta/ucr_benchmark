# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

UCR Benchmark — benchmarks time series classifiers on [UCR archive](https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/) datasets using the [aeon](https://www.aeon-toolkit.org/) toolkit.

## Commands

```bash
uv sync                              # install dependencies
uv run pytest                        # run all tests
uv run pytest tests/test_runner.py   # run a single test file
uv run pytest -k test_name           # run a single test by name
uv run python scripts/run_benchmark.py                    # all built-in classifiers, quick datasets
uv run python scripts/run_benchmark.py -c MiniROCKET      # single classifier
uv run python scripts/run_benchmark.py -c MiniROCKET HIVE-COTEV2  # multiple classifiers
uv run python scripts/run_benchmark.py -d GunPoint Coffee  # specific datasets
uv run python scripts/run_benchmark.py --dataset-suite standard   # use STANDARD_DATASETS (15)
uv run python scripts/run_benchmark.py -o results/my_run.csv      # custom output path
```

## Architecture

The library is a src-layout package (`src/ucr_benchmark/`) with a flat module structure:

- **Registry pattern** (`registry.py`): Global `_REGISTRY` dict mapping classifier names to zero-arg factory functions. `register()` adds entries; `get()` retrieves them. `clear()` exists for test isolation.
- **Built-in classifiers** (`classifiers.py`): Registers MiniROCKET, HIVE-COTEV2, and InceptionTime via lazy imports (heavy deps like tensorflow only load on instantiation). This module is imported for side-effects in `__init__.py`.
- **Runner** (`runner.py`): `run()` iterates classifier × dataset combinations, catches per-run exceptions into `BenchmarkResult.error`, and optionally saves CSV. Uses `_single_run()` internally which calls `load_dataset`, fits, predicts, and computes accuracy/f1.
- **Hooks** (`_hooks.py`): `RunHooks` base class provides lifecycle callbacks (`on_benchmark_start`, `on_run_start`, `on_run_end`, `on_benchmark_end`). `NullHooks` is the default no-op. Designed for future MLflow integration.
- **Types** (`_types.py`): `Classifier` protocol (fit/predict) and frozen `BenchmarkResult` dataclass.
- **Datasets** (`datasets.py`): Wraps `aeon.datasets.load_classification`. Defines `QUICK_DATASETS` (5) and `STANDARD_DATASETS` (15) name lists. Returns 3-D arrays `(n_samples, n_channels, n_timepoints)`.
- **Results** (`results.py`): `to_dataframe()` and `to_csv()` convert `BenchmarkResult` lists.

## Testing

Tests use an autouse `_clean_registry` fixture (in `conftest.py`) that clears the global registry before and after every test. A `DummyClassifier` fixture and synthetic `dummy_dataset` fixture are available for tests that don't need real UCR data or aeon classifiers.

## Key Details

- Python >=3.10, managed with `uv`
- CSV results tracked with Git LFS (`.gitattributes`)
- Adding a classifier: call `bench.register("Name", factory_fn)` where factory is a zero-arg callable returning a fit/predict object
- InceptionTime requires tensorflow (`[deep]` optional dep)
