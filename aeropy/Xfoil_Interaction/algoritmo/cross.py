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
from algoritmo.initial import Airfoil


def cross(parents, pop_len, generation):
    '''Generates a population of (num_pop) airfoil genomes by mixing randomly
    the genomes of the given parents.
    The parents are preserved as the first elements of the new population.
    '''
    children = []
    parents_len = len(parents)
    
    for parent_num in range(len(parents)):
        parent = parents[parent_num]
        parent.copy_data(generation + 1, parent_num)
        children.append(parent)
        
    for child_num in range(parents_len, pop_len):
        parent_1 = parents[np.random.choice(parents_len)]
        parent_2 = parents[np.random.choice(parents_len)]
        genome_1 = parent_1.genome
        genome_2 = parent_2.genome
        child_genome = []
        coefs = np.random.rand(len(genome_1))
        for gen_num in range(len(genome_1)):
            gen = genome_1[gen_num] * coefs[gen_num]
            gen += genome_2[gen_num] * (1- coefs[gen_num])
            child_genome.append(gen)
        child_genome = np.array(child_genome)
        child = Airfoil(child_genome)
        children.append(child)
        
    return children

