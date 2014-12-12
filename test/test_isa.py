# coding: utf-8
"""Tests of the ISA functions.

All numerical results are validated against the `COESA`_ standard.

.. _`COESA`: http://hdl.handle.net/2060/19770009539

Based on scikit-aero (c) 2012 scikit-aero authors.

"""
import numpy as np
from numpy.testing import (assert_equal, assert_almost_equal,
                           assert_array_equal, assert_array_almost_equal)

import pytest

from isa import std


def test_sea_level():
    h = 0.0  # km
    expected_T = 288.15  # K
    expected_p = 101325.0  # Pa
    expected_rho = 1.2250  # kg / m3

    T, p, rho = std(h)

    # Reads: "Assert if T equals expected_T"
    assert_equal(T, expected_T)
    assert_equal(p, expected_p)
    assert_almost_equal(rho, expected_rho, decimal=4)


def test_scalar_input_returns_scalar_output():
    h = 0.0  # km

    T, p, rho = std(h)

    # Reads: "Assert if T is a float"
    assert isinstance(T, float)
    assert isinstance(p, float)
    assert isinstance(rho, float)


def test_array_input_returns_array_output():
    num = 5
    h = np.zeros(5)  # km

    T, p, rho = std(h)

    # Reads: "Assert if the length of T equals num"
    # Notice that T has to be a sequence in the first place or len(T)
    # will raise TypeError
    assert_equal(len(T), num)
    assert_equal(len(p), num)
    assert_equal(len(rho), num)


def test_emits_warning_for_altitude_outside_range(recwarn):
    h = -1.0  # km

    std(h)
    warning = recwarn.pop(RuntimeWarning)

    assert issubclass(warning.category, RuntimeWarning)


def test_values_outside_range_are_nan():
    h = np.array([-1.0, 0.0])  # km

    T, p, rho = std(h)

    assert_equal(T[0], np.nan)
    assert_equal(p[0], np.nan)
    assert_equal(rho[0], np.nan)


def test_results_under_11km():
    h = np.array([0.0,
                  0.05,
                  0.55,
                  6.5,
                  10.0,
                  11.0
    ])  # km
    expected_T = np.array([288.150,
                           287.825,
                           284.575,
                           245.900,
                           223.150,
                           216.650
    ])  # K
    expected_p = np.array([101325.0,
                           100720.0,
                           94890.0,
                           44034.0,
                           26436.0,
                           22632.0
    ])  # Pa
    expected_rho = np.array([1.2250,
                             1.2191,
                             1.1616,
                             0.62384,
                             0.41271,
                             0.36392
    ])  # kg / m3

    T, p, rho = std(h)

    assert_array_almost_equal(T, expected_T, decimal=3)
    assert_array_almost_equal(p, expected_p, decimal=-1)
    assert_array_almost_equal(rho, expected_rho, decimal=4)
