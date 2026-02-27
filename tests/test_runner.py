"""Tests for the benchmark runner."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from conftest import DummyClassifier

from ucr_benchmark._hooks import RunHooks
from ucr_benchmark.registry import register
from ucr_benchmark.runner import run


@pytest.fixture()
def _register_dummy():
    register("dummy", DummyClassifier)


def _make_dummy_data(*_args, **_kwargs):
    rng = np.random.default_rng(0)
    X = rng.standard_normal((10, 1, 20))
    y = np.array(["0"] * 5 + ["1"] * 5)
    return X, y, X, y


class TestRun:
    @patch("ucr_benchmark.runner.load_dataset", side_effect=_make_dummy_data)
    def test_single_run(self, _mock_load, _register_dummy):
        results = run(["dummy"], ["FakeDS"])
        assert len(results) == 1
        r = results[0]
        assert r.classifier_name == "dummy"
        assert r.dataset_name == "FakeDS"
        assert r.accuracy is not None
        assert r.f1_weighted is not None
        assert r.train_time_s >= 0
        assert r.predict_time_s >= 0
        assert r.error is None

    @patch("ucr_benchmark.runner.load_dataset", side_effect=_make_dummy_data)
    def test_cartesian_product(self, _mock_load, _register_dummy):
        results = run(["dummy"], ["DS1", "DS2"])
        assert len(results) == 2
        assert {r.dataset_name for r in results} == {"DS1", "DS2"}

    @patch("ucr_benchmark.runner.load_dataset", side_effect=RuntimeError("boom"))
    def test_error_recorded(self, _mock_load, _register_dummy):
        results = run(["dummy"], ["BadDS"])
        assert len(results) == 1
        assert results[0].error == "boom"
        assert results[0].accuracy is None

    @patch("ucr_benchmark.runner.load_dataset", side_effect=_make_dummy_data)
    def test_hooks_called(self, _mock_load, _register_dummy):
        hooks = MagicMock(spec=RunHooks)
        run(["dummy"], ["DS1"], hooks=hooks)
        hooks.on_benchmark_start.assert_called_once()
        hooks.on_run_start.assert_called_once_with("dummy", "DS1")
        hooks.on_run_end.assert_called_once()
        hooks.on_benchmark_end.assert_called_once()
