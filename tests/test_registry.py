"""Tests for the classifier registry."""

from __future__ import annotations

import pytest

from ucr_benchmark.registry import clear, get, list_classifiers, register


class TestRegister:
    def test_register_and_get(self):
        register("A", lambda: "clf_a")
        assert get("A")() == "clf_a"

    def test_duplicate_raises(self):
        register("A", lambda: None)
        with pytest.raises(ValueError, match="already registered"):
            register("A", lambda: None)

    def test_unknown_raises(self):
        with pytest.raises(KeyError, match="Unknown classifier"):
            get("nope")

    def test_list_classifiers_sorted(self):
        register("B", lambda: None)
        register("A", lambda: None)
        assert list_classifiers() == ["A", "B"]

    def test_clear(self):
        register("A", lambda: None)
        clear()
        assert list_classifiers() == []
