import copy
import warnings

import numpy as np
from isa.isacpp import ISACpp


class ISA:

    def __init__(self, **kwargs):

        self.__build(**kwargs)

    def __build(self, **kwargs):

        ints = {'psize': 100}
        doubles = {'R': 287.05287,
                   'g': 9.80665,
                   'T0': 288.15,
                   'p0': 101325}
        arrays = {'hl': [0., 11000., 20000., 32000.],
                  'al': [-0.0065, 0.0000, 0.0010]}

        for item in ints.keys():
            ints[item] = np.int(kwargs[item]) \
                if item in kwargs.keys() else np.int(ints[item])
        for item in doubles.keys():
            doubles[item] = np.float64(kwargs[item]) \
                if item in kwargs.keys() else np.float64(doubles[item])
        for item in arrays.keys():
            arrays[item] = np.atleast_1d(kwargs[item]).astype(np.float64) \
                if item in kwargs.keys() else \
                np.atleast_1d(arrays[item]).astype(np.float64)
        self.__params = {}
        self.__params.update(ints)
        self.__params.update(doubles)
        self.__params.update(arrays)

        assert self.__params['hl'].size == self.__params['al'].size + 1, \
            '"hl" array must be a unit higher than "al" array in size'

        self.__ISA = ISACpp(self.__params['R'], self.__params['g'],
                            self.__params['hl'], self.__params['al'],
                            self.__params['T0'], self.__params['p0'],
                            self.__params['psize'])

    @property
    def params(self):

        return copy.deepcopy(self.__params)

    def set(self, **kwargs):

        self.__build(**kwargs)

    def atm(self, h):

        h = np.atleast_1d(h).astype(np.float64)
        T = np.empty(h.shape)
        p = np.empty(h.shape)
        rho = np.empty(h.shape)

        error = self.__ISA.atm(h, T, p, rho)
        if(error > 0):
            warnings.warn('Altitude value outside range', RuntimeWarning)

        if h.shape[0] == 1:
            return T.item(), p.item(), rho.item()
        else:
            return T, p, rho


def get_atm(**kwargs):

    default_isa = ISA(**kwargs)

    def atm(h, dT=0.):

        if dT != 0.:
            params = default_isa.params
            params['T0'] += dT
            isa = ISA(**params)
            return isa.atm(h)
        else:
            return default_isa.atm(h)
    return atm

atm = get_atm()
