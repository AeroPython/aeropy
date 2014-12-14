#include <cmath>
#include <iostream>

#include "isacpp.h"

using namespace std;

const double ISACpp::al[layers] = {-0.0065,  0.0000, 0.0010, 0.0028}; 
// To extend the model: 0.0000, -0.0028, -0.0020, 0.0000, 0.0000

const double ISACpp::hl[layers] = {    0., 11019., 20063., 32162.};
// To extend the model: 47350., 51413., 71802., 86000., 90000.

ISACpp::ISACpp(const ISACpp &original) {}

ISACpp::ISACpp(double delta_T) : dT(delta_T) {

    // Temperatures in the points of layer change
    Tl[0] = 288.15 + dT;
    for(uint i = 1; i < layers; i++)
        Tl[i] = Ts(hl[i], hl[i - 1], al[i - 1], Tl[i - 1]);

    // Pressures and densities in the points of layer change
    pl[0] = 101325;
    rhol[0] = pl[0] / (R * Tl[0]);
    for(uint i = 1; i < layers; i++) {
        pl[i] = ps(hl[i], hl[i - 1], al[i - 1], Tl[i - 1], pl[i - 1]);
        rhol[i] = pl[i] / (R * Tl[i]);
    }
}

double ISACpp::Ts(double h, double h0, double a0, double T0) const {

    return T0 + a0 * (h - h0);
}


double ISACpp::ps(double h, double h0, double a0, double T0,
                  double p0) const {

    double p = 0;

    if(d(a0))    // 1 if T grad is 0
        p = p0 * exp(-g * (h - h0) / (R * T0));
    else
        p = p0 * pow((1. + a0 * (h - h0) / T0), -g / (R * a0));

    return p;
}

double ISACpp::rhos(double h, double h0, double a0, double T0,
                    double rho0) const {

    double rho = 0;

    if(d(a0))    // 1 if T grad is 0
        rho = rho0 * exp(-g * (h - h0) / (R * T0));
    else
        rho = rho0 * pow((1. + a0 * (h - h0) / T0), -1. - g / (R * a0));

    return rho;
}

double ISACpp::T(double h) const {
 
    uint l = select(h);
    double T = 0;
    
    T = Ts(h, hl[l], al[l], Tl[l]);

    return T;
}

double ISACpp::p(double h) const {
 
    uint l = select(h);
    double p = 0;

    p = ps(h, hl[l], al[l], Tl[l], pl[l]);

    return p;
}

double ISACpp::rho(double h) const {
 
    uint l = select(h);
    double rho = 0;

    rho = rhos(h, hl[l], al[l], Tl[l], rhol[l]);

    return rho;
}

int ISACpp::T(double *h, uint n_h, double *T, uint n_T) {

    if(n_h != n_T)
        return -1;    // Dimensions mismatch
    
    for(uint i = 0; i < n_h; i++)
        if(h[i] >= 0.)
            T[i] = this->T(h[i]);

    return 0;    // Everything OK
}

int ISACpp::p(double *h, uint n_h, double *p, uint n_T) {

    if(n_h != n_T)
        return -1;    // Dimensions mismatch
    
    for(uint i = 0; i < n_h; i++)
        if(h[i] >= 0.)
            p[i] = this->p(h[i]);

    return 0;    // Everything OK
}

int ISACpp::rho(double *h, uint n_h, double *rho, uint n_T) {

    if(n_h != n_T)
        return -1;    // Dimensions mismatch
    
    for(uint i = 0; i < n_h; i++)
        if(h[i] >= 0.)
            rho[i] = this->rho(h[i]);

    return 0;    // Everything OK
}

double ISACpp::sgn(double x) const {

    return (x > 0.) - (x < 0.);
}

double ISACpp::d(double x) const {

    if(abs(x) < 1e-12)
        return 1.;
    else
        return 0.;
}

double ISACpp::u(double x) const {

    return (1. + sgn(x)) / 2. + d(x) / 2.;
}

uint ISACpp::select(double h) const {

    uint i;
    for(uint j = 0; j < layers - 1; j++) {
        i = (j + 1) * (u(h - hl[j]) - u(h - hl[j + 1]));
        if(i > 0)
            break;
    }
    if(u(h - hl[layers - 1]) == 1)
        i = layers;

    return i - 1;
}
