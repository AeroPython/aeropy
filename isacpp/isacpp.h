#ifndef ISACPP_H
#define ISACPP_H

#define layers 9

using namespace std;

const double R = 287.05;
const double g = 9.80665;

class ISACpp {

    double _dT;
    double al[layers] = {-0.00649, 0., 0.00099, 0.00277,
                         0., -0.00275,-0.00196, 0., 0.};
    double hl[layers] = {0., 11019., 20063., 32162., 47350.,
                         51413., 71802., 86000., 90000.};
    double Tl[layers];
    double pl[layers];
    double rhol[layers];

    ISACpp(const ISACpp& other);

    double T(double h);
    double p(double h);
    double rho(double h);

    double sgn(double x);
    double d(double x);
    double u(double x);

public:

    ISACpp(double dT = 0.);
    int T(double *h, int n_h, double *T, int n_T);
    int p(double *h, int n_h, double *p, int n_T);
    int rho(double *h, int n_h, double *rho, int n_T);
};

#endif
