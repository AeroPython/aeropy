#ifndef ISACPP_H
#define ISACPP_H

#define layers 9

typedef const double cdouble;

cdouble R = 287.05;
cdouble g = 9.80665;

class ISACpp {

    double _dT;
    double al[layers] = {-0.00649, 0., 0.00099, 0.00277,
                         0., -0.00275,-0.00196, 0., 0.};
    double hl[layers] = {0., 11019., 20063., 32162., 47350.,
                         51413., 71802., 86000., 90000.};
    double Tl[layers];
    double pl[layers];
    double rhol[layers];

    ISACpp(const ISACpp &other);

    double Ts(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0) const;
    double ps(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0,
              cdouble &p0) const;
    double rhos(cdouble &h, cdouble &h0, cdouble &a0, cdouble &T0,
                cdouble &rho0) const;

    double T(cdouble &h) const;
    double p(cdouble &h) const;
    double rho(cdouble &h) const;

    double sgn(cdouble &x) const;
    double d(cdouble &x) const;
    double u(cdouble &x) const;

public:

    ISACpp(double dT = 0.);
    int T(double *h, int n_h, double *T, int n_T);
    int p(double *h, int n_h, double *p, int n_T);
    int rho(double *h, int n_h, double *rho, int n_T);
};

#endif
