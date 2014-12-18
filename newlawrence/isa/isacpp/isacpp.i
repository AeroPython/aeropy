/* -*- C -*- */
%module isacpp
%{ 
    #define SWIG_FILE_WITH_INIT
    #include "isacpp.h"
%}

%include "numpy.i"

%init %{
import_array();
%}

%apply (double* IN_ARRAY1, int DIM1) {(double *h, int n_h)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *T, int n_T)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *p, int n_p)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *rho, int n_rho)};

%include "isacpp.h"
