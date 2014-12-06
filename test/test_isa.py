# coding: utf-8
"""Tests of the ISA functions.

All numerical results are validated against the `COESA`_ standard.

.. _`COESA`: http://hdl.handle.net/2060/19770009539

Based on scikit-aero (c) 2012 scikit-aero authors.

"""
import numpy as np
from numpy.testing import (assert_equal, assert_almost_equal,
                           assert_array_equal, assert_array_almost_equal)

from isa import std


def test_sea_level():
    h = 0.0  # km
    expected_T = 273.15  # K
    expected_p = 101325.0  # Pa
    expected_rho = 1.2250  # kg / m3

    T, p, rho = std(h)

    # Reads: "Assert if T equals expected_T"
    assert_equal(T, expected_T)
    assert_equal(p, expected_p)
    assert_almost_equal(rho, expected_rho, decimal=4)
