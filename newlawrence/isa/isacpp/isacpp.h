#ifndef ISACPP_H
#define ISACPP_H

#define layers 4

typedef unsigned int uint;

const double R = 287.05287;
const double g = 9.80665;

class ISACpp {

    double dT;
    static const double al[layers];
    static const double hl[layers];
    double Tl[layers];
    double pl[layers];
    double rhol[layers];

    ISACpp(const ISACpp &other);    // No copy constructor allowed

    double Ts(double h, double h0, double a0, double T0) const;
    double ps(double h, double h0, double a0, double T0,
              double p0) const;
    double rhos(double h, double h0, double a0, double T0,
                double rho0) const;

    double sgn(double x) const;
    double d(double x) const;
    double u(double x) const;
    uint select(double h) const;

public:

    ISACpp(double delta_T = 0.);
    int T(double *h, uint n_h, double *T, uint n_T);
    int p(double *h, uint n_h, double *p, uint n_T);
    int rho(double *h, uint n_h, double *rho, uint n_T);
};

#endif
