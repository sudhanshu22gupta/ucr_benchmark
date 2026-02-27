# UCR Benchmark

Benchmark time series classifiers on [UCR archive](https://www.cs.ucr.edu/%7Eeamonn/time_series_data_2018/) datasets.

Built-in classifiers (via [aeon](https://www.aeon-toolkit.org/)):

- **MiniROCKET** — fast convolution-based
- **HIVE-COTEV2** — hybrid ensemble
- **InceptionTime** — deep learning (requires `tensorflow`)

## Quick start

```bash
uv sync
```

```python
import ucr_benchmark as bench

results = bench.run(["MiniROCKET"], bench.QUICK_DATASETS)
df = bench.to_dataframe(results)
print(df)
```

## Adding a custom classifier

```python
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier

bench.register("KNN-DTW", lambda: KNeighborsTimeSeriesClassifier(distance="dtw"))
results = bench.run(["KNN-DTW"], ["GunPoint"])
```

## Running tests

```bash
uv run pytest
```
