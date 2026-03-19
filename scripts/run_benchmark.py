#!/usr/bin/env python
"""Run the UCR benchmark and save metrics to CSV.

Usage:
    uv run python scripts/run_benchmark.py                          # all built-ins, quick datasets
    uv run python scripts/run_benchmark.py -c MiniROCKET            # single classifier
    uv run python scripts/run_benchmark.py -c MiniROCKET HIVE-COTEV2
    uv run python scripts/run_benchmark.py -d GunPoint Coffee       # specific datasets
    uv run python scripts/run_benchmark.py --dataset-suite standard # use STANDARD_DATASETS
    uv run python scripts/run_benchmark.py -o results/my_run.csv    # custom output path
"""

import argparse
from pathlib import Path

import ucr_benchmark as bench


def main() -> None:
    parser = argparse.ArgumentParser(description="Run UCR benchmark")
    parser.add_argument(
        "-c", "--classifiers",
        nargs="+",
        default=None,
        help="Classifier names to benchmark (default: all built-in)",
    )
    parser.add_argument(
        "-d", "--datasets",
        nargs="+",
        default=None,
        help="Dataset names to benchmark (overrides --dataset-suite)",
    )
    parser.add_argument(
        "--dataset-suite",
        choices=["quick", "standard"],
        default="quick",
        help="Predefined dataset suite (default: quick)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("results/benchmark_results.csv"),
        help="Output CSV path (default: results/benchmark_results.csv)",
    )
    args = parser.parse_args()

    classifiers = args.classifiers or bench.list_classifiers()
    if args.datasets:
        datasets = args.datasets
    elif args.dataset_suite == "standard":
        datasets = bench.STANDARD_DATASETS
    else:
        datasets = bench.QUICK_DATASETS

    args.output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Classifiers: {classifiers}")
    print(f"Datasets:    {datasets}")
    print()

    results = bench.run(classifiers, datasets, save_path=args.output)

    df = bench.to_dataframe(results)
    print(df.to_string(index=False))
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
