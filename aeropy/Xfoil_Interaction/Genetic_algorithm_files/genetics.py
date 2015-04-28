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
import analyze as analyze
import selection as selection
import cross as cross
import mutation as mutation



def genetic_step(generation,num_parent, weights):
    '''Returns the genome of the (n+1)generation
    '''
    file_parent_name = 'generation'+ str(generation) + '.txt'
    genome_parent_root = os.path.join('genome', file_parent_name)    
    genome = np.loadtxt(genome_parent_root, skiprows=1)
    num_pop = genome.shape[0]
    results_data = analyze.pop_analice(generation, num_pop)
    
    scores = analyze.score(generation,num_pop, weights)
    parents = selection.selection(scores, genome, num_parent)
    children = cross.cross(parents, num_pop)
    children = mutation.mutation(children, generation, num_parent)
    
    profile_number = children.shape[0] 
    
    
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
    
    genome_file = open(genome_root, mode = 'x')
    results_file = open(results_root, mode = 'x')
    genome_file.write(title + '\n')
    results_file.write(results_title + '\n')
    results_file.write('Cl max   Eficciency      Score' + '\n')
    
    for profile in np.arange(0, profile_number, 1):
        line = ''
        for gen in np.arange(0, 16,1):
            line = line + str(children[profile, gen]) +'    '
        line = line + '\n'
        genome_file.write(line)
        result = str(results_data[profile, 0]) + '   ' 
        result = result + str(results_data[profile, 1]) + '   '
        result = result + str(scores[profile]) + '\n'
        results_file.write(result)
    
    genome_file.close()
    results_file.close()    
    return children