# coding: utf-8
"""ISA function, minimal working example.

"""
import numpy as np
import warnings


def std(h):
    if isinstance(h, float) and h < 0.0:
        warnings.warn("Altitude value outside range", RuntimeWarning)

    return 288.15, 101325.0, 1.2250
