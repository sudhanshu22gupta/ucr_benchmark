"""Built-in classifier factory registrations.

Each factory uses lazy imports so that heavy dependencies (e.g. tensorflow for
InceptionTime) are only loaded when the classifier is actually instantiated.
"""

from __future__ import annotations

from ucr_benchmark.registry import register


def _make_minirocket():
    from aeon.classification.convolution_based import MiniRocketClassifier

    return MiniRocketClassifier()


def _make_hivecotev2():
    from aeon.classification.hybrid import HIVECOTEV2

    return HIVECOTEV2()


def _make_inceptiontime():
    from aeon.classification.deep_learning import InceptionTimeClassifier

    return InceptionTimeClassifier()


register("MiniROCKET", _make_minirocket)
register("HIVE-COTEV2", _make_hivecotev2)
register("InceptionTime", _make_inceptiontime)
