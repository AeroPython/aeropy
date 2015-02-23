'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the main program. It will call the different submodules
and manage the data transfer between them in order to achieve the
genetic optimization of the profile.

'''



import subprocess
import sys
import os
import interfaz as interfaz
import numpy as np
import initial as initial
import testing as test

def mutation(children, generation, num_parent):
    coeff = 0.5 / (1 + generation**0.5)
    gen_deviation = np.array([10*np.pi/180, #ang s1
                  0.15,           #dist s1
                  0.2,           #x 1
                  0.1,           #y 1
                  10*np.pi/180,  #ang 1
                  0.2,           #dist b1
                  0.2,           #dist c1
                  0.1,           #dist a1
                  0.1,          #dist a2
                  0.4,           #x 2
                  0.05,          #y 2
                  10*np.pi/180,   #ang 2
                  0.2,           #dist b2 
                  0.2,           #dist c2
                  30*np.pi/180, #ang s2
                  0.15])          #dist s2
    
    pop_num = children.shape[0]
    
    children_n = children.copy()
    
    for i in np.arange(num_parent, pop_num, 1):
        deviation = coeff * np.random.randn(16) * gen_deviation
        children_n[i,:] = children[i,:] + deviation
        n = 0
        while not(test.test_perfil(children_n[i,:])):
            n = n + 1
            deviation = coeff * np.random.randn(16) * gen_deviation
            children_n[i,:] = children[i,:] + deviation
            print('mutando perfil viable, intento',n)
        children[i,:] = children_n[i,:]
    
    return children
