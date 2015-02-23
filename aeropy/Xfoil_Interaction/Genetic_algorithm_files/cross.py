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




def cross(parents, num_pop):
    children = np.zeros([num_pop, 16])
    num_parents = parents.shape[0]
    children[0:num_parents] = parents
    for i in np.arange(num_parents, num_pop, 1):
        coef = np.random.rand(num_parents)
        coef = coef/sum(coef)
        children[i,:]= np.dot(coef, parents)
        
    return children

