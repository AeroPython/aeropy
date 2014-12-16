/* -*- C -*-  (not really, but good for syntax highlighting) */
%module isacpp
%{ 
    #define SWIG_FILE_WITH_INIT
    #include "isacpp.h"
%}

%include "numpy.i"

%init %{
import_array();
%}

%inline %{
typedef unsigned int uint;
%}

%apply (double* IN_ARRAY1, int DIM1) {(double *h, uint n_h)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *T, uint n_T)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *p, uint n_p)};
%apply (double* INPLACE_ARRAY1, int DIM1) {(double *rho, uint n_rho)};

%include "isacpp.h"
