#!/usr/bin/env python
"""Run the UCR benchmark and save metrics to CSV.

Usage:
    uv run python scripts/run_benchmark.py
"""

from pathlib import Path

import ucr_benchmark as bench

OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

CLASSIFIERS = ["MiniROCKET", "HIVE-COTEV2", "InceptionTime"]
DATASETS = bench.QUICK_DATASETS

print(f"Classifiers: {CLASSIFIERS}")
print(f"Datasets:    {DATASETS}")
print()

save_path = OUTPUT_DIR / "benchmark_results.csv"
results = bench.run(CLASSIFIERS, DATASETS, save_path=save_path)

df = bench.to_dataframe(results)
print(df.to_string(index=False))
print(f"\nResults saved to {save_path}")
