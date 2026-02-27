"""Classifier registry — Strategy pattern hub."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_REGISTRY: dict[str, Callable[[], Any]] = {}


def register(name: str, factory: Callable[[], Any]) -> None:
    """Register a classifier factory under *name*. Raises on duplicates."""
    if name in _REGISTRY:
        raise ValueError(f"Classifier {name!r} is already registered")
    _REGISTRY[name] = factory


def get(name: str) -> Callable[[], Any]:
    """Return the factory for *name*, or raise ``KeyError``."""
    try:
        return _REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise KeyError(
            f"Unknown classifier {name!r}. Available: {available}"
        ) from None


def list_classifiers() -> list[str]:
    """Return sorted list of registered classifier names."""
    return sorted(_REGISTRY)


def clear() -> None:
    """Remove all registrations (for test isolation)."""
    _REGISTRY.clear()
