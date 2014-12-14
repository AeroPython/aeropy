# coding: utf-8
"""ISA functions.

Author: Juan Luis Cano Rodríguez <juanlu001@gmail.com>

"""

import numpy as np
import warnings

# Constants
R_a = 287.05287  # J/(Kg·K)
g0 = 9.80665  # m/s^2
T0 = 288.15  # K
p0 = 101325.0  # Pa

alpha = np.array([-6.5e-3, 0.0, 1.0e-3])  # K / m

# Computed constants
# This prevents UnboundLocalError to arise
# "With this value of T_M,b [b = 0] defined, and the set of six
# values of H_b and the six corresponding to values of L_M,b
# defined in table 4, the function T_M of H is completely defined
# from the surface to 84.8520 km' (86 km)."
# Therefore I should not define a variable T1 in advance.
T1 = T0 + alpha[0] * 11000.0  # FIXME: Repeated code
p1 = p0 * (T0 / (T0 + alpha[0] * 11000.0)) ** (g0 / (R_a * alpha[0]))
T2 = T1
p2 = p1 * np.exp(-g0 * (20000.0 - 11000.0) / (R_a * T1))


def atm(h, dT=0.0):
    """Standard atmosphere temperature, pressure and density.

    Parameters
    ----------
    h : array-like
        Geopotential altitude, m.

    """
    h = np.atleast_1d(h).astype(float)
    scalar = (h.size == 1)
    assert len(h.shape) == 1
    T = np.empty_like(h)
    p = np.empty_like(h)
    rho = np.empty_like(h)
    for ii in range(h.size):
        if h[ii] < 0.0:
            warnings.warn("Altitude value outside range", RuntimeWarning)
            T[ii] = np.nan
            p[ii] = np.nan
        elif 0.0 <= h[ii] < 11000.0:
            T[ii] = T0 + alpha[0] * h[ii]
            p[ii] = p0 * (T0 / (T0 + alpha[0] * h[ii])) ** (g0 / (R_a * alpha[0]))
        elif 11000.0 <= h[ii] < 20000.0:
            T[ii] = T1#  + alpha[1] * (h[ii] - 11000.0)
            p[ii] = p1 * np.exp(-g0 * (h[ii] - 11000.0) / (R_a * T1))
        elif 20000.0 <= h[ii] <= 32000.0:
            T[ii] = T2 + alpha[2] * (h[ii] - 20000.0)
            p[ii] = p2 * (T2 / (T2 + alpha[2] * (h[ii] - 20000.0))) ** (g0 / (R_a * alpha[2]))
    rho = p / (R_a * T)

    if scalar:
        T = T[0]
        p = p[0]
        rho = rho[0]

    return T, p, rho
