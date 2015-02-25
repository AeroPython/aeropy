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
import genetics as genetics

if not os.path.exists('aerodata'):
        os.makedirs('aerodata')
        
if not os.path.exists('genome'):
        os.makedirs('genome')

generation = 0
starting_profiles = 30
total_generations = 10
num_parent = 3
ambient_data = ('Earth', 0.3, 11, 'mach', 0.5)

genome = initial.start_pop(starting_profiles)

interfaz.xfoil_calculate_population(generation, ambient_data)


#arange antes en 0

for generation in np.arange(0,total_generations,1):
    
    genome = genetics.genetic_step(generation,num_parent)
    
    interfaz.xfoil_calculate_population(generation + 1, ambient_data)
    
    
    
    
    
    