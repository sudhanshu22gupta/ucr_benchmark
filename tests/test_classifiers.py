"""Tests for built-in classifier registrations."""

from __future__ import annotations

from ucr_benchmark import registry


def test_builtins_registered():
    """Importing classifiers module registers the three built-ins."""
    # classifiers module is imported by __init__, but registry is cleared by
    # the autouse fixture.  Re-import to trigger registrations.
    import importlib
    import ucr_benchmark.classifiers

    importlib.reload(ucr_benchmark.classifiers)

    names = registry.list_classifiers()
    assert "MiniROCKET" in names
    assert "HIVE-COTEV2" in names
    assert "InceptionTime" in names
