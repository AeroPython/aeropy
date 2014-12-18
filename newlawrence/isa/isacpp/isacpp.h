#ifndef ISACPP_H
#define ISACPP_H

#define layers 4

class ISACpp {

    static const double R, g;
    static const double al[layers], hl[layers];

    double dT;
    double Tl[layers], pl[layers], rhol[layers];

    ISACpp(const ISACpp &other);    // No copy constructor allowed

    int select(double h) const;

public:

    ISACpp(double delta_T = 0.);

    double Ts(double h, double h0, double a0, double T0) const;
    double ps(double h, double h0, double a0, double T0,
              double p0) const;
    double rhos(double h, double h0, double a0, double T0,
                double rho0) const;

    int atm(double *h, int n_h, double *T, int n_T,
            double *p, int n_p, double *rho, int n_rho) const;

};

#endif
