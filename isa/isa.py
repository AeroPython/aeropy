# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 21:25:16 2014

@author: alex.saez.12@gmail.com
"""

import numpy as np
import warnings


R_a = 287.05287    # J/(Kg·K)
g = 9.80665    # m/s^2

# Used for adimensionalization
T_0 = 288.15
P_0 = 101325
rho_0 = P_0 / (R_a * T_0)

# Used for altitude conversion
# Mean earth radious
r0 = 6356766    # m


def layer(h0, T0, P0, alpha):
    """
    Layer constructor

    Parameters
    ----------
    h0 : float
        Initial height of the layer [m].
    T0 : float
        Initial temperature of the layer [K].
    P0 : float
        Initial pressure of the layer [Pa].
    alpha : float
        Temperature gradient of the layer [K/m].

    Returns
    -------
    out : func
        function that accepts height as input
        and returns T, P, rho.

    Notes
    -----
    This could be implemented as a class with methods
    __init__ and __call__

    """

    rho0 = P0 / (R_a * T0)

    if alpha == 0:

        def constant_temp_layer(h):
            """
            Layer with constant temperature
            """

            T = T0 * np.ones_like(h)
            h = h - h0

            constant = - g / (R_a * T0)
            exp = np.exp(constant * h)

            P = P0 * exp
            rho = rho0 * exp

            return T, P, rho

        return constant_temp_layer

    else:

        def linear_temp_layer(h):
            """
            Layer with lineal temperature variation
            """

            h = h - h0

            constant_1 = alpha / T0
            constant_2 = -g / (R_a * alpha)

            base = (1 + constant_1 * h)

            T = T0 * base
            P = P0 * base ** constant_2
            rho = rho0 * base ** (constant_2 - 1)

            return T, P, rho

        return linear_temp_layer


def atm(h, deltaT=0.0, adim=False):
    """
    Standard atmosphere temperature, pressure and density values.

    Parameters
    ----------
    h : float, ndarray
        height or heights for variables calculation.
    deltaT : float, optional
        Set a temperature offset. Not verified results!!
    adim : bool, optional
        If True results returned in adimensional form theta, sigma, delta.

    Returns
    -------
    T : float, ndarray
        Temperature [K] for each height in h.
    P : float, ndarray
        Pressure [Pa] for each height in h.
    rho : float, ndarray
        Density [kg/m^3] for each height in h.

    """

    if hasattr(h, '__iter__'):

        h = np.asarray(h)

        if any(h) < 0 or any(h) > 32000:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    else:

        if h > 32000 or h < 0:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    # First layer: Troposphere
    # 0 m < h <= 11000 m
    h0 = 0
    T0 = T_0 + deltaT   # Base temperature [K]
    P0 = P_0    # Base pressure [Pa]
    alpha0 = -6.5e-3         # T gradient [K/m]

    troposphere = layer(h0, T0, P0, alpha0)

    # Second layer: Tropopause
    # 11000 m < h <= 20000 m
    h11 = 11000
    T11, P11, _ = troposphere(h11)
    alpha11 = 0    # T gradient [K/m]

    tropopause = layer(h11, T11, P11, alpha11)

    # Third layer: Stratosphere
    # 20000 m < h <= 32000
    h20 = 20000
    T20, P20, _ = tropopause(h20)
    alpha20 = 1e-3    # T gradient [K/m]

    stratosphere = layer(h20, T20, P20, alpha20)

    condlist = [h < 0,         # Out of range
                h <= 11000,    # First layer: Troposphere
                h <= 20000,    # Second layer: Tropopause
                h <= 32000,    # Third layer: Stratosphere
                h > 32000]     # Out of range

    choicelist = [np.nan,
                  troposphere(h),
                  tropopause(h),
                  stratosphere(h),
                  np.nan]

    T, P, rho = np.select(condlist, choicelist)

    if adim:

        T /= T_0
        P /= P_0
        rho /= rho_0

    return T, P, rho


def geometric_2_geopotential(h):
    """
    Computes the geopotential altitude given the geometric altitude.
    This function is based on ISA constants and is not a generalised definition
    in which earth radious and gravitation change.

    Parameters
    ----------
    h : float, ndarray
        geometric height or heights to be converted.

    Returns
    -------
    h : float, ndarray
        geopotential height or heights.

    """

    if hasattr(h, '__iter__'):
        h = np.asarray(h)
        if any(h) < 0:
            warnings.warn("Altitude value smaller than zero", RuntimeWarning)

    else:
        if h < 0:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    return r0 * h / (r0 + h)


def geopotential_2_geometric(h):
    """
    Computes the geometric altitude given the geopotential altitude.
    This function is based on ISA constants and is not a generalised definition
    in which earth radious and gravitation change.

    Parameters
    ----------
    h : float, ndarray
        geopotential height or heights to be converted.

    Returns
    -------
    h : float, ndarray
        geometric height or heights.

    """

    if hasattr(h, '__iter__'):
        h = np.asarray(h)
        if any(h) < 0:
            warnings.warn("Altitude value smaller than zero", RuntimeWarning)

    else:
        if h < 0:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    return r0 * h / (r0 - h)


def barometric_altitude(p):
    """
    Computes the barometric altitude given the static pressure at that altitude

    Parameters
    ----------
    p : float, ndarray
        static pressure.

    Returns
    -------
    h : float, ndarray
        geopotential height.
    """

    if hasattr(p, '__iter__'):
        p = np.asarray(p)
        if any(p) < 868.02 or any(p) > 101325:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    else:
        if p > 868.02 or p < 101325:
            warnings.warn("Altitude value outside range", RuntimeWarning)

    # Parameters for different layers
    layers_h = np.array([0, 11000, 20000, 32000])    # m
    layers_p = np.array([101325, 22632, 5474.9, 868.02])    # Pa
    layers_T = np.array([288.15, 216.65, 216.65])   # K
    layers_alpha = np.array([-6.5e-3, 0, 1e-3])    # K/m

    # True if the temperature gradient is linear, Flase if it is constant
    layers_gradient = np.array([True, False, True])

    # Identify current layer
    layer = np.max(np.argwhere(p <= layers_p))

    # Set layer parameters
    h0 = layers_h[layer]
    T0 = layers_T[layer]
    P0 = layers_p[layer]
    alpha = layers_alpha[layer]

    if layers_gradient[layer]:
        h = T0 / alpha * ((p / P0) ** (- R_a * alpha / g) - 1) + h0

    else:
        h = - R_a * T0 / g * np.log(p / P0) + h0

    return h
