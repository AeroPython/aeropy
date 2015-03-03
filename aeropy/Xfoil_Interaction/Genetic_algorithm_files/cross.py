'''

Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the cross subprogramme. Its objective is to generate 
a whole new population genome from the genome of the previous generation
winners (parents).

In order to eliminate the chance of randomly getting worse results,
the parents are preserved as the first elements of the new population.

'''




import numpy as np



def cross(parents, num_pop):
    '''Generates a population of (num_pop) airfoil genomes by mixing randomly
    the genomes of the given parents.
    The parents are preserved as the first elements of the new population.
    '''
    children = np.zeros([num_pop, 16])
    num_parents = parents.shape[0]
    children[0:num_parents] = parents
    for i in np.arange(num_parents, num_pop, 1):
        coef = np.random.rand(num_parents)
        coef = coef/sum(coef)
        children[i,:]= np.dot(coef, parents)
        
    return children

