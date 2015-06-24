#ifndef ISACPP_H
#define ISACPP_H

class ISACpp {

    class T_Layer {
        double hs, a, Ts;

    public:
        T_Layer();
        void set(double hs_, double a_, double Ts_);
        double operator()(const double &h) const;
    };

    class p_Layer {
        double (p_Layer::*pl)(const double&) const;
        double R, g, hs, a, Ts, ps;

    public:
        p_Layer();
        void set(double R_, double g_, double hs_,
                 double a_, double Ts_, double ps_);
        double operator()(const double &h) const;
        double pl_noTgrad(const double &h) const;
        double pl_Tgrad(const double &h) const;
    };

    double R, g;
    double *hl, *al;
    double T0, p0;
    int parallel_size, layers;

    T_Layer *Tl;
    p_Layer *pl;

    ISACpp(const ISACpp &other);    // No copy constructor allowed

    double rhol(const double &T, const double &p) const;
    int select(const double &h) const;

public:
    ISACpp(double R_, double g_, double *hl_, int n_hl,
           double *al_, int n_al, double T0_, double p0_,
           int psize);
    ~ISACpp();

    int atm(double *h, int n_h, double *T, int n_T,
            double *p, int n_p, double *rho, int n_rho) const;
};

#endif
