import warnings
import numpy as np
from isa.isacpp import ISACpp

blimit = 0.
tlimit = 90000.

def std(h, dT=0.):

    h = np.asarray(h, dtype=np.float64, order='c').flatten()
    dT = np.float64(dT)

    T = np.empty(h.shape)
    p = np.empty(h.shape)
    rho = np.empty(h.shape)

    ISA = ISACpp(dT)
    ISA.T(h, T)
    ISA.p(h, p)
    ISA.rho(h, rho)

    
    mask1 = h < blimit
    mask2 = h > tlimit
    if mask1.any() or mask2.any():
        warnings.warn("Altitude value outside range", RuntimeWarning)
        for item in (T, p, rho):
            item[mask1] = np.nan
            item[mask2] = np.nan

    if h.shape[0] == 1:
        return T.item(), p.item(), rho.item()
    else:
        return T, p, rho
