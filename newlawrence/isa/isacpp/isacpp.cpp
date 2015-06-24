#include <limits>
#include <cmath>

#include "isacpp.h"
#include "cstmath.h"

using namespace std;
using namespace custom_math;

// T_Layer class

ISACpp::T_Layer::T_Layer() {}

void ISACpp::T_Layer::set(double hs_, double a_, double Ts_) {

    hs = hs_, a = a_;
    Ts = Ts_;
}

double ISACpp::T_Layer::operator()(const double &h) const {

    return Ts + a * (h - hs);
}

// p_Layer class

ISACpp::p_Layer::p_Layer() {}

void ISACpp::p_Layer::set(double R_, double g_, double hs_,
                          double a_, double Ts_, double ps_) {

    R = R_, g = g_;
    hs = hs_, a = a_;
    Ts = Ts_, ps = ps_;

    if(d(a))
        pl = &p_Layer::pl_noTgrad;
    else
        pl = &p_Layer::pl_Tgrad;
}

double ISACpp::p_Layer::operator()(const double &h) const {

    return (this->*pl)(h);
}

double ISACpp::p_Layer::pl_noTgrad(const double &h) const {

    return ps * exp(-g * (h - hs) / (R * Ts));
}

double ISACpp::p_Layer::pl_Tgrad(const double &h) const {

    return ps * pow((1. + a * (h - hs) / Ts), -g / (R * a));
}

// ISACpp class

ISACpp::ISACpp(const ISACpp &original) {}    // No copy constructor allowed

double ISACpp::rhol(const double &T, const double &p) const {

    return p / (R * T);
}

int ISACpp::select(const double &h) const {

    int i = 1;

    for(int j = 0; j < layers; j++) {
        i = (j + 1) *
            static_cast<int>(u(h - hl[j]) - u(h - hl[j + 1]));
        if(i > 0)
            break;
    }
    if(u(h - hl[layers - 1]) == 1)
        i = layers;

    return i - 1;
}

ISACpp::ISACpp(double R_, double g_, double *hl_, int n_hl,
               double *al_, int n_al, double T0_, double p0_,
               int psize) :
               R(R_), g(g_), hl(hl_), al(al_),
               T0(T0_), p0(p0_), parallel_size(psize) {

    // Set the number of layers
    layers = n_al;

    //Allocate memory for functions
    Tl = new T_Layer[layers];
    pl = new p_Layer[layers];

    // Temperature and pressure layers
    Tl[0].set(0., al[0], T0);
    pl[0].set(R, g, 0., al[0], T0, p0);
    for(int i = 1; i < layers; i++) {
        Tl[i].set(hl[i], al[i], Tl[i - 1](hl[i]));
        pl[i].set(R, g, hl[i], al[i], Tl[i - 1](hl[i]), pl[i - 1](hl[i]));
    }
}

ISACpp::~ISACpp() {

    delete[] Tl;
    delete[] pl;
}

int ISACpp::atm(double *h, int n_h, double *T, int n_T,
                double *p, int n_p, double *rho, int n_rho) const {

    int parallel = 0;
    int error = 0;    // Error flag
    int l;

    if((n_h != n_T) && (n_h != n_p) && (n_h != n_rho))
        return -1;    // Dimensions mismatch

    if(n_h > parallel_size)
		parallel = 1;    // Turn on parallelism for large loops

    #pragma omp parallel shared(T, p, rho, error) private(l) if(parallel)
    {
        #pragma omp for schedule(static)
        for(int i = 0; i < n_h; i++)
            if((h[i] >= 0.) && (h[i] <= hl[layers])) {
                l = select(h[i]);
                T[i] = Tl[l](h[i]);
                p[i] = pl[l](h[i]);
                rho[i] = rhol(T[i], p[i]);
            }
            else {
                T[i] = numeric_limits<double>::quiet_NaN();
                p[i] = numeric_limits<double>::quiet_NaN();
                rho[i] = numeric_limits<double>::quiet_NaN();
                error = 1;    // Out of bounds
            }
    }

    return error;    // Everything OK
}
