import warnings
import numpy as np
from isa.isacpp import ISACpp

def atm(h, dT=0.):

    h = np.asarray(h, dtype=np.float64, order='c').flatten()
    dT = np.float64(dT)

    T = np.empty(h.shape)
    p = np.empty(h.shape)
    rho = np.empty(h.shape)

    error = 0
    ISA = ISACpp(dT)
    error += ISA.T(h, T)
    error += ISA.p(h, p)
    error += ISA.rho(h, rho)
    if(error > 0):
        warnings.warn("Altitude value outside range", RuntimeWarning)

    if h.shape[0] == 1:
        return T.item(), p.item(), rho.item()
    else:
        return T, p, rho
