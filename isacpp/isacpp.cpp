#include <cmath>

#include "isacpp.h"

ISACpp::ISACpp(const ISACpp &original) {}

ISACpp::ISACpp(double dT) : _dT(dT) {

    Tl[0] = 288.15 + _dT;
    for(int i = 1; i < layers; i++)
        Tl[i] = ((1. - d(al[i - 1])) * (Tl[i - 1] + al[i - 1] *
                (hl[i] - hl[i - 1])) + d(al[i - 1]) * Tl[i - 1]);

    pl[0] = 101325;
    rhol[0] = pl[0] / R * Tl[0];
    for(int i = 1; i < layers; i++) {
        pl[i] = ((1. - d(al[i - 1])) *
                (pl[i - 1] * pow((1. - al[i - 1] *
                (hl[i] - hl[i - 1]) / Tl[i - 1]), (g / (R * al[i - 1])))) +
                d(al[i - 1]) * pl[i - 1] *
                exp(g * (hl[i - 1] - hl[i]) / (R * Tl[i - 1])));
        rhol[i] = pl[i] / R * Tl[i];
    }
}

double ISACpp::T(double h) {
 
    int l = layers - 1;
    double T = 0;

    for(int i = 0; i < l; i++)
        T += (u(h - hl[i]) - u(h - hl[i + 1])) *
             ((1. - d(al[i])) * (Tl[i] + al[i] * (h - hl[i])) +
             d(al[i]) * Tl[i]);
    T += u(h - hl[l]) * ((1. - d(al[l])) * (Tl[l] + al[l] * (h - hl[l])) +
         d(al[l]) * Tl[l]);

    return T;
}

double ISACpp::p(double h) {
 
    int l = layers - 1;
    double p = 0;

    for(int i = 0; i < l; i++)
        p += (u(h - hl[i]) - u(h - hl[i + 1])) *
             ((1. - d(al[i])) *
             (pl[i] * pow((1. - al[i] *
             (h - hl[i]) / Tl[i]), (g / (R * al[i])))) +
             d(al[i]) * pl[i] * exp(g * (hl[i] - h) / (R * Tl[i])));
    p += (u(h - hl[l])) * ((1. - d(al[l])) *
         (pl[l] * pow((1. - al[l] * h / Tl[l]), (g / (R * al[l])))) +
         d(al[l]) * pl[l] * exp(g * (hl[l] - h) / (R * Tl[l])));

    return p;
}

double ISACpp::rho(double h) {
 
    int l = layers - 1;
    double rho = 0;

    for(int i = 0; i < l; i++)
        rho += (u(h - hl[i]) - u(h - hl[i + 1])) *
             ((1. - d(al[i])) *
             (rhol[i] * pow((1. - al[i] *
             (h - hl[i]) / Tl[i]), (g / (R * al[i]) - 1.))) +
             d(al[i]) * rhol[i] * exp(g * (hl[i] - h) / (R * Tl[i])));
    rho += (u(h - hl[l])) * ((1. - d(al[l])) *
         (rhol[l] * pow((1. - al[l] * h / Tl[l]), (g / (R * al[l]) - 1.))) +
         d(al[l]) * rhol[l] * exp(g * (hl[l] - h) / (R * Tl[l])));

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

double ISACpp::sgn(double x) {
    return (x > 0.) - (x < 0.);
}

double ISACpp::d(double x) {
    if(abs(x) < 1e-12)
        return 1.;
    else
        return 0.;
}

double ISACpp::u(double x) {
    return (1. + sgn(x)) / 2. + d(x) / 2.;
}
