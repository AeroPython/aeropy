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


def selection(score, genome, num_parent):
    invscore = 1- score
    positions = np.argsort(invscore)
    parents = np.zeros([num_parent,16])
    for i in np.arange(0,num_parent,1):
        parents[i,:] = genome[positions[i],:]
    
    return parents