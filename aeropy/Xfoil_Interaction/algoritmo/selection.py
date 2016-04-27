'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the selection subprogramme. Given a population and a score array, 
it just selects the (num_parent) best and ignores the rest.

This has its own subprogramme because other genetic algorithms have 
other selection parameters, so this can be easily found and changed here
if you wanted.

'''




import numpy as np


def selection(population, num_parent):
    '''Select the genome of the (num_parent) best airfoils.
    '''
    pop_len = len(population)
    score = np.zeros(pop_len)
    for airfoil_num in range(pop_len):
        airfoil = population[airfoil_num]
        score[airfoil_num] = airfoil.score
    invscore = 1- score
    positions = np.argsort(invscore)
    parents =[]
    for parent_count in range(num_parent):
        parents.append(population[positions[parent_count]])
    
    return parents