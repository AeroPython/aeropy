#include <cmath>

#include "isacpp.h"

using namespace std;

ISACpp::ISACpp(const ISACpp &original) {}

ISACpp::ISACpp(double dT) : _dT(dT) {

    // Temperatures in the points of layer change
    Tl[0] = 288.15 + _dT;
    for(int i = 1; i < layers; i++)
        Tl[i] = Ts(hl[i], hl[i - 1], al[i - 1], Tl[i - 1]);

    // Pressures and densities in the points of layer change
    pl[0] = 101325;
    rhol[0] = pl[0] / (R * Tl[0]);
    for(int i = 1; i < layers; i++) {
        pl[i] = ps(hl[i], hl[i - 1], al[i - 1], Tl[i - 1], pl[i - 1]);
        rhol[i] = pl[i] / (R * Tl[i]);
    }
}

double ISACpp::Ts(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0) const {

    return T0 + a0 * (h - h0);
}


double ISACpp::ps(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0,
                  cdouble &p0) const {

    double p = 0;

    p += (1. - d(a0)) *    // 1 if T grad is not 0, 0 otherwise
         p0 * pow((1. + a0 * (h - h0) / T0), -g / (R * a0));
    p += d(a0) *    // 1 if T grad is 0, 0 otherwise
         p0 * exp(-g * (h - h0) / (R * T0));

    if(isnan(p))
        return 0.;

    return p;
}

double ISACpp::rhos(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0,
                    cdouble &rho0) const {

    double rho = 0;

    rho += (1. - d(a0)) *    // 1 if T grad is not 0, 0 otherwise
         rho0 * pow((1. + a0 * (h - h0) / T0), -1. - g / (R * a0));
    rho += d(a0) *    // 1 if T grad is 0, 0 otherwise
         rho0 * exp(-g * (h - h0) / (R * T0));

    if(isnan(rho))
        return 0.;

    return rho;
}

double ISACpp::T(cdouble &h) const {
 
    int l = layers - 1;
    double T = 0;

    // Temperature calculation for the first and intermediate layers
    for(int i = 0; i < l; i++)
        T += Ts(h, hl[i], al[i], Tl[i]) *
             (u(h - hl[i]) - u(h - hl[i + 1]));    // Window function
    // Temperature calculation for the outer layer
    T += Ts(h, hl[l], al[l], Tl[l]) *
         u(h - hl[l]);    // Window function

    return T;
}

double ISACpp::p(cdouble &h) const {
 
    int l = layers - 1;
    double p = 0;

    // Pressure calculation for the first and intermediate layers
    for(int i = 0; i < l; i++)
        p += ps(h, hl[i], al[i], Tl[i], pl[i]) *
             (u(h - hl[i]) - u(h - hl[i + 1]));    // Window function
    // Pressure calculation for the outer layer
    p += ps(h, hl[l], al[l], Tl[l], pl[l]) *
         u(h - hl[l]);    // Window function

    return p;
}

double ISACpp::rho(cdouble &h) const {
 
    int l = layers - 1;
    double rho = 0;

    // Pressure calculation for the first and intermediate layers
    for(int i = 0; i < l; i++)
        rho += rhos(h, hl[i], al[i], Tl[i], rhol[i]) *
             (u(h - hl[i]) - u(h - hl[i + 1]));    // Window function
    // Pressure calculation for the outer layer
    rho += rhos(h, hl[l], al[l], Tl[l], rhol[l]) *
         u(h - hl[l]);    // Window function

    return rho;
}

int ISACpp::T(double *h, int n_h, double *T, int n_T) {

    if(n_h != n_T)
        return -1;
    
    for(int i = 0; i < n_h; i++)
        T[i] = this->T(h[i]);

    return 0;
}

int ISACpp::p(double *h, int n_h, double *p, int n_T) {

    if(n_h != n_T)
        return -1;
    
    for(int i = 0; i < n_h; i++)
        p[i] = this->p(h[i]);

    return 0;
}

int ISACpp::rho(double *h, int n_h, double *rho, int n_T) {

    if(n_h != n_T)
        return -1;
    
    for(int i = 0; i < n_h; i++)
        rho[i] = this->rho(h[i]);

    return 0;
}

double ISACpp::sgn(cdouble &x) const {

    return (x > 0.) - (x < 0.);
}

double ISACpp::d(cdouble &x) const {

    if(abs(x) < 1e-12)
        return 1.;
    else
        return 0.;
}

double ISACpp::u(cdouble &x) const {

    return (1. + sgn(x)) / 2. + d(x) / 2.;
}
