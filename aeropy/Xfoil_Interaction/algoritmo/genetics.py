# -*- coding: utf-8 -*-
'''
Created on Fri Feb 20 20:57:16 2015

@author: Siro Moreno

This is a submodule for the genetic algorithm that is explained in
https://docs.google.com/presentation/d/1_78ilFL-nbuN5KB5FmNeo-EIZly1PjqxqIB-ant-GfM/edit?usp=sharing

This script is the Genetic Step Subprograme. After the XFoil analysis of the
'N' generation, this subprogramme will calculate the population of the 
'N+1' generation. 

'''




import os
import numpy as np
import algoritmo.analyze as analyze
import algoritmo.selection as selection
import algoritmo.cross as cross
import algoritmo.mutation as mutation



def genetic_step(generation,population, num_parent, weights):
    '''Returns the genome of the (n+1)generation
    '''
#    file_parent_name = 'generation'+ str(generation) + '.txt'
#    genome_parent_root = os.path.join('genome', file_parent_name)    
#    genome = np.loadtxt(genome_parent_root, skiprows=1)
#    num_pop = genome.shape[0]
    pop_len = len(population)
    
    analyze.pop_analice(generation, population, num_parent)    
    analyze.score(generation, population, weights)
    parents = selection.selection(population, num_parent)
    children = cross.cross(parents, pop_len, generation)
    mutation.mutation(children, generation, num_parent)
    
    
    
    
    file_name = 'generation'+ str(generation + 1) + '.txt'
    genome_root = os.path.join('genome', file_name)
    title = 'generation' + str(generation + 1) + 'genome'
    
    results_name = 'results_data_generation'+ str(generation) + '.txt'
    results_root = os.path.join('results', 'data', results_name )
    results_title = 'generation' + str(generation) + 'results:'
    try:
        os.remove(genome_root)
    except :
        pass
    
    try:
        os.remove(results_root)
    except :
        pass
    
    if os.path.exists(genome_root):
        os.remove(genome_root)
    
    genome_file = open(genome_root, mode = 'x')
    results_file = open(results_root, mode = 'x')
    genome_file.write(title + '\n')
    results_file.write(results_title + '\n')
    results_file.write('Cl max   Eficciency      Score\n')
    
    for airfoil in population:
        line = ''
        for gen in airfoil.genome:
            line = line + str(gen) +'    '
        line = line + '\n'
        genome_file.write(line)
        result = str(airfoil.clmax) + '   ' 
        result += str(airfoil.maxefic) + '   '
        result += str(airfoil.score) + '\n'
        results_file.write(result)
    
    genome_file.close()
    results_file.close()    
    return children