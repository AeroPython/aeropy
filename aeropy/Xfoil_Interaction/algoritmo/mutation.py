'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the Mutation subprogramme. Its objective is to add diversity
to the population, in order to avoid stagnation in a not good solution.

Intensity of the mutation is propotional to the square root of the generation 
number, in order to refine the search for an optimal solution.

The parents of the generation are left unmutated in order to avoid the chance
of decreasing the quality obtained in a previous step.

'''




import numpy as np
import algoritmo.testing as test

def mutation(children, generation, num_parent):
    '''Given a genome, mutates it in order to have a diverse population
    '''
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
    
    len_pop = len(children)
    
    #children_n = children.copy()
    
    for airfoil_num in range(num_parent, len_pop):
        deviation = coeff * np.random.randn(16) * gen_deviation
        airfoil = children[airfoil_num]
        proposed_genome = airfoil.genome + deviation
        n = 0
        while not(test.airfoil_test(proposed_genome)):
            n = n + 1
            deviation = coeff * np.random.randn(16) * gen_deviation
            proposed_genome = airfoil.genome + deviation
            print('mutating into viable airfoil, try #',n)
        airfoil.genome = proposed_genome
    
   
