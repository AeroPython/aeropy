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
import analice as analice
import selection as selection
import cross as cross
import mutation as mutation




def genetic_step(generation,num_parent):
    
    genome_parent_root = 'genome\generation'+ str(generation) + '.txt'    
    genome = np.loadtxt(genome_parent_root, skiprows=1)
    num_pop = genome.shape[0]
    
    scores = analice.score(generation,num_pop)
    parents = selection.selection(scores, genome, num_parent)
    children = cross.cross(parents, num_pop)
    children = mutation.mutation(children, generation, num_parent)
    
    profile_number = children.shape[0]    
    genome_root = 'genome\generation'+ str(generation + 1) + '.txt'
    title = 'generation' + str(generation + 1) + 'genome'
    
    try:
        os.remove(genome_root)
    except :
        pass
    archivo = open(genome_root, mode = 'x')
    archivo.write(title + '\n')
    
    for profile in np.arange(0, profile_number, 1):
        line = ''
        for gen in np.arange(0, 16,1):
            line = line + str(children[profile, gen]) +'    '
        line = line + '\n'
        archivo.write(line)
    return children